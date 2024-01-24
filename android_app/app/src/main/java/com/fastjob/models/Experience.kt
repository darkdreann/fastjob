package com.fastjob.models

import com.google.gson.annotations.SerializedName
import java.time.LocalDate
import java.util.UUID

data class ExperienceIN(
    val id: UUID,
    @SerializedName("company_name")
    val companyName: String,
    @SerializedName("job_position")
    val jobPosition: String,
    @SerializedName("job_position_description")
    val jobPositionDescription: String,
    @SerializedName("start_date")
    val startDate: LocalDate,
    @SerializedName("end_date")
    val endDate: LocalDate?,
    val sector: Sector
)

data class ExperienceOUT(
    @SerializedName("company_name")
    val companyName: String,
    @SerializedName("job_position")
    val jobPosition: String,
    @SerializedName("job_position_description")
    val jobPositionDescription: String,
    @SerializedName("start_date")
    val startDate: LocalDate,
    @SerializedName("end_date")
    val endDate: LocalDate?,
    @SerializedName("sector_id")
    val sectorId: UUID
)

data class PartialExperienceOUT(
    @SerializedName("company_name")
    val companyName: String?,
    @SerializedName("job_position")
    val jobPosition: String?,
    @SerializedName("job_position_description")
    val jobPositionDescription: String?,
    @SerializedName("start_date")
    val startDate: LocalDate?,
    @SerializedName("end_date")
    val endDate: LocalDate?,
    @SerializedName("sector_id")
    val sectorId: UUID?
)