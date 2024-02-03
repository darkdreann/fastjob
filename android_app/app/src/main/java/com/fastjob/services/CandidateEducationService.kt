package com.fastjob.services

import com.fastjob.models.CandidateEducationIN
import com.fastjob.models.CandidateEducationOUT
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.DELETE
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.POST
import retrofit2.http.PUT
import retrofit2.http.Path
import retrofit2.http.Query
import java.time.LocalDate
import java.util.UUID

interface CandidateEducationService {
    companion object {
        private const val ENDPOINT = "/candidates/educations/{candidate_id}/"
        private const val EDUCATION_BY_ID_ENDPOINT = "${ENDPOINT}{id}/"
    }

    @GET(ENDPOINT)
    suspend fun getCandidateEducations(
        @Header("Authorization") auth: String,
        @Path("candidate_id") candidateId: UUID,
        @Query("limit") limit: Int? = null,
        @Query("offset") offset: Int? = null
    ): Response<List<CandidateEducationIN>>

    @GET(EDUCATION_BY_ID_ENDPOINT)
    suspend fun getCandidateEducation(
        @Header("Authorization") auth: String,
        @Path("candidate_id") candidateId: UUID,
        @Path("id") id: UUID
    ): Response<CandidateEducationIN>

    @POST(ENDPOINT)
    suspend fun createCandidateEducations(
        @Header("Authorization") auth: String,
        @Path("candidate_id") candidateId: UUID,
        @Body candidateEducation: CandidateEducationOUT
    ): Response<CandidateEducationIN>


    @PUT(EDUCATION_BY_ID_ENDPOINT)
    suspend fun updateCandidateEducations(
        @Header("Authorization") auth: String,
        @Path("candidate_id") candidateId: UUID,
        @Path("id") id: UUID,
        @Body candidateEducationCompletionDate: LocalDate
    ): Response<CandidateEducationIN>

    @DELETE(EDUCATION_BY_ID_ENDPOINT)
    suspend fun deleteCandidateEducations(
        @Header("Authorization") auth: String,
        @Path("candidate_id") candidateId: UUID,
        @Path("id") id: UUID
    ): Response<Unit>
}