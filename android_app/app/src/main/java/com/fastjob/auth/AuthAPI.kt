package com.fastjob.auth

import android.content.Context
import android.util.Base64
import com.fastjob.models.Token
import com.fastjob.models.UserType
import com.fastjob.network.Client
import com.fastjob.services.LoginService
import com.google.gson.Gson
import com.google.gson.annotations.SerializedName
import kotlinx.coroutines.DelicateCoroutinesApi
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.Job
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking
import java.util.UUID

/**
 * Clase que se encarga de manejar la autenticación de la aplicación.
 * Se encarga de almacenar el token y de renovarlo cuando sea necesario.
 * También se encarga de almacenar las credenciales del usuario para poder iniciar sesión automáticamente.
 *
 * @param filesDir directorio de archivos de la aplicación.
 */
@OptIn(DelicateCoroutinesApi::class)
class AuthAPI private constructor(
    context: Context
) {
    // constantes de la clase
    companion object {
        private const val MAX_RETRIES = 5
        private const val TIME_DIFF_RENEW = 10 * 60
        private lateinit var instance: AuthAPI

        /**
         * Inicializa la instancia de AuthAPI.
         *
         * @param filesDir directorio de archivos de la aplicación.
         */
        fun init(context: Context) {
            if (!::instance.isInitialized)
                instance = AuthAPI(context)
        }

        /**
         * Obtiene la instancia de AuthAPI.
         * Si no se ha inicializado devuelve UninitializedPropertyAccessException.
         *
         * @throws UninitializedPropertyAccessException
         */
        @Throws(UninitializedPropertyAccessException::class)
        fun getInstance(): AuthAPI {
            return instance
        }
    }

    private val loginService = Client.getInstance().getService(LoginService::class.java)
    private val credentialsManager = CredentialsManager(context)
    private var token: Token? = null
    private var userData: UserData? = null
    private var tokenRenewJob: Job? = null



    init {
        // si hay credenciales guardadas se intenta iniciar sesión automáticamente
        if (credentialsManager.isCredentialsSaved())
            tryLogin()
    }

    /**
     * Obtiene el token de autenticación.
     * Si el token esta a punto de expirar se renueva asincronamente y se devuelve el token actual.
     * Si el token esta expirado se renueva y se devuelve el nuevo token. Si no hay credenciales guardadas devuelve null.
     * Si el token no existe (no esta autenticado) devuelve null.
     * Si el token esta vigente se devuelve el token actual.
     *
     * @return token de autenticación o null si no esta autenticado o no hay credenciales guardadas.
     */
    fun getToken(): String? {
        when (isTokenExpired()) {
            // si no esta autenticado se devuelve null
            TokenTime.NOT_AUTHENTICATED -> return null
            // si esta expirado se renueva y se devuelve el nuevo token
            TokenTime.EXPIRED -> {
                // si no hay credenciales guardadas se devuelve null
                if(!credentialsManager.isCredentialsSaved())
                    return null

                // si hay un job de renovación se cancela
                if(tokenRenewJob != null) {
                    tokenRenewJob!!.cancel()
                    tokenRenewJob = null
                }

                // se intenta iniciar sesión automáticamente
                if (!tryLogin())
                    return null
            }
            // si esta a punto de expirar se renueva asincronamente y se devuelve el token actual
            TokenTime.NEED_RENEW -> {
                // si no hay un job de renovación se crea para que no se creen varios
                if(tokenRenewJob == null)
                    // se crea un job de renovación con scope global para que no se cancele al del scope
                    tokenRenewJob = GlobalScope.launch(Dispatchers.IO) { renewToken() }

            }
            TokenTime.VALID -> Unit
        }

        // se devuelve el token actual
        return getTokenFormat()
    }

    /**
     * Obtiene el id del usuario.
     *
     * @return id del usuario o null si no esta autenticado.
     */
    fun getUserId(): UUID? {
        return userData?.userId
    }

    /**
     * Obtiene el tipo de usuario.
     *
     * @return tipo de usuario o null si no esta autenticado.
     */
    fun getUserType(): UserType? {
        return userData?.let {
            UserType.valueOf(it.userType)
        }
    }

    /**
     * Obtiene el token de autenticación en el formato "token_type token".
     *
     * @return token de autenticación en el formato "token_type token" o null si no esta autenticado.
     */
    private fun getTokenFormat(): String? {
        // si no esta autenticado se devuelve null
        if (token == null)
            return null

        return  "${token!!.tokenType} ${token!!.token}"
    }

    /**
     * Inicia sesión con las credenciales guardadas.
     * Si la petición es exitosa se guarda el token y se decodifica el payload.
     * Si la petición falla se borran las credenciales guardadas y se devuelve false.
     *
     * @return true si la petición es exitosa, false si falla.
     */
    private fun tryLogin(): Boolean {
        val (username, password) = credentialsManager.getCredentials()!!
        val loginSuccess = login(username, password)

        return when {
            loginSuccess -> true
            else -> {
                credentialsManager.clearCredentials()
                false
            }
        }
    }

    /**
     * Inicia sesión con el nombre de usuario y la contraseña.
     * Si la petición es exitosa se guarda el token y se decodifica el payload y se guardan si se indica.
     * Si la petición falla por credenciales incorrectas se devuelve false.
     *
     * @param username nombre de usuario.
     * @param password contrasena.
     * @param saveCredentials si se guardan las credenciales. Por defecto es false.
     * @param retryCount número de intentos de inicio de sesión. Por defecto es 0.
     * @return true si la petición es exitosa, false si falla por credenciales incorrectas.
     */
    fun login(username: String, password: String, saveCredentials: Boolean = false, retryCount: Int = 0) : Boolean = runBlocking {
        // se hace la petición de inicio de sesión con las credenciales guardadas
        val loginResponse = loginService.login(username, password)

        // se devuelve true si ha podido iniciar sesión o false si no
        return@runBlocking when {
            // si la petición es exitosa se guarda el token y se decodifica el payload
            loginResponse.isSuccessful -> {
                token = loginResponse.body()
                userData = decodeUserData()
                // si se indica se guardan las credenciales
                if(saveCredentials)
                    credentialsManager.setCredentials(username, password)
                true
            }
            // si la petición falla por credenciales incorrectas se devuelve false
            loginResponse.code() == 401 -> false
            // si la petición falla se intenta iniciar sesión de nuevo si no se ha superado el número de intentos
            retryCount <= MAX_RETRIES -> return@runBlocking login(username, password, saveCredentials, retryCount + 1)
            // en cualquier otro caso se devuelve false
            else -> false
        }
    }

    /**
     * Renueva el token de autenticación.
     * Si la petición es exitosa se guarda el nuevo token y se decodifica el payload.
     * Si la petición falla se intenta renovar el token de nuevo si no se ha superado el número de intentos.
     *
     * @param retryCount número de intentos de renovación. Por defecto es 0.
     */
    private suspend fun renewToken(retryCount: Int = 0) {
        // si no esta autenticado se para la función
        if (token == null)
            return

        // se obtiene el token actual
        val currentToken = getTokenFormat()!!
        // se hace la petición de renovación del token
        val renewTokenResponse = loginService.renewToken(currentToken)

        // si la petición es exitosa se guarda el nuevo token y se decodifica el payload
        when{
            renewTokenResponse.isSuccessful -> {
                token = renewTokenResponse.body()
                userData = decodeUserData()
                // se establece el job a null para que se pueda crear uno nuevo
                tokenRenewJob = null
            }
            // si la petición falla se intenta renovar el token de nuevo si no se ha superado el número de intentos
            retryCount <= MAX_RETRIES -> renewToken(retryCount + 1)
        }
    }

    /**
     * Decodifica el payload del token y lo devuelve como UserData.
     *
     * @return UserData o null si no esta autenticado.
     */
    private fun decodeUserData(): UserData? {
        // si no esta autenticado se devuelve null
        if(token == null)
            return null

        // se decodifica el payload del token
        val gson = Gson()
        val tokenPayload = token!!.token.split(".")[1]
        val decodedPayload = String(Base64.decode(tokenPayload, Base64.DEFAULT))

        return gson.fromJson(decodedPayload, UserData::class.java)
    }

    /**
     * Comprueba el estado del token.
     * Si no esta autenticado devuelve NOT_AUTHENTICATED.
     * Si esta expirado devuelve EXPIRED.
     * Si esta a punto de expirar devuelve NEED_RENEW.
     * En cualquier otro caso devuelve VALID.
     *
     * @return TokenTime
     */
    private fun isTokenExpired(): TokenTime {
        // si no esta autenticado se devuelve NOT_AUTHENTICATED
        val tokenTime = userData?.expireTime ?: return TokenTime.NOT_AUTHENTICATED
        // se obtiene la hora actual en segundos
        val currentTime = System.currentTimeMillis() / 1000

        // se comprueba el estado del token
        return when {
            // si el token esta expirado se devuelve EXPIRED
            tokenTime < currentTime -> TokenTime.EXPIRED
            // si el token esta a punto de expirar se devuelve NEED_RENEW
            tokenTime < currentTime + TIME_DIFF_RENEW -> TokenTime.NEED_RENEW
            // en cualquier otro caso se devuelve VALID
            else -> TokenTime.VALID
        }
    }

    /**
     * Actualiza la contraseña del usuario.
     * @param password nueva contraseña.
     */
    fun updatePassword(password: String) {
        credentialsManager.updatePassword(password)
    }

    /**
     * Comprueba si el usuario esta autenticado.
     *
     * @return true si esta autenticado, false si no.
     */
    fun isAuthenticated(): Boolean {
        return token != null
    }


    /**
     * Cierra la sesión del usuario.
     * Borra el token, el payload decodificado y las credenciales guardadas.
     */
    fun logout() {
        token = null
        userData = null
        credentialsManager.clearCredentials()
    }
}

/**
 * Data class para deserializar el payload del token
 */
private data class UserData(
    @SerializedName("sub")
    val userId: UUID,
    @SerializedName("user_type")
    val userType: String,
    @SerializedName("exp")
    val expireTime: Int
)

/**
 * Enum que representa el estado del token.
 */
private enum class TokenTime {
    NOT_AUTHENTICATED,
    EXPIRED,
    NEED_RENEW,
    VALID
}

