package com.fastjob.models

import com.google.gson.annotations.SerializedName
import java.util.UUID

enum class UserType(val value: String) {
    CANDIDATE("CANDIDATE"),
    COMPANY("COMPANY"),
    ADMIN("ADMIN")
}

data class UserIN(
    val id: UUID,
    val username: String,
    val email: String,
    val name: String,
    val surname: String,
    @SerializedName("phone_numbers")
    val phoneNumbers: List<Int>,
    @SerializedName("user_type")
    val userType: UserType,
    val address: AddressIN
)

data class UserOUT(
    val username: String,
    val email: String,
    val name: String,
    val surname: String,
    val password: String,
    @SerializedName("phone_numbers")
    val phoneNumbers: List<Int>,
    val address: AddressOUT
)

data class PartialUserOUT(
    val username: String?,
    val email: String?,
    val name: String?,
    val surname: String?,
    val password: String?,
    @SerializedName("phone_numbers")
    val phoneNumbers: List<Int>?,
    val address: AddressOUT?
)
