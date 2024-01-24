package com.fastjob.services

import com.fastjob.models.Sector
import com.fastjob.models.SectorSubcategory
import retrofit2.Response
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.Path
import retrofit2.http.Query

interface SectorService {
    companion object {
        private const val ENDPOINT = "/sectors/"
        private const val ENDPOINT_CATEGORIES = "${ENDPOINT}categories/{category_keyword}/"
        private const val ENDPOINT_SUBCATEGORIES = "${ENDPOINT}{category}/subcategories/{subcategory_keyword}/"
    }

    @GET(ENDPOINT)
    suspend fun getSectors(
        @Header("Authorization") auth: String,
        @Query("limit") limit: Int? = null,
        @Query("offset") offset: Int? = null
    ): Response<List<Sector>>

    @GET(ENDPOINT_CATEGORIES)
    suspend fun getSectorsCategories(
        @Header("Authorization") auth: String? = null,
        @Path("category_keyword") categoryKeyword: String,
        @Query("limit") limit: Int? = null,
        @Query("offset") offset: Int? = null
    ): Response<List<String>>

    @GET(ENDPOINT_SUBCATEGORIES)
    suspend fun getSectorsSubcategories(
        @Header("Authorization") auth: String? = null,
        @Path("category") category: String,
        @Path("subcategory_keyword") subcategoryKeyword: String,
        @Query("limit") limit: Int? = null,
        @Query("offset") offset: Int? = null
    ): Response<List<SectorSubcategory>>
}