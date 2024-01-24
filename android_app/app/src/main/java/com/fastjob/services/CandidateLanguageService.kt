package com.fastjob.services

import com.fastjob.models.LanguageWithLevelIN
import com.fastjob.models.LanguageWithLevelOUT
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.DELETE
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.POST
import retrofit2.http.Path
import retrofit2.http.Query
import java.util.UUID

interface CandidateLanguageService {
    companion object {
        private const val ENDPOINT = "/candidates/languages/{candidate_id}"
        private const val LANG_BY_ID_ENDPOINT = "${ENDPOINT}{id}"
    }

    @GET(ENDPOINT)
    suspend fun getCandidateLanguages(
        @Header("Authorization") auth: String,
        @Path("candidate_id") candidateId: UUID,
        @Query("limit") limit: Int? = null,
        @Query("offset") offset: Int? = null
    ): Response<List<LanguageWithLevelIN>>

    @GET(LANG_BY_ID_ENDPOINT)
    suspend fun getCandidateLanguage(
        @Header("Authorization") auth: String,
        @Path("candidate_id") candidateId: UUID,
        @Path("id") id: UUID
    ): Response<LanguageWithLevelIN>

    @POST(ENDPOINT)
    suspend fun createCandidateLanguages(
        @Header("Authorization") auth: String,
        @Path("candidate_id") candidateId: UUID,
        @Body language: LanguageWithLevelOUT,
    ): Response<LanguageWithLevelIN>

    @POST(LANG_BY_ID_ENDPOINT)
    suspend fun updateCandidateLanguages(
        @Header("Authorization") auth: String,
        @Path("candidate_id") candidateId: UUID,
        @Path("id") id: UUID,
        @Body languageId: UUID,
    ): Response<LanguageWithLevelIN>

    @DELETE(LANG_BY_ID_ENDPOINT)
    suspend fun deleteCandidateLanguages(
        @Header("Authorization") auth: String,
        @Path("candidate_id") candidateId: UUID,
        @Path("id") id: UUID
    ): Response<Unit>

}