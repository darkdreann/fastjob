package com.fastjob.models

import com.google.gson.annotations.SerializedName
import java.time.LocalDate
import java.util.UUID

data class CandidateEducationIN(
    @SerializedName("completion_date")
    val completionDate: LocalDate,
    val education: Education
)

data class CandidateEducationOUT(
    @SerializedName("completion_date")
    val completionDate: LocalDate,
    @SerializedName("education_id")
    val education: UUID
)