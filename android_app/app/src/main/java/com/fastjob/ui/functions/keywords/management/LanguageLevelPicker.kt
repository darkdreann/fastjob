package com.fastjob.ui.functions.keywords.management

import android.util.Log
import com.fastjob.auth.AuthAPI
import com.fastjob.models.LanguageLevel
import com.fastjob.network.Client
import com.fastjob.services.LanguageService

/**
 * Clase para obtener los niveles de idioma
 * @property levelList lista de niveles de idioma
 */
class LanguageLevelPicker {
    private var levelList: List<LanguageLevel>? = null

    /**
     * Obtiene los niveles de idioma
     * @param keyword palabra clave para buscar los niveles
     * @return lista de niveles de idioma
     */
    suspend fun getLanguageLevels(keyword: String): List<String>? {
        // obtener la instancia de autenticación
        val auth = AuthAPI.getInstance()

        if(!auth.isAuthenticated()) return null

        // limit y offset
        val limit = 10
        val offset = 0
        // obtener el servicio de langguage level
        val languageService = Client.getInstance().getService(LanguageService::class.java)

        // token de autenticación si el usuario está autenticado
        val token = auth.getToken()
        // lista de niveles a devolver
        var result: List<String>? = null


        // si la palabra está vacía, devolver null
        if (keyword.isEmpty())
            return null


        // obtener los niveles
        val response = languageService.getLanguagesLevel(auth = token!!, limit = limit, offset = offset, levelNameKeyword = keyword)


        // si la respuesta es exitosa, obtener la lista de niveles de idioma
        if(response.isSuccessful) {
            levelList = response.body()
            result = levelList?.map { level -> level.name }
        }

        return result
    }

    /**
     * Obtiene el id del nivel de idioma
     * @param name nombre del nivel de idioma
     * @return id del nivel de idioma
     */
    fun getLevelId(name: String): String {
        // obtener el nivel de idioma
        val level = levelList?.filter { it.name == name }

        // si la lista está vacía, devolver vacío
        if(level?.isEmpty() == true)
            return ""

        // devolver el id del nivel de idioma
        return level?.map { it.id.toString() }?.first() ?: ""
    }

}
