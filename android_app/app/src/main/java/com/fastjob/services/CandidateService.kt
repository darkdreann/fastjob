package com.fastjob.services

import com.fastjob.models.CandidateIN
import com.fastjob.models.CandidateOUT
import com.fastjob.models.CandidateExtraFields
import com.fastjob.models.PartialCandidateOUT
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

interface CandidateService {
    companion object {
        private const val ENDPOINT = "/candidates/"
        private const val CANDIDATE_BY_ID_ENDPOINT = "${ENDPOINT}{id}"
    }

    @GET(CANDIDATE_BY_ID_ENDPOINT)
    suspend fun getCandidate(
        @Header("Authorization") auth: String,
        @Path("id") id: UUID,
        @Query("extra_fields") extraFields: Set<CandidateExtraFields>? = null
    ): Response<CandidateIN>

    @POST(ENDPOINT)
    suspend fun createCandidate(
        @Body candidate: CandidateOUT
    ): Response<CandidateIN>

    @PUT(CANDIDATE_BY_ID_ENDPOINT)
    suspend fun updateCandidate(
        @Header("Authorization") auth: String,
        @Path("id") id: UUID,
        @Body candidate: CandidateOUT
    ): Response<CandidateIN>

    @PATCH(CANDIDATE_BY_ID_ENDPOINT)
    suspend fun partialUpdateCandidate(
        @Header("Authorization") auth: String,
        @Path("id") id: UUID,
        @Body candidate: PartialCandidateOUT
    ): Response<CandidateIN>

    @DELETE(CANDIDATE_BY_ID_ENDPOINT)
    suspend fun deleteCandidate(
        @Header("Authorization") auth: String,
        @Path("id") id: UUID
    ): Response<Unit>

}