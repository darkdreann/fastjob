package com.fastjob.models

import com.google.gson.annotations.SerializedName
import java.time.LocalDate
import java.util.UUID

data class MinimalJobIN(
    val id: UUID,
    val title: String,
    val description: String,
    val province: String,
)

data class JobIN(
    val id: UUID,
    val title: String,
    val description: String,
    val skills: List<String>,
    @SerializedName("work_schedule")
    val workSchedule: Availability,
    @SerializedName("required_experience")
    val requiredExperience: Int,
    val active: Boolean,
    @SerializedName("publication_date")
    val publicationDate: LocalDate,
    val sector: Sector,
    val address: AddressIN,
    @SerializedName("required_education")
    val requiredEducation: Map<String, Education>?,
    @SerializedName("language_list")
    val languages: List<LanguageWithLevelIN>?
)

data class BaseJob(
    val title: String,
    val description: String,
    val skills: List<String>,
    @SerializedName("work_schedule")
    val workSchedule: Availability,
    @SerializedName("required_experience")
    val requiredExperience: Int,
    val active: Boolean,
    val address: AddressOUT,
    @SerializedName("required_education")
    val requiredEducation: UUID?,
    @SerializedName("sector_id")
    val sectorId: UUID,
    @SerializedName("company_id")
    val companyId: UUID,
)

data class JobOUT(
    @SerializedName("job")
    val baseJob: BaseJob,
    @SerializedName("job_languages")
    val languages: List<LanguageWithLevelOUT>?,
)

data class UpdateJobOUT(
    val title: String,
    val description: String,
    val skills: List<String>,
    @SerializedName("work_schedule")
    val workSchedule: Availability,
    @SerializedName("required_experience")
    val requiredExperience: Int,
    val address: AddressOUT,
    @SerializedName("required_education")
    val requiredEducation: UUID?,
    @SerializedName("sector_id")
    val sector: UUID,
    @SerializedName("company_id")
    val companyId: UUID,
    val active: Boolean,
)

data class PartialUpdateJobOUT(
    val title: String? = null,
    val description: String? = null,
    val skills: List<String>? = null,
    @SerializedName("work_schedule")
    val workSchedule: Availability? = null,
    @SerializedName("required_experience")
    val requiredExperience: Int? = null,
    val address: AddressOUT? = null,
    @SerializedName("required_education")
    val requiredEducation: UUID? = null,
    @SerializedName("sector_id")
    val sector: UUID? = null,
    @SerializedName("company_id")
    val companyId: UUID? = null,
    val active: Boolean? = null
)