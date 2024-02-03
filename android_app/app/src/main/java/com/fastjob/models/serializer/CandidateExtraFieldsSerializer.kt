package com.fastjob.models.serializer

import android.util.Log
import com.fastjob.models.CandidateExtraFields
import com.google.gson.JsonDeserializationContext
import com.google.gson.JsonDeserializer
import com.google.gson.JsonElement
import com.google.gson.JsonParseException
import com.google.gson.JsonSerializationContext
import com.google.gson.JsonSerializer
import java.lang.reflect.Type

class CandidateExtraFieldsSerializer: JsonDeserializer<CandidateExtraFields>, JsonSerializer<CandidateExtraFields> {
    /**
     * Deserializa un [JsonElement] a un [CandidateExtraFields]
     */
    override fun deserialize(json: JsonElement?, typeOfT: Type?, context: JsonDeserializationContext?): CandidateExtraFields {
        val enumString = json?.asString ?: "ANY"
        return try {
            CandidateExtraFields.valueOf(enumString)
        } catch (e: IllegalArgumentException) {
            Log.e("CandidateExtraFieldsSerializer", "Error serializer: $enumString")
            throw JsonParseException("Error")
        }
    }

    /**
     * Serializa un [CandidateExtraFields] a un [JsonElement]
     */
    override fun serialize(
        src: CandidateExtraFields?,
        typeOfSrc: Type?,
        context: JsonSerializationContext?
    ): JsonElement {
        return context?.serialize(src?.value)
            ?: throw JsonParseException("Error")
    }
}