package com.fastjob.ui.functions.keywords.management

import android.util.Log
import com.fastjob.auth.AuthAPI
import com.fastjob.models.SectorSubcategory
import com.fastjob.network.Client
import com.fastjob.services.SectorService

/**
 * Clase que se encarga de obtener las subcategorías de un sector
 * Guarda la lista de subcategorías y devuelve una lista de nombres de subcategorías
 * Permite obtener el id de una subcategoría a partir de su nombre
 * @property subCategoryList lista de subcategorías
 * @property category categoría de la que se quieren obtener las subcategorías
 */
class SubcategoryPicker {
    private var subCategoryList: List<SectorSubcategory>? = null
    private var category: String = ""

    /**
     * Obtiene las subcategorías de un sector
     * @param keyword palabra clave para filtrar las subcategorías
     * @return lista de nombres de subcategorías
     */
    suspend fun getSubcategories(keyword: String): List<String>? {
        // limit y offset
        val limit = 10
        val offset = 0
        // obtener el servicio de address
        val sectorService = Client.getInstance().getService(SectorService::class.java)
        val auth = AuthAPI.getInstance()
        // token de autenticación si el usuario está autenticado
        val token = auth.getToken()
        // lista de provincias a devolver
        var result: List<String>? = null

        // si la palabra está vacía, devolver null
        if (keyword.isEmpty() || category.isEmpty())
            return null

        // obtener las provincias
        val response = sectorService.getSectorsSubcategories(auth = token, limit = limit, offset = offset, subcategoryKeyword = keyword, category = category)

        // si la respuesta es exitosa, obtener la lista de provincias
        if(response.isSuccessful) {
            subCategoryList = response.body()
            result = subCategoryList?.map { cat -> cat.subcategory }
        }

        return result
    }

    /**
     * Establece la categoría de la que se quieren obtener las subcategorías
     * @param category categoría
     */
    fun setCategory(category: String) {
        this.category = category
    }

    /**
     * Obtiene el id de una subcategoría a partir de su nombre
     * @param name nombre de la subcategoría
     * @return id de la subcategoría
     */
    fun getSectorId(name: String): String {
        val sector = subCategoryList?.filter { it.subcategory == name }

        if(sector?.isEmpty() == true)
            return ""

        return sector?.map { it.id.toString() }?.first() ?: ""
    }

}