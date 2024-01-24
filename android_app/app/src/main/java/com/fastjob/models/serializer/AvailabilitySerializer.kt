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

/**
 * Serializador y deserializador de la enumeración [Availability]
 */
class AvailabilitySerializer : JsonDeserializer<Availability>, JsonSerializer<Availability> {
    /**
     * Deserializa un [JsonElement] a un [Availability]
     */
    override fun deserialize(json: JsonElement?, typeOfT: Type?, context: JsonDeserializationContext?): Availability {
        val enumString = json?.asString ?: "ANY"
        return try {
            Availability.getByValue(enumString)
        } catch (e: IllegalArgumentException) {
            Log.d("AvailabilitySerializer", "Error serializer: $enumString")
            Availability.ANY
        }
    }

    /**
     * Serializa un [Availability] a un [JsonElement]
     */
    override fun serialize(
        src: Availability?,
        typeOfSrc: Type?,
        context: JsonSerializationContext?
    ): JsonElement {
        return context?.serialize(src?.value)
            ?: context?.serialize(Availability.ANY.value)
            ?: throw JsonParseException("Error")
    }
}