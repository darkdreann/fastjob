package com.fastjob.services

import com.fastjob.models.CandidateEducationIN
import com.fastjob.models.CandidateIN
import com.fastjob.models.CandidateExtraFields
import com.fastjob.models.ExperienceIN
import com.fastjob.models.LanguageWithLevelIN
import com.fastjob.models.MinimalCandidateIN
import okhttp3.ResponseBody
import retrofit2.Response
import retrofit2.http.DELETE
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.POST
import retrofit2.http.Path
import retrofit2.http.Query
import java.util.UUID

interface JobCandidateService {

    companion object {
        private const val ENDPOINT = "/jobs/candidates/{job_id}/"
        private const val GET_MINIMAL_CANDIDATES = "${ENDPOINT}?minimal_fields=true"
        private const val CANDIDATE_BY_ID = "${ENDPOINT}{candidate_id}/"
        private const val CANDIDATE_BY_ID_EXPERIENCES = "${CANDIDATE_BY_ID}experiences/"
        private const val CANDIDATE_BY_ID_EDUCATIONS = "${CANDIDATE_BY_ID}educations/"
        private const val CANDIDATE_BY_ID_LANGUAGES = "${CANDIDATE_BY_ID}languages/"
        private const val CANDIDATE_CV_BY_ID = "${CANDIDATE_BY_ID}curriculum/"
        private const val IS_APPLIED = "${ENDPOINT}is-applied/{candidate_id}/"
        private const val APPLY_JOB = "${ENDPOINT}apply/{candidate_id}/"
        private const val REMOVE_JOB = "${ENDPOINT}remove/{candidate_id}/"
    }

    @GET(GET_MINIMAL_CANDIDATES)
    suspend fun getJobCandidatesMinimal(
        @Header("Authorization") auth: String,
        @Path("job_id") jobId: UUID,
        @Query("limit") limit: Int? = null,
        @Query("offset") offset: Int? = null,
        @Query("postal_code") postalCode: Int? = null,
        @Query("province") province: String? = null,
        @Query("experience_months") experienceMonths: Int? = null,
        @Query("experience_sector") experienceSector: String? = null,
        @Query("language") language: String? = null,
        @Query("language_level") languageLevel: Int? = null,
        @Query("education_name") educationName: String? = null,
        @Query("education_level") educationLevel: Int? = null,
        @Query("education_sector") educationSector: String? = null,
        @Query("skills") skills: Set<String>? = null,
        @Query("availability") availability: String? = null
    ): Response<List<MinimalCandidateIN>>

    @GET(ENDPOINT)
    @JvmSuppressWildcards
    suspend fun getJobCandidates(
        @Header("Authorization") auth: String,
        @Path("job_id") jobId: UUID,
        @Query("limit") limit: Int? = null,
        @Query("offset") offset: Int? = null,
        @Query("extra_fields") extraFields: Set<CandidateExtraFields>? = null,
        @Query("postal_code") postalCode: Int? = null,
        @Query("province") province: String? = null,
        @Query("experience_months") experienceMonths: Int? = null,
        @Query("experience_sector") experienceSector: String? = null,
        @Query("language") language: String? = null,
        @Query("language_level") languageLevel: Int? = null,
        @Query("education_name") educationName: String? = null,
        @Query("education_level") educationLevel: Int? = null,
        @Query("education_sector") educationSector: String? = null,
        @Query("skills") skills: Set<String>? = null,
        @Query("availability") availability: String? = null
    ): Response<List<CandidateIN>>

    @GET(CANDIDATE_BY_ID)
    @JvmSuppressWildcards
    suspend fun getJobCandidate(
        @Header("Authorization") auth: String,
        @Path("job_id") jobId: UUID,
        @Path("candidate_id") candidateId: UUID,
        @Query("extra_fields") extraFields: Set<CandidateExtraFields>? = null
    ): Response<CandidateIN>

    @GET(CANDIDATE_CV_BY_ID)
    suspend fun getJobCandidateCurriculum(
        @Header("Authorization") auth: String,
        @Path("job_id") jobId: UUID,
        @Path("candidate_id") candidateId: UUID
    ): Response<ResponseBody>

    @GET(CANDIDATE_BY_ID_EXPERIENCES)
    suspend fun getJobCandidateExperiences(
        @Header("Authorization") auth: String,
        @Path("job_id") jobId: UUID,
        @Path("candidate_id") candidateId: UUID,
        @Query("limit") limit: Int? = null,
        @Query("offset") offset: Int? = null,
    ): Response<List<ExperienceIN>>

    @GET(CANDIDATE_BY_ID_EDUCATIONS)
    suspend fun getJobCandidateEducations(
        @Header("Authorization") auth: String,
        @Path("job_id") jobId: UUID,
        @Path("candidate_id") candidateId: UUID,
        @Query("limit") limit: Int? = null,
        @Query("offset") offset: Int? = null,
    ): Response<List<CandidateEducationIN>>

    @GET(CANDIDATE_BY_ID_LANGUAGES)
    suspend fun getJobCandidateLanguages(
        @Header("Authorization") auth: String,
        @Path("job_id") jobId: UUID,
        @Path("candidate_id") candidateId: UUID,
        @Query("limit") limit: Int? = null,
        @Query("offset") offset: Int? = null,
    ): Response<List<LanguageWithLevelIN>>

    @GET(IS_APPLIED)
    suspend fun isAppliedJob(
        @Header("Authorization") auth: String,
        @Path("job_id") jobId: UUID,
        @Path("candidate_id") candidateId: UUID
    ): Response<Boolean>

    @POST(APPLY_JOB)
    suspend fun applyJob(
        @Header("Authorization") auth: String,
        @Path("job_id") jobId: UUID,
        @Path("candidate_id") candidateId: UUID
    ): Response<ResponseBody>

    @DELETE(REMOVE_JOB)
    suspend fun removeJob(
        @Header("Authorization") auth: String,
        @Path("job_id") jobId: UUID,
        @Path("candidate_id") candidateId: UUID
    ): Response<ResponseBody>

}