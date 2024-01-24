package com.fastjob.auth

import android.util.Log
import androidx.datastore.core.Serializer
import com.google.gson.Gson
import com.google.gson.JsonSyntaxException
import com.google.gson.annotations.SerializedName
import java.io.DataInputStream
import java.io.DataOutputStream
import java.io.InputStream
import java.io.OutputStream

/**
 * Clase para guardar las credenciales en texto plano.
 */
data class Credentials(
    val username: String,
    val password: String
){
    companion object {
        private const val LOG_TAG = "Credentials"
        private val gson = Gson()

        /**
         * Devuelve un objeto Credentials a partir de un array de bytes.
         * @param byteArray array de bytes que contiene las credenciales.
         * @return objeto Credentials.
         */
        fun fromByteArray(byteArray: ByteArray): Credentials {
            return try{
                gson.fromJson(String(byteArray), Credentials::class.java)
            }catch (e: JsonSyntaxException){
                Log.e(LOG_TAG, e.message ?: e.toString())
                Credentials("", "")
            }

        }
    }

    /**
     * Devuelve un array de bytes que contiene las credenciales.
     * @return array de bytes.
     */
    fun toByteArray(): ByteArray {
        return gson.toJson(this).toByteArray()
    }
}

/**
 * Clase para guardar las credenciales encriptadas y los vectores de inicialización.
*/

data class EncryptedCredentials(
    @SerializedName("iv")
    val initializationVector: ByteArray? = null,
    @SerializedName("credentials")
    val credentials: ByteArray? = null
) {
    /**
     * Devuelve si los vectores de inicialización y las credenciales no son null.
     *
     * @return true si no son null, false si lo son.
     */
    fun notNulls(): Boolean {
        return initializationVector != null && credentials != null
    }

    /**
     * Compara dos objetos EncryptedCredentials.
     * @param byteArray array de bytes que contiene las credenciales encriptadas.
     * @return booleano que indica si los objetos son iguales.
     */
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (javaClass != other?.javaClass) return false

        other as EncryptedCredentials

        if (!initializationVector.contentEquals(other.initializationVector)) return false
        if (!credentials.contentEquals(other.credentials)) return false

        return true
    }

    /**
     * Devuelve el hash del objeto.
     * @return hash del objeto.
     */
    override fun hashCode(): Int {
        var result = initializationVector.contentHashCode()
        result = 31 * result + credentials.contentHashCode()
        return result
    }
}

/**
 * Clase para serializar objetos EncryptedCredentials.
 */
class CredentialsSerializer: Serializer<EncryptedCredentials> {
    companion object {
        private const val LOG_TAG = "CredentialsSerializer"
        private val gson = Gson()
    }

    /**
     * Devuelve un objeto EncryptedCredentials vacío.
     * @return objeto EncryptedCredentials.
     */
    override val defaultValue: EncryptedCredentials
        get() = EncryptedCredentials()

    /**
     * Lee un objeto EncryptedCredentials de un InputStream y lo devuelve.
     *
     * @param input InputStream del que leer.
     * @return objeto EncryptedCredentials.
     */
    override suspend fun readFrom(input: InputStream): EncryptedCredentials {
        try{
            DataInputStream(input).use {
                return gson.fromJson(it.readUTF(), EncryptedCredentials::class.java)
            }
        }catch (e: Exception){
            return defaultValue
        }
    }

    /**
     * Escribe un objeto EncryptedCredentials en un OutputStream.
     *
     * @param t objeto EncryptedCredentials a escribir.
     * @param output OutputStream en el que escribir.
     */
    override suspend fun writeTo(t: EncryptedCredentials, output: OutputStream) {
        try {
            DataOutputStream(output).use {
                it.writeUTF(gson.toJson(t))
            }
        }catch (e: Exception) {
            Log.e(LOG_TAG, e.message ?: e.toString())
        }
    }
}



































/**
 * Clase para guardar las credenciales encriptadas y los vectores de inicialización.

data class EncryptedCredentials(
val usernameIV: ByteArray,
val passwordIV: ByteArray,
val username: ByteArray,
val password: ByteArray
) {
override fun equals(other: Any?): Boolean {
if (this === other) return true
if (javaClass != other?.javaClass) return false

other as EncryptedCredentials

if (!usernameIV.contentEquals(other.usernameIV)) return false
if (!passwordIV.contentEquals(other.passwordIV)) return false
if (!username.contentEquals(other.username)) return false
if (!password.contentEquals(other.password)) return false

return true
}

override fun hashCode(): Int {
var result = usernameIV.contentHashCode()
result = 31 * result + passwordIV.contentHashCode()
result = 31 * result + username.contentHashCode()
result = 31 * result + password.contentHashCode()
return result
}
}
 */