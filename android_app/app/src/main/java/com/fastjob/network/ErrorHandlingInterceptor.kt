package com.fastjob.network

import android.util.Log
import okhttp3.Interceptor
import okhttp3.Protocol
import okhttp3.Response
import java.io.IOException

/**
 * Interceptor para interceptar errores de red
 * @see okhttp3.Interceptor
 */
class GlobalErrorInterceptor : Interceptor {
    /**
     * Intercepta la peticion y devuelve una respuesta de error en caso de que no se pueda conectar
     */
    override fun intercept(chain: Interceptor.Chain): Response {
        val request = chain.request()
        return try {
            chain.proceed(request)
        } catch (ex: IOException) {
            Log.e("GlobalErrorInterceptor", "Error: ${ex.message}")
            // respuesta de error
            Response.Builder()
                .request(chain.request())
                .protocol(Protocol.HTTP_1_1)
                .message("Can't connect!")
                .body(
                    okhttp3.ResponseBody.create(
                        okhttp3.MediaType.parse("application/json"),
                        "{}"
                    )
                )
                .code(500)
                .build()
        }
    }
}
