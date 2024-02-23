package com.fastjob.ui.functions

import android.content.Context
import android.text.format.DateFormat
import androidx.core.text.isDigitsOnly
import java.time.LocalDate
import java.time.ZoneId
import java.util.Date
import java.util.Locale
import java.util.UUID

/**
 * Genera un texto de experiencia a partir de los meses de experiencia
 * @param exp meses de experiencia
 * @param labels etiquetas para el texto
 * @return texto de experiencia
 */
fun generateExperienceText(exp: Int, labels: List<String>): String? {
    if (exp == 0) return null

    // calcular anios y meses
    val years = exp / 12
    val months = exp % 12
    // desestructurar etiquetas
    val (experienceLabel, experienceYearLabel, experienceYearsLabel, experienceMonthLabel, experienceMonthsLabel) = labels
    val result: StringBuilder = StringBuilder(experienceLabel).append(" ")

    // anadir anios
    if(years > 0) {
        result.append(years)
            .append(" ")
            .append(if (years < 2) experienceYearLabel else experienceYearsLabel)
    }
    // anadir meses
    if(months > 0) {
        if(years > 0) result.append(" y ")
        result.append(months)
            .append(" ")
            .append(if (months < 2) experienceMonthLabel else experienceMonthsLabel)
    }
    return result.toString()
}

/**
 * Capitaliza un párrafo de texto.
 * @return párrafo capitalizado
 */
fun String.capitalizeParagraph(): String {
    return this.split(".").joinToString(separator = ". ") { it.trim().capitalize() }
}

/**
 * Capitaliza una cadena de texto.
 * @return cadena capitalizada
 */
fun String.capitalize(): String {
    return this.trim().replaceFirstChar { string ->
        if (string.isLowerCase()) string.titlecase(Locale.getDefault())
        else string.toString()
    }
}

/**
 * Capitaliza las palabras de una cadena de texto separadas por espacios.
 * @return cadena capitalizada
 */
fun String.capitalizeWords(): String {
    return this.split(" ").joinToString(" ") { it.capitalize() }
}

/**
 * Formatea una fecha con el formato local.
 * @param localContext contexto local
 * @return fecha formateada
 */
fun LocalDate.localFormat(localContext: Context): String {
    return DateFormat
            .getDateFormat(localContext)
            .format(Date.from(this
            .atStartOfDay()
            .atZone(ZoneId.systemDefault()).toInstant()))
}

/**
 * Comprueba si una cadena de texto es un email.
 * @return true si es un email, false en caso contrario

 */
fun String.isEmail(): Boolean {
    val regexEmail = Regex("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}")
    return regexEmail.matches(this)
}

/**
 * Comprueba si una cadena de texto es una contraseña segura.
 * @return true si es una contraseña segura, false en caso contrario
 */
fun String.isPasswordSecure(): Boolean {
    val passwordRegex = Regex("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[.!@#?\$%^&*()\\-_+=])[A-Za-z\\d?.!@#\$%^&*()\\-_+=]{8,}\$")
    return passwordRegex.matches(this)
}

/**
 * Convierte una cadena de texto a UUID.
 * @return UUID o null si no se puede convertir
 */
fun String.toUUID(): UUID? {
    return try {
        UUID.fromString(this)
    }catch (e: IllegalArgumentException) {
        null
    }

}

/**
 * Comprueba si una cadena de texto es un numero
 * @return true si es numero, false en caso contrario
 */
fun String.isDigit(): Boolean {
    return this.isNotEmpty() && this.isDigitsOnly()
}

/**
 * Convierte un Date a LocalDate.
 * @return LocalDate
 */
fun Date.toLocalDate(): LocalDate {
    return this.toInstant()
        .atZone(ZoneId.systemDefault())
        .toLocalDate()
}