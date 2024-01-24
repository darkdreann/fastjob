package com.fastjob.services

import okhttp3.MultipartBody
import okhttp3.ResponseBody
import retrofit2.Response
import retrofit2.http.DELETE
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.Multipart
import retrofit2.http.POST
import retrofit2.http.Part
import retrofit2.http.Path
import java.util.UUID

interface CandidateCurriculumService {
    companion object {
        private const val ENDPOINT = "/candidates/{candidate_id}/curriculum/"
    }

    @GET(ENDPOINT)
    suspend fun getCandidateCurriculum(
        @Header("Authorization") auth: String,
        @Path("candidate_id") candidateId: UUID
    ): Response<ResponseBody>

    @Multipart
    @POST(ENDPOINT)
    suspend fun setCandidateCurriculum(
        @Header("Authorization") auth: String,
        @Path("candidate_id") candidateId: UUID,
        @Part("curriculum") cvFile: MultipartBody.Part
    ): Response<Unit>

    @DELETE(ENDPOINT)
    suspend fun deleteCandidateCurriculum(
        @Header("Authorization") auth: String,
        @Path("candidate_id") candidateId: UUID
    ): Response<Unit>
}