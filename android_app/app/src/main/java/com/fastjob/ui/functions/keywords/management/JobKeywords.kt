package com.fastjob.ui.functions.keywords.management

import com.fastjob.auth.AuthAPI
import com.fastjob.network.Client
import com.fastjob.services.JobService

/**
 * Función que devuelve una lista de palabras clave
 * @param String palabra a buscar
 * @return List<String> lista de palabras clave o null si no se encuentra ninguna
 */
suspend fun getJobKeywords(keyword: String): List<String>? {
    // limit y offset
    val limit = 10
    val offset = 0
    // obtener el servicio de trabajo
    val jobService = Client.getInstance().getService(JobService::class.java)
    val auth = AuthAPI.getInstance()
    // obtener la palabra a buscar
    val word = keyword.split("\\s+".toRegex()).last()
    // token de autenticación si el usuario está autenticado
    val token = auth.getToken()
    // lista de palabras a devolver
    var result: List<String>? = null

    // si la palabra está vacía, devolver null
    if (word.isEmpty())
        return null

    // obtener las palabras
    val response = jobService.getKeywords(auth = token, keyword = word, limit = limit, offset = offset)

    // si la respuesta es exitosa, obtener la lista de palabras
    if(response.isSuccessful)
        result = response.body()

    return result
}

/**
 * Función que añade una palabra clave a una cadena de texto.
 * La palabra clave se añade al final de la cadena de texto reemplazando la última palabra.
 * @param String cadena de texto
 * @param String palabra clave
 * @return String cadena de texto con la palabra clave añadida
 */
fun appendToKeyword(currentString: String, keyword: String): String {
    val stringBuilder = StringBuilder()
    // añadir las palabras a la cadena de texto
    currentString.split("\\s+".toRegex()).apply {
        this.subList(0, this.size - 1).forEach {
            stringBuilder.append("$it ")
        }
    }
    // añadir la palabra clave y devolver la cadena de texto
    stringBuilder.append(keyword)
    return stringBuilder.toString()
}
