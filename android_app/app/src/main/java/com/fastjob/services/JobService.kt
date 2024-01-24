package com.fastjob.services

import com.fastjob.models.JobIN
import com.fastjob.models.JobOUT
import com.fastjob.models.LanguageWithLevelIN
import com.fastjob.models.LanguageWithLevelOUT
import com.fastjob.models.MinimalJobIN
import com.fastjob.models.PartialUpdateJobOUT
import com.fastjob.models.UpdateJobOUT
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

interface JobService {
    companion object {
        private const val ENDPOINT = "/jobs/"
        private const val JOB_BY_ID = "${ENDPOINT}{id}/"
        private const val GET_JOBS_MINIMAL = "${ENDPOINT}?minimal_fields=true"
        private const val JOB_LANGUAGES = "${JOB_BY_ID}languages/{language_id}/"
        private const val JOB_EDUCATION_REMOVE = "${JOB_BY_ID}education/"
        private const val GET_KEYWORDS = "${ENDPOINT}keywords/{keyword}/"
    }

    @GET(ENDPOINT)
    suspend fun getJobs(
        @Header("Authorization") auth: String? = null,
        @Query("limit") limit: Int? = null,
        @Query("offset") offset: Int? = null,
        @Query("active") active: Boolean? = null,
        @Query("sector_category") sectorCategory: String? = null,
        @Query("sector_id") sectorId: UUID? = null,
        @Query("province") province: String? = null,
        @Query("keyword") keyword: String? = null,
        @Query("education_name") educationName: String? = null,
        @Query("education_level_value") educationLevel: Int? = null,
        @Query("languages") languages: Set<String>? = null
    ): Response<List<JobIN>>

    @GET(GET_JOBS_MINIMAL)
    suspend fun getJobsMinimal(
        @Header("Authorization") auth: String? = null,
        @Query("limit") limit: Int? = null,
        @Query("offset") offset: Int? = null,
        @Query("active") active: Boolean? = null,
        @Query("sector_category") sectorCategory: String? = null,
        @Query("sector_id") sectorId: UUID? = null,
        @Query("province") province: String? = null,
        @Query("keyword") keyword: String? = null,
        @Query("education_name") educationName: String? = null,
        @Query("education_level_value") educationLevel: Int? = null,
        @Query("languages") languages: Set<String>? = null
    ): Response<List<MinimalJobIN>>

    @GET(JOB_BY_ID)
    suspend fun getJob(
        @Header("Authorization") auth: String? = null,
        @Path("id") id: UUID
    ): Response<JobIN>

    @GET(GET_KEYWORDS)
    suspend fun getKeywords(
        @Header("Authorization") auth: String? = null,
        @Path("keyword") keyword: String,
        @Query("limit") limit: Int? = null,
        @Query("offset") offset: Int? = null
    ): Response<List<String>>

    @POST(ENDPOINT)
    suspend fun createJob(
        @Header("Authorization") auth: String,
        @Body job: JobOUT
    ): Response<JobIN>

    @PUT(JOB_BY_ID)
    suspend fun updateJob(
        @Header("Authorization") auth: String,
        @Path("id") id: UUID,
        @Body job: UpdateJobOUT
    ): Response<JobIN>

    @PATCH(JOB_BY_ID)
    suspend fun partialUpdateJob(
        @Header("Authorization") auth: String,
        @Path("id") id: UUID,
        @Body job: PartialUpdateJobOUT
    ): Response<JobIN>

    @DELETE(JOB_BY_ID)
    suspend fun deleteJob(
        @Header("Authorization") auth: String,
        @Path("id") id: UUID
    ): Response<Unit>

    @POST(JOB_BY_ID)
    suspend fun addJobLanguage(
        @Header("Authorization") auth: String,
        @Path("id") id: UUID,
        @Body language: LanguageWithLevelOUT
    ): Response<LanguageWithLevelIN>

    @POST(JOB_LANGUAGES)
    suspend fun updateJobLanguage(
        @Header("Authorization") auth: String,
        @Path("id") id: UUID,
        @Path("language_id") languageId: UUID,
        @Body languageLevelId: UUID
    ): Response<LanguageWithLevelIN>

    @DELETE(JOB_LANGUAGES)
    suspend fun deleteJobLanguage(
        @Header("Authorization") auth: String,
        @Path("id") id: UUID,
        @Path("language_id") languageId: UUID
    ): Response<Unit>

    @DELETE(JOB_EDUCATION_REMOVE)
    suspend fun deleteJobEducation(
        @Header("Authorization") auth: String,
        @Path("id") id: UUID
    ): Response<Unit>

}