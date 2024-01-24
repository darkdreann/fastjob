package com.fastjob.models


import com.fastjob.R
import com.google.gson.JsonDeserializationContext
import com.google.gson.JsonDeserializer
import com.google.gson.JsonElement
import com.google.gson.JsonParseException
import com.google.gson.JsonSerializationContext
import com.google.gson.JsonSerializer
import java.lang.reflect.Type


/**
 * Enum que representa la disponibilidad laboral
 */
enum class Availability(
    val value: String,
    val displayName: Int
) {
    FULL_TIME("FULL-TIME", R.string.job_availability_full_time),
    PART_TIME("PART-TIME", R.string.job_availability_part_time),
    MORNING("MORNING", R.string.job_availability_morning),
    AFTERNOON("AFTERNOON", R.string.job_availability_afternoon),
    DAY("DAY", R.string.job_availability_day),
    NIGHT("NIGHT", R.string.job_availability_night),
    FLEXTIME("FLEXTIME", R.string.job_availability_flextime),
    REMOTE_WORK("REMOTE-WORK", R.string.job_availability_remote_work),
    ANY("ANY", R.string.job_availability_any);

    companion object {
        fun getByValue(value: String): Availability {
            return values().find { it.value == value } ?: ANY
        }

        fun getDisplayNameByValue(value: String): Int {
            return values().find { it.value == value }?.displayName ?: ANY.displayName
        }
    }
}
