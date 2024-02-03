package com.fastjob.network

import com.fastjob.models.Availability
import com.fastjob.models.CandidateExtraFields
import com.fastjob.models.UserType
import com.fastjob.models.serializer.AvailabilitySerializer
import com.fastjob.models.serializer.CandidateExtraFieldsSerializer
import com.fastjob.models.serializer.LocalDateSerializer
import com.fastjob.models.serializer.UserTypeSerializer
import com.google.gson.Gson
import com.google.gson.GsonBuilder
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.time.LocalDate
import java.util.concurrent.TimeUnit

class Client private constructor() {
    // STATIC
    companion object {
        private const val URL = "http://192.168.1.54:8080/"
        private val clientInstance: Client by lazy { Client() }

        fun getInstance(): Client {
            return clientInstance
        }
    }

    private val retrofitClient: Retrofit

    init {
        // GSON Converter
        val gson: Gson = GsonBuilder()
                            .registerTypeAdapter(Availability::class.java, AvailabilitySerializer())
                            .registerTypeAdapter(LocalDate::class.java, LocalDateSerializer())
                            .registerTypeAdapter(UserType::class.java, UserTypeSerializer())
                            .registerTypeAdapter(CandidateExtraFieldsSerializer::class.java, CandidateExtraFieldsSerializer())
                            .create()
        val gsonFactory = GsonConverterFactory.create(gson)
        // Creamos el objeto Retrofit
        this.retrofitClient = Retrofit.Builder()
            .baseUrl(URL)
            .client(
                OkHttpClient.Builder()
                    .connectTimeout(15, TimeUnit.SECONDS)
                    .addInterceptor(GlobalErrorInterceptor())
                    .build()
            )
            .addConverterFactory(gsonFactory)
            .build()
    }

    fun <Service> getService(service: Class<Service>): Service {
        return this.retrofitClient.create(service)
    }

}