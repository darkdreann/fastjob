package com.fastjob.models

import com.google.gson.annotations.SerializedName
import java.util.UUID

data class Language(
    val id: UUID,
    val name: String
)

data class LanguageLevel(
    val id: UUID,
    val name: String,
    val value: Int
)

data class LanguageWithLevelIN(
    val language: Language,
    @SerializedName("language_level")
    val level: LanguageLevel
)

data class LanguageWithLevelOUT(
    @SerializedName("language_id")
    val language: UUID,
    @SerializedName("level_id")
    val level: UUID
)
