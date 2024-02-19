package com.fastjob.services

import com.fastjob.models.AddressNoStreetIN
import retrofit2.Response
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.Path
import retrofit2.http.Query

interface AddressService {
    companion object {
        private const val ENDPOINT = "/addresses/"
        private const val ADDRESS_BY_POSTAL_CODE = "${ENDPOINT}postal-code/{postal_code}"
        private const val ADDRESS_PROVINCES = "${ENDPOINT}province/{province_keyword}/"
    }

    @GET(ADDRESS_BY_POSTAL_CODE)
    suspend fun getAddressByPostalCode(
        @Header("Authorization") auth: String? = null,
        @Path("postal_code") postalCode: Int
    ): Response<AddressNoStreetIN>

    @GET(ADDRESS_PROVINCES)
    suspend fun getAddressProvinces(
        @Header("Authorization") auth: String? = null,
        @Path("province_keyword") provinceKeyword: String,
        @Query("limit") limit: Int? = null,
        @Query("offset") offset: Int? = null
    ): Response<List<String>>
}