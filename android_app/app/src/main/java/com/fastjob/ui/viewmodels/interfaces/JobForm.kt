package com.fastjob.ui.viewmodels.interfaces

import com.fastjob.models.Availability
import kotlinx.coroutines.flow.StateFlow
import java.util.UUID




/**
 * Interfaz para el formulario de una oferta de trabajo
 * @property jobData StateFlow<BasicJobData> datos de la oferta
 * @property jobDataError StateFlow<BasicJobDataError> errores de los datos de la oferta
 * @property setJobData función para establecer los datos de la oferta
 * @property setJobDataError función para establecer los errores de los datos de la oferta
 */
interface JobForm {
    val jobData: StateFlow<BasicJobData>
    val jobDataError: StateFlow<BasicJobDataError>
    fun setJobData(jobData: BasicJobData)
    fun setJobDataError(jobDataError: BasicJobDataError)
}


/**
 * Datos básicos de una oferta de trabajo
 * @property title String título de la oferta
 * @property description String descripción de la oferta
 * @property skills List<String> habilidades requeridas
 * @property workSchedule Availability horario de trabajo
 * @property requiredExperience Int experiencia requerida
 * @property active Boolean estado de la oferta
 * @property sectorId UUID? id del sector
 * @property companyId UUID? id de la empresa
 */
data class BasicJobData(
    val title: String = "",
    val description: String = "",
    val skills: List<String> = emptyList(),
    val workSchedule: Availability = Availability.ANY,
    val requiredExperience: String = "",
    val active: Boolean = true,
    val sectorCategory: String = "",
    val sectorSubcategory: String = "",
    val sectorId: UUID? = null
)

/**
 * Errores de los datos básicos de una oferta de trabajo
 * @property title Boolean error del título
 * @property description Boolean error de la descripción
 * @property requiredExperience Boolean error de la experiencia requerida
 * @property sectorId Boolean error del id del sector
 * @property companyId Boolean error del id de la empresa
 */
data class BasicJobDataError(
    val title: Boolean = false,
    val description: Boolean = false,
    val requiredExperience: Boolean = false,
    val sectorId: Boolean = false
){
    val hasError: Boolean
        get() = title || description || requiredExperience || sectorId
}

/**
 * Establece la formación de la oferta
 * @property educationQualification String nombre de la formación
 * @property educationId UUID? id de la formación
 */
data class JobEducation(
    val educationQualification: String = "",
    val educationId: UUID? = null
)

/**
 * Data class que representa un idioma de una oferta de trabajo
 * @property languageName String nombre del idioma
 * @property languageId UUID? id del idioma
 * @property languageLevelName String nombre del nivel del idioma
 * @property languageLevelId UUID? id del nivel del idioma
 */
data class JobLanguage(
    val languageName: String = "",
    val languageId: UUID? = null,
    val languageLevelName: String = "",
    val languageLevelId: UUID? = null
)