package com.fastjob.ui.functions.keywords.management

import com.fastjob.auth.AuthAPI
import com.fastjob.models.Education
import com.fastjob.network.Client
import com.fastjob.services.EducationService

/**
 * Clase para seleccionar formaciones
 * Permite obtener los id de las formaciones a partir de su nombre
 * @property educationList lista de formaciones
 */
class EducationPicker {
    private var educationList: List<Education>? = null

    /**
     * Obtiene las formaciones a partir de una palabra clave
     * @param keyword palabra clave
     * @return lista de nombres de formaciones
     */
    suspend fun getEducations(keyword: String): List<String>? {
        // obtener la instancia de autenticación
        val auth = AuthAPI.getInstance()

        // si el usuario no está autenticado, devolver null
        if(!auth.isAuthenticated()) return null

        // limit y offset
        val limit = 10
        val offset = 0
        // obtener el servicio de education
        val educationService = Client.getInstance().getService(EducationService::class.java)

        // token de autenticación si el usuario está autenticado
        val token = auth.getToken()
        // lista de provincias a devolver
        var result: List<String>? = null


        // si la palabra está vacía, devolver null
        if (keyword.isEmpty())
            return null

        // obtener las formaciones
        val response = educationService.getEducations(auth = token!!, limit = limit, offset = offset, nameKeyword = keyword)


        // si la respuesta es exitosa, obtener la lista de formaciones
        if(response.isSuccessful) {
            educationList = response.body()
            result = educationList?.map { education -> education.qualification }
        }

        return result
    }


    /**
     * Obtiene el id de una formación a partir de su nombre
     * @param qualification nombre de la formación
     * @return id de la formación
     */
    fun getEducationId(qualification: String): String {
        // obtener el nivel de formación
        val education = educationList?.filter { it.qualification == qualification }

        // si la lista está vacía, devolver vacío
        if(education?.isEmpty() == true)
            return ""

        // devolver el id del nivel de formación
        return education?.map { it.id.toString() }?.first() ?: ""
    }

}
