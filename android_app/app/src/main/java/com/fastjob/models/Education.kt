package com.fastjob.models

import com.google.gson.annotations.SerializedName
import java.time.LocalDate
import java.util.UUID

data class Education(
    val id: UUID,
    val qualification: String,
    val level: EducationLevel,
    val sector: Map<String, Sector>?
)

data class EducationLevel(
    val id: UUID,
    val name: String,
    val value: Int
)