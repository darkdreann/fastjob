package com.fastjob.models.serializer

import android.util.Log
import com.fastjob.models.UserType
import com.google.gson.JsonDeserializationContext
import com.google.gson.JsonDeserializer
import com.google.gson.JsonElement
import com.google.gson.JsonParseException
import com.google.gson.JsonSerializationContext
import com.google.gson.JsonSerializer
import java.lang.reflect.Type

class UserTypeSerializer: JsonDeserializer<UserType>, JsonSerializer<UserType> {
    /**
     * Deserializa un [JsonElement] a un [UserType]
     */
    override fun deserialize(json: JsonElement?, typeOfT: Type?, context: JsonDeserializationContext?): UserType {
        val enumString = json?.asString ?: "ANY"
        return try {
            UserType.valueOf(enumString)
        } catch (e: IllegalArgumentException) {
            Log.e("UserTypeSerializer", "Error serializer: $enumString")
            UserType.CANDIDATE
        }
    }

    /**
     * Serializa un [UserType] a un [JsonElement]
     */
    override fun serialize(
        src: UserType?,
        typeOfSrc: Type?,
        context: JsonSerializationContext?
    ): JsonElement {
        return context?.serialize(src?.value)
            ?: context?.serialize(UserType.CANDIDATE.value)
            ?: throw JsonParseException("Error")
    }
}