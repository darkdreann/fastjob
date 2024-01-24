package com.fastjob.models

import java.util.UUID


data class Sector(
    val id: UUID,
    val category: String,
    val subcategory: String,
)

data class SectorSubcategory(
    val id: UUID,
    val subcategory: String
)