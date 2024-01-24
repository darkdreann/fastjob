package com.fastjob.services

import com.fastjob.models.Token
import retrofit2.Response
import retrofit2.http.Field
import retrofit2.http.FormUrlEncoded
import retrofit2.http.Header
import retrofit2.http.POST

interface LoginService {
    companion object {
        private const val ENDPOINT = "/login/"
        private const val RENEW_TOKEN_ENDPOINT = "${ENDPOINT}renew/"
    }

    @FormUrlEncoded
    @POST(ENDPOINT)
    suspend fun login(
        @Field("username") username: String,
        @Field("password") password: String
    ): Response<Token>

    @POST(RENEW_TOKEN_ENDPOINT)
    suspend fun renewToken(@Header("Authorization") auth: String): Response<Token>

}