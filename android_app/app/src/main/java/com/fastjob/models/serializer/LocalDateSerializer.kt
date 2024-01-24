package com.fastjob.models.serializer

import android.util.Log
import com.fastjob.models.Availability
import com.google.gson.JsonDeserializationContext
import com.google.gson.JsonDeserializer
import com.google.gson.JsonElement
import com.google.gson.JsonParseException
import com.google.gson.JsonSerializationContext
import com.google.gson.JsonSerializer
import java.lang.reflect.Type
import java.time.LocalDate


class LocalDateSerializer : JsonDeserializer<LocalDate>, JsonSerializer<LocalDate> {
    /**
     * Deserializa un [JsonElement] a un [Availability]
     */
    override fun deserialize(json: JsonElement?, typeOfT: Type?, context: JsonDeserializationContext?): LocalDate {
        val dateString = json?.asString ?: ""
        return try {
            LocalDate.parse(dateString)
        } catch (e: Exception) {
            Log.e("LocalDateSerializer", "Error serializer: ${e.message}")
            LocalDate.now()
        }
    }

    /**
     * Serializa un [Availability] a un [JsonElement]
     */
    override fun serialize(
        src: LocalDate?,
        typeOfSrc: Type?,
        context: JsonSerializationContext?
    ): JsonElement? {
        return context?.serialize(src?.toString())
            ?: context?.serialize(LocalDate.now().toString())
            ?: throw JsonParseException("Error")
    }
}

