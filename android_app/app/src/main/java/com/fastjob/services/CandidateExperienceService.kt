package com.fastjob.services

import com.fastjob.models.ExperienceIN
import com.fastjob.models.ExperienceOUT
import com.fastjob.models.PartialExperienceOUT
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.DELETE
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.PATCH
import retrofit2.http.POST
import retrofit2.http.PUT
import retrofit2.http.Path
import retrofit2.http.Query
import java.util.UUID

interface CandidateExperienceService {
    companion object {
        private const val ENDPOINT = "/candidates/experiences/{candidate_id}/"
        private const val EXP_BY_ID_ENDPOINT = "${ENDPOINT}{id}/"
    }

    @GET(ENDPOINT)
    suspend fun getExperiences(
        @Header("Authorization") auth: String,
        @Path("candidate_id") candidateId: UUID,
        @Query("limit") limit: Int? = null,
        @Query("offset") offset: Int? = null
    ): Response<List<ExperienceIN>>

    @GET(EXP_BY_ID_ENDPOINT)
    suspend fun getExperience(
        @Header("Authorization") auth: String,
        @Path("candidate_id") candidateId: UUID,
        @Path("id") id: UUID
    ): Response<ExperienceIN>

    @POST(ENDPOINT)
    suspend fun createExperience(
        @Header("Authorization") auth: String,
        @Path("candidate_id") candidateId: UUID,
        @Body experience: ExperienceOUT
    ): Response<ExperienceIN>

    @PUT(EXP_BY_ID_ENDPOINT)
    suspend fun updateExperience(
        @Header("Authorization") auth: String,
        @Path("candidate_id") candidateId: UUID,
        @Path("id") id: UUID,
        @Body experience: ExperienceOUT
    ): Response<ExperienceIN>

    @PATCH(EXP_BY_ID_ENDPOINT)
    suspend fun partialUpdateExperience(
        @Header("Authorization") auth: String,
        @Path("candidate_id") candidateId: UUID,
        @Path("id") id: UUID,
        @Body experience: PartialExperienceOUT
    ): Response<ExperienceIN>

    @DELETE(EXP_BY_ID_ENDPOINT)
    suspend fun deleteExperience(
        @Header("Authorization") auth: String,
        @Path("candidate_id") candidateId: UUID,
        @Path("id") id: UUID
    ): Response<Unit>

}