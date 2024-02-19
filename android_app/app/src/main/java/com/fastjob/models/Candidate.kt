package com.fastjob.models

import com.google.gson.annotations.SerializedName
import java.util.UUID

enum class CandidateExtraFields(val value: String) {
    EXPERIENCES("experiences"),
    EDUCATION("education"),
    LANGUAGES("language"),
    APPLIED_JOBS("applied_jobs")
}

data class MinimalCandidateIN(
    val id: UUID,
    val name: String,
    val surname: String,
    val skills: List<String>? = null,
    @SerializedName("availability")
    val availabilities: List<Availability>? = null,
    val province: String
)

data class CandidateIN(
    val skills: List<String>? = null,
    @SerializedName("availability")
    val availabilities: List<Availability>? = null,
    val user: UserIN,
    @SerializedName("experience_list")
    val experiences: List<ExperienceIN>? = null,
    @SerializedName("education_list")
    val education: List<CandidateEducationIN>? = null,
    @SerializedName("language_list")
    val languages: List<LanguageWithLevelIN>? = null,
    @SerializedName("applied_jobs_list")
    val appliedJobs: List<JobIN>? = null
)

data class CandidateOUT(
    val skills: List<String>,
    @SerializedName("availability")
    val availabilities: List<Availability>,
    val user: UserOUT
)

data class PartialCandidateOUT(
    val skills: List<String>? = null,
    @SerializedName("availability")
    val availabilities: List<Availability>? = null,
    val user: PartialUserOUT? = null
)





