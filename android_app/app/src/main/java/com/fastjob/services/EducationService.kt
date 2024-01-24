package com.fastjob.services

import com.fastjob.models.Education
import com.fastjob.models.EducationLevel
import retrofit2.Response
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.Path
import retrofit2.http.Query

interface EducationService {
    companion object {
        private const val ENDPOINT = "/educations/"
        private const val ENDPOINT_GET_QUALIFICATIONS = "${ENDPOINT}qualification/{qualifications_keyword}/"
        private const val ENDPOINT_LEVELS = "${ENDPOINT}education-levels/"
    }

    @GET(ENDPOINT)
    suspend fun getEducations(
        @Header("Authorization") auth: String,
        @Query("limit") limit: Int? = null,
        @Query("offset") offset: Int? = null
    ): Response<List<Education>>

    @GET(ENDPOINT_GET_QUALIFICATIONS)
    suspend fun getEducationsQualification(
        @Header("Authorization") auth: String? = null,
        @Path("qualifications_keyword") qualificationsKeyword: String,
        @Query("limit") limit: Int? = null,
        @Query("offset") offset: Int? = null
    ): Response<List<String>>

    @GET(ENDPOINT_LEVELS)
    suspend fun getEducationsLevel(
        @Header("Authorization") auth: String? = null,
        @Query("name_keyword") levelNameKeyword: String? = null,
        @Query("limit") limit: Int? = null,
        @Query("offset") offset: Int? = null
    ): Response<List<EducationLevel>>

}