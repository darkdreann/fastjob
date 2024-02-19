package com.fastjob.models

import com.google.gson.annotations.SerializedName

data class CompanyIN(
    val tin: String,
    @SerializedName("company_name")
    val companyName: String,
    val user: UserIN,
    val jobs: List<JobIN>
)

data class CompanyOUT(
    val tin: String,
    @SerializedName("company_name")
    val companyName: String,
    val user: UserOUT
)

data class PartialCompanyOUT(
    val tin: String? = null,
    @SerializedName("company_name")
    val companyName: String? = null,
    val user: PartialUserOUT? = null
)