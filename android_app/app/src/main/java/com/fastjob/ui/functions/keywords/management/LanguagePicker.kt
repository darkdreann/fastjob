package com.fastjob.ui.functions.keywords.management

import com.fastjob.auth.AuthAPI
import com.fastjob.models.Language
import com.fastjob.network.Client
import com.fastjob.services.LanguageService

/**
 * Clase para obtener los idiomas
 * @property languageList lista de idioma
 */
class LanguagePicker {
    private var languageList: List<Language>? = null

    /**
     * Obtiene los idiomas
     * @param keyword palabra clave para buscar los idiomas
     * @return lista de idiomas
     */
    suspend fun getLanguages(keyword: String): List<String>? {
        // obtener la instancia de autenticación
        val auth = AuthAPI.getInstance()

        if(!auth.isAuthenticated()) return null

        // limit y offset
        val limit = 10
        val offset = 0
        // obtener el servicio de language
        val languageService = Client.getInstance().getService(LanguageService::class.java)

        // token de autenticación si el usuario está autenticado
        val token = auth.getToken()
        // lista de niveles a devolver
        var result: List<String>? = null


        // si la palabra está vacía, devolver null
        if (keyword.isEmpty())
            return null

        // obtener los idiomas
        val response = languageService.getLanguages(auth = token!!, limit = limit, offset = offset, nameKeyword = keyword)


        // si la respuesta es exitosa, obtener la lista de idiomas
        if(response.isSuccessful) {
            languageList = response.body()
            result = languageList?.map { level -> level.name }
        }

        return result
    }

    /**
     * Obtiene el id del idioma
     * @param name nombre del  idioma
     * @return id del idioma
     */
    fun getLanguageId(name: String): String {
        // obtener el nivel de idioma
        val level = languageList?.filter { it.name == name }

        // si la lista está vacía, devolver vacío
        if(level?.isEmpty() == true)
            return ""

        // devolver el id del nivel de idioma
        return level?.map { it.id.toString() }?.first() ?: ""
    }

}
