package com.fastjob.ui.functions.keywords.management

import com.fastjob.auth.AuthAPI
import com.fastjob.models.EducationLevel
import com.fastjob.network.Client
import com.fastjob.services.EducationService

/**
 * Clase que se encarga de obtener los niveles de formación
 * Almacena la lista de niveles de formación y devuelve una lista de nombres
 * Se puede obtener el valor de un nivel de formación a partir de su nombre
 * @property levelList lista de provincias
 */
class EducationLevelPicker {
    private var levelList: List<EducationLevel>? = null

    /**
     * Obtiene los niveles de formación a partir de una palabra clave
     * @param keyword palabra clave para buscar los niveles de formación
     * @return lista de nombres de niveles de formación
     */
    suspend fun getEducationLevels(keyword: String): List<String>? {
        // limit y offset
        val limit = 10
        val offset = 0
        // obtener el servicio de address
        val educationService = Client.getInstance().getService(EducationService::class.java)
        val auth = AuthAPI.getInstance()
        // token de autenticación si el usuario está autenticado
        val token = auth.getToken()
        // lista de provincias a devolver
        var result: List<String>? = null


        // si la palabra está vacía, devolver null
        if (keyword.isEmpty())
            return null

        // obtener las provincias
        val response = educationService.getEducationsLevel(auth = token, limit = limit, offset = offset, levelNameKeyword = keyword)


        // si la respuesta es exitosa, obtener la lista de provincias
        if(response.isSuccessful) {
            levelList = response.body()
            result = levelList?.map { level -> level.name }
        }

        return result
    }

    /**
     * Obtiene el valor de un nivel de formación a partir de su nombre
     * @param name nombre del nivel de formación
     * @return valor del nivel de formación
     */
    fun getLevelValue(name: String): String {
        // obtener el nivel de formación
        val level = levelList?.filter { it.name == name }

        // si la lista está vacía, devolver vacío
        if(level?.isEmpty() == true)
            return ""

        // devolver el id del nivel de formación
        return level?.map { it.value.toString() }?.first() ?: ""
    }

}
