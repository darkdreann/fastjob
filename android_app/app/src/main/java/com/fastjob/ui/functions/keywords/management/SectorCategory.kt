package com.fastjob.ui.functions.keywords.management

import com.fastjob.auth.AuthAPI
import com.fastjob.network.Client
import com.fastjob.services.SectorService

/**
 * Obtiene las categorias de sectores que coincidan con la palabra clave
 * @param keyword palabra clave
 */
suspend fun getSectorCategoryKeyword(keyword: String): List<String>? {
    // limit y offset
    val limit = 10
    val offset = 0
    // obtener el servicio de sector
    val sectorService = Client.getInstance().getService(SectorService::class.java)
    val auth = AuthAPI.getInstance()
    // token de autenticación si el usuario está autenticado
    val token = auth.getToken()
    // lista de categorias a devolver
    var result: List<String>? = null

    // si la palabra está vacía, devolver null
    if (keyword.isEmpty())
        return null

    // obtener las categorias
    val response = sectorService.getSectorsCategories(auth = token,limit = limit, offset = offset, categoryKeyword = keyword)

    // si la respuesta es exitosa, obtener la lista de categorias
    if(response.isSuccessful)
        result = response.body()

    return result
}