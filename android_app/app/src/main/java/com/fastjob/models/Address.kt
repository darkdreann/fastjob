package com.fastjob.models

import com.google.gson.annotations.SerializedName
import java.util.UUID

data class AddressIN(
    val id: UUID,
    @SerializedName("postal_code")
    val postalCode: Int,
    val street: String,
    val city: String,
    val province: String
)

data class AddressOUT(
    @SerializedName("postal_code")
    val postalCode: Int,
    val street: String,
    val city: String,
    val province: String
)