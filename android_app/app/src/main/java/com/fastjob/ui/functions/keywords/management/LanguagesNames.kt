package com.fastjob.ui.functions.keywords.management

import com.fastjob.auth.AuthAPI
import com.fastjob.network.Client
import com.fastjob.services.LanguageService

/**
 * Obtiene una lista de nombres de lenguajes que coincidan con la palabra clave
 * @param keyword palabra clave
 */
suspend fun getLanguages(keyword: String): List<String>? {
    // limit y offset
    val limit = 10
    val offset = 0
    // obtener el servicio de address
    val languageService = Client.getInstance().getService(LanguageService::class.java)
    val auth = AuthAPI.getInstance()
    // token de autenticación si el usuario está autenticado
    val token = auth.getToken()
    // lista de provincias a devolver
    var result: List<String>? = null

    // si la palabra está vacía, devolver null
    if (keyword.isEmpty())
        return null

    // obtener las provincias
    val response = languageService.getLanguagesName(auth = token, limit = limit, offset = offset, nameKeyword = keyword)

    // si la respuesta es exitosa, obtener la lista de provincias
    if(response.isSuccessful)
        result = response.body()

    return result
}