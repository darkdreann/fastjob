package com.fastjob.auth

import android.content.Context
import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import android.util.Log
import java.security.KeyStore
import javax.crypto.Cipher
import javax.crypto.KeyGenerator
import javax.crypto.SecretKey
import javax.crypto.spec.IvParameterSpec
import androidx.datastore.dataStore
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.runBlocking
import java.io.IOException

/**
 * Esta clase se encarga de guardar y leer las credenciales de usuario de forma segura.
 * Las credenciales se guardan en un archivo en el directorio de archivos de la aplicación.
 * El archivo se encripta con una clave que se guarda en el KeyStore del dispositivo.
 * Solo leerá las credenciales la primera vez que se inicie la aplicación.
 * Si se cambian las credenciales, se sobreescribirán las anteriores.
 * @param filesDir directorio de archivos de la aplicación.
 */
class CredentialsManager(
    private val context: Context
) {
    // constantes de la clase
    companion object {
        private const val FILE_NAME = "fastjob_credentials"
        private const val KEY_ALIAS = "fastjob_credentials_key"
        private const val KEY_STORE_TYPE = "AndroidKeyStore"
        private const val LOG_TAG = "CredentialsManager"
        private const val KEY_SIZE = 256
        private const val ALGORITHM = KeyProperties.KEY_ALGORITHM_AES
        private const val BLOCK_MODE = KeyProperties.BLOCK_MODE_CBC
        private const val PADDING = KeyProperties.ENCRYPTION_PADDING_PKCS7
        private const val TRANSFORMATION = "$ALGORITHM/$BLOCK_MODE/$PADDING"
    }

    //private val filePath: File = File(filesDir, FILE_NAME)
    private val keyStore = KeyStore.getInstance(KEY_STORE_TYPE).apply {
        load(null)
    }
    // dataStore para guardar las credenciales encriptadas
    private val Context.dataStore by dataStore(
        fileName = FILE_NAME,
        serializer = CredentialsSerializer()
    )
    private var encryptedCredentials: EncryptedCredentials

    init {
        // intenta leer las credenciales encriptadas
        encryptedCredentials = readEncryptedCredentials()
    }

    /**
     * Devuelve un cifrador para encriptar datos.
     * @return Cipher para encriptar datos.
     */
    private fun getEncryptCipher(): Cipher {
        return Cipher.getInstance(TRANSFORMATION).apply {
            init(Cipher.ENCRYPT_MODE, getKey())
        }
    }

    /**
     * Devuelve un cifrador para desencriptar datos.
     * @param iv Vector de inicialización.
     * @return Cipher para desencriptar datos.
     */
    private fun getDecryptCipher(iv: ByteArray): Cipher {
        return Cipher.getInstance(TRANSFORMATION).apply {
            init(Cipher.DECRYPT_MODE, getKey(), IvParameterSpec(iv))
        }
    }

    /**
     * Devuelve la clave para encriptar y desencriptar datos.
     * @return Clave para encriptar y desencriptar datos.
     */
    private fun getKey(): SecretKey {
        // intenta obtener la clave del KeyStore
        val key = keyStore.getEntry(KEY_ALIAS, null) as? KeyStore.SecretKeyEntry
        // si no hay clave la crea
        return key?.secretKey ?: createKey()
    }

    /**
     * Crea una clave para encriptar y desencriptar datos.
     * @return Clave para encriptar y desencriptar datos.
     */
    private fun createKey(): SecretKey {
        // crea la clave y la guarda en el KeyStore
        return KeyGenerator.getInstance(ALGORITHM).apply {
            init(
                KeyGenParameterSpec.Builder(
                    KEY_ALIAS,
                    KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
                )
                .setBlockModes(BLOCK_MODE)
                .setEncryptionPaddings(PADDING)
                .setUserAuthenticationRequired(false)
                .setRandomizedEncryptionRequired(true)
                .setKeySize(KEY_SIZE)
                .build()
            )
        }.generateKey()
    }

    /**
     * Lee las credenciales encriptadas de la dataStore.
     * Si no hay credenciales devuelve un objeto EncryptedCredentials vacío.
     *
     * @return EncryptedCredentials con las credenciales encriptadas.
     */
    private fun readEncryptedCredentials(): EncryptedCredentials = runBlocking {
        return@runBlocking context.dataStore.data.first()
    }

    /**
     * Guarda las credenciales encriptadas en la dataStore.
     */
    private fun saveEncryptedCredentials() = runBlocking {
        // guarda las credenciales encriptadas en la dataStore
        try {
            context.dataStore.updateData { encryptedCredentials }

        // si hay un error al guardar las credenciales encriptadas lo muestra en el log
        }catch (e: IOException){
            Log.e(LOG_TAG, e.message ?: e.toString())
        }

    }

    /**
     * Devuelve si hay credenciales guardadas.
     * @return true si hay credenciales guardadas, false si no.
     */
    fun isCredentialsSaved(): Boolean {
        return encryptedCredentials.notNulls()
    }

    /**
     * Encripta y guarda las credenciales pasadas por parámetro.
     * @param username Nombre de usuario.
     * @param password Contraseña.
     */
    fun setCredentials(username: String, password: String) {
        // obtiene un cifrador para encriptar los datos
        val cipher = getEncryptCipher()
        // crea un objeto Credentials con los datos pasados por parámetro
        val credentials = Credentials(username, password)

        // encripta las credenciales
        val encryptedCredentials = cipher.doFinal(credentials.toByteArray())

        // guarda las credenciales encriptadas en el objeto
        this.encryptedCredentials = EncryptedCredentials(
            cipher.iv,
            encryptedCredentials
        )

        // guarda las credenciales en la dataStore
        saveEncryptedCredentials()
    }

    /**
     * Devuelve las credenciales desencriptadas.
     * @return Credentials con las credenciales desencriptadas o null si no hay credenciales guardadas.
     */
    fun getCredentials(): Credentials? {
        // si no hay credenciales devuelve null
        if (!encryptedCredentials.notNulls())
            return null

        // desencripta las credenciales y las devuelve
        val encryptedCredentials =
            getDecryptCipher(encryptedCredentials.initializationVector!!).doFinal(
                encryptedCredentials.credentials!!
            )

        return Credentials.fromByteArray(encryptedCredentials)
    }

    /**
     * Borra las credenciales guardadas y el archivo de credenciales.
     */
    fun clearCredentials() {
        // borra las credenciales guardadas creando un objeto EncryptedCredentials vacío
        encryptedCredentials = EncryptedCredentials()

        // guarda el objeto EncryptedCredentials vacío en la dataStore
        saveEncryptedCredentials()
    }


}


