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

data class JobOUT(
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
    val companyId: UUID
)

data class PartialUpdateJobOUT(
    val title: String?,
    val description: String?,
    val skills: List<String>?,
    @SerializedName("work_schedule")
    val workSchedule: Availability?,
    @SerializedName("required_experience")
    val requiredExperience: Int?,
    val address: AddressOUT?,
    @SerializedName("required_education")
    val requiredEducation: UUID?,
    @SerializedName("sector_id")
    val sector: UUID?,
    @SerializedName("company_id")
    val companyId: UUID?
)