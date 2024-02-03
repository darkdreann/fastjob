package com.fastjob.ui.functions.keywords.management

import android.util.Log
import com.fastjob.auth.AuthAPI
import com.fastjob.network.Client
import com.fastjob.services.EducationService

/**
 * Obtiene una lista de nombres de formaciones que coincidan con la palabra clave
 * @param keyword palabra clave
 */
suspend fun getEducationNameKeyword(keyword: String): List<String>?{
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
    val response = educationService.getEducationsQualification(auth = token, limit = limit, offset = offset, qualificationsKeyword = keyword)

    // si la respuesta es exitosa, obtener la lista de provincias
    if(response.isSuccessful)
        result = response.body()

    return result
}