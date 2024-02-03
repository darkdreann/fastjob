package com.fastjob.services

import com.fastjob.models.Language
import com.fastjob.models.LanguageLevel
import retrofit2.Response
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.Path
import retrofit2.http.Query

interface LanguageService {
    companion object {
        private const val ENDPOINT = "/languages/"
        private const val LANGUAGE_LEVEL_ENDPOINT = "${ENDPOINT}language-levels/"
        private const val LANGUAGE_NAME_ENDPOINT = "${ENDPOINT}language-name/{name_keyword}/"
    }

    @GET(ENDPOINT)
    suspend fun getLanguages(
        @Header("Authorization") auth: String,
        @Query("limit") limit: Int? = null,
        @Query("offset") offset: Int? = null,
        @Query("name_keyword") nameKeyword: String? = null,
    ): Response<List<Language>>

    @GET(LANGUAGE_LEVEL_ENDPOINT)
    suspend fun getLanguagesLevel(
        @Header("Authorization") auth: String,
        @Query("language_level_keyword") levelNameKeyword: String? = null,
        @Query("limit") limit: Int? = null,
        @Query("offset") offset: Int? = null
    ): Response<List<LanguageLevel>>

    @GET(LANGUAGE_NAME_ENDPOINT)
    suspend fun getLanguagesName(
        @Header("Authorization") auth: String? = null,
        @Path("name_keyword") nameKeyword: String,
        @Query("limit") limit: Int? = null,
        @Query("offset") offset: Int? = null
    ): Response<List<String>>
}