package com.fastjob.services

import com.fastjob.models.CompanyIN
import com.fastjob.models.CompanyOUT
import com.fastjob.models.JobIN
import com.fastjob.models.PartialCompanyOUT
import okhttp3.ResponseBody
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.DELETE
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.PATCH
import retrofit2.http.POST
import retrofit2.http.PUT
import retrofit2.http.Path
import retrofit2.http.Query
import java.util.UUID

interface CompanyService {

    companion object {
        private const val ENDPOINT = "/companies/"
        private const val COMPANY_BY_ID = "${ENDPOINT}/{id}/"
        private const val GET_JOBS = "${COMPANY_BY_ID}jobs/"
    }

    @GET(COMPANY_BY_ID)
    suspend fun getCompany(
        @Header("Authorization") auth: String,
        @Path("id") id: UUID,
        @Query("get_jobs") getJobs: Boolean? = null
    ): Response<CompanyIN>

    @GET(GET_JOBS)
    suspend fun getCompanyJobs(
        @Header("Authorization") auth: String,
        @Path("id") id: UUID,
        @Query("limit") limit: Int? = null,
        @Query("offset") offset: Int? = null
    ): Response<List<JobIN>>

    @POST(ENDPOINT)
    suspend fun createCompany(
        @Body company: CompanyOUT
    ): Response<CompanyIN>

    @PUT(COMPANY_BY_ID)
    suspend fun updateCompany(
        @Header("Authorization") auth: String,
        @Path("id") id: UUID,
        @Body company: CompanyOUT
    ): Response<CompanyIN>

    @PATCH(COMPANY_BY_ID)
    suspend fun partialUpdateCompany(
        @Header("Authorization") auth: String,
        @Path("id") id: UUID,
        @Body company: PartialCompanyOUT
    ): Response<CompanyIN>

    @DELETE(COMPANY_BY_ID)
    suspend fun deleteCompany(
        @Header("Authorization") auth: String,
        @Path("id") id: UUID
    ): Response<Unit>

}