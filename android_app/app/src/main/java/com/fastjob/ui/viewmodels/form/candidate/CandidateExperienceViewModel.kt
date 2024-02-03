package com.fastjob.ui.viewmodels.form.candidate

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import androidx.navigation.NavController
import com.fastjob.auth.AuthAPI
import com.fastjob.models.ExperienceOUT
import com.fastjob.network.Client
import com.fastjob.services.CandidateExperienceService
import com.fastjob.ui.enums.LoadState
import com.fastjob.ui.viewmodels.form.user.UpdatePasswordViewModel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.time.LocalDate
import java.util.UUID

class CandidateExperienceViewModel(
    private val navController: NavController,
    private val id: UUID? = null
) : ViewModel() {
    // static
    companion object {
        private val candidateExpService = Client.getInstance().getService(CandidateExperienceService::class.java)
        val auth = AuthAPI.getInstance()
    }

    // estado de carga
    private val _loadState = MutableStateFlow(LoadState.LOADING)
    val loadState = _loadState.asStateFlow()

    // experiencia
    private val _experience = MutableStateFlow(Experience())
    val experience = _experience.asStateFlow()

    // visibilidad de error
    private val _errorVisibility = MutableStateFlow(false)
    val errorVisibility = _errorVisibility.asStateFlow()

    // error de la experiencia
    private val _experienceError = MutableStateFlow(ExperienceError())
    val experienceError = _experienceError.asStateFlow()

    // no end date state
    private val _noEndDateState = MutableStateFlow(false)
    val noEndDateState = _noEndDateState.asStateFlow()

    /**
     * Establece el estado de no end date
     * @param value valor del estado
     */
    fun setNoEndDateState(value: Boolean) {
        _noEndDateState.value = value
    }

    /**
     * Establece la experiencia
     * @param experience experiencia
     */
    fun setExperience(experience: Experience) {
        _experience.value = experience
    }


    /**
     * Establece la visibilidad del error
     * @param value valor de la visibilidad
     */
    fun setErrorVisibility(value: Boolean) {
        _errorVisibility.value = value
    }


    /**
     * Valida la experiencia
     * @return true si es valida, false si no
     */
    private fun validateExperience(): Boolean {
        _experienceError.value = ExperienceError(
            companyName = experience.value.companyName.isEmpty(),
            jobPosition = experience.value.jobPosition.isEmpty(),
            jobPositionDescription = experience.value.jobPositionDescription.isEmpty(),
            sectorId = experience.value.sectorId == null
        )
        return !experienceError.value.hasError
            .or(experience.value.startDate == null)
            .or(experience.value.startDate?.isAfter(LocalDate.now())?:true)
            .or(experience.value.endDate?.isAfter(LocalDate.now())?:true)
            .or(experience.value.endDate?.isBefore(experience.value.startDate?:LocalDate.now())?:true)
    }


    /**
     * Carga la experiencia
     * Si el id es null carga una nueva experiencia
     */
    fun loadExperience(setSubcategory: (String) -> Unit) {
        if(!auth.isAuthenticated()) {
            _loadState.value = LoadState.ERROR
            return
        }

        if(id == null) {
            _loadState.value = LoadState.LOADED
            return
        }

        viewModelScope.launch(Dispatchers.IO){
            val response = candidateExpService.getExperience(
                auth = auth.getToken()!!,
                candidateId = auth.getUserId()!!,
                id = id
            )

            if(response.isSuccessful) {
                response.body()?.let {
                    _experience.value = Experience(
                        companyName = it.companyName,
                        jobPosition = it.jobPosition,
                        jobPositionDescription = it.jobPositionDescription,
                        startDate = it.startDate,
                        endDate = it.endDate,
                        sectorId = it.sector.id,
                        sectorCategory = it.sector.category,
                        sectorSubcategory = it.sector.subcategory
                    )
                    setSubcategory(it.sector.subcategory)
                    _noEndDateState.value = it.endDate == null
                    _loadState.value = LoadState.LOADED
                } ?: run {
                    _loadState.value = LoadState.ERROR
                }

            } else {
                _loadState.value = LoadState.ERROR
            }
        }
    }

    /**
     * Guarda la experiencia
     * Si el id es null crea una nueva experiencia
     * Si el id no es null actualiza la experiencia
     */
    fun saveExperience() {
        if(id == null) createExperience()
        else updateExperience()
    }

    /**
     * Crea una nueva experiencia
     * Si la experiencia no es valida establece el error
     */
    private fun createExperience() {
        if(!auth.isAuthenticated()) return

        if(!validateExperience()) {
            _errorVisibility.value = true
            return
        }

        viewModelScope.launch(Dispatchers.IO){
            val response = candidateExpService.createExperience(
                auth = auth.getToken()!!,
                candidateId = auth.getUserId()!!,
                experience = ExperienceOUT(
                    companyName = experience.value.companyName,
                    jobPosition = experience.value.jobPosition,
                    jobPositionDescription = experience.value.jobPositionDescription,
                    startDate = experience.value.startDate!!,
                    endDate = experience.value.endDate,
                    sectorId = experience.value.sectorId!!
                )
            )

            _errorVisibility.value = !response.isSuccessful
            if(response.isSuccessful) {
                withContext(Dispatchers.Main){ navController.popBackStack() }
            }
        }
    }

    /**
     * Actualiza la experiencia
     * Si la experiencia no es valida establece el error
     */
    private fun updateExperience() {
        if(!auth.isAuthenticated() || id == null) return

        if(!validateExperience()) {
            _errorVisibility.value = true
            return
        }

        viewModelScope.launch(Dispatchers.IO){
            val response = candidateExpService.updateExperience(
                auth = auth.getToken()!!,
                candidateId = auth.getUserId()!!,
                id = id,
                experience = ExperienceOUT(
                    companyName = experience.value.companyName,
                    jobPosition = experience.value.jobPosition,
                    jobPositionDescription = experience.value.jobPositionDescription,
                    startDate = experience.value.startDate!!,
                    endDate = experience.value.endDate,
                    sectorId = experience.value.sectorId!!
                )
            )

            _errorVisibility.value = !response.isSuccessful
            if(response.isSuccessful) {
                withContext(Dispatchers.Main){ navController.popBackStack() }
            }
        }
    }


    /**
     * Data class de la experiencia
     * @param companyName nombre de la empresa
     * @param jobPosition puesto de trabajo
     * @param jobPositionDescription descripcion del puesto de trabajo
     * @param startDate fecha de inicio
     * @param endDate fecha de fin
     * @param sectorId id del sector
     * @param sectorCategory categoria del sector
     * @param sectorSubcategory subcategoria del sector
     */
    data class Experience(
        val companyName: String = "",
        val jobPosition: String = "",
        val jobPositionDescription: String = "",
        val startDate: LocalDate? = null,
        val endDate: LocalDate? = null,
        val sectorId: UUID? = null,
        val sectorCategory: String = "",
        val sectorSubcategory: String = ""
    )

    /**
     * Data class de error de la experiencia
     * @param companyName error del nombre de la empresa
     * @param jobPosition error del puesto de trabajo
     * @param jobPositionDescription error de la descripcion del puesto de trabajo
     * @param sectorId error del id del sector
     */
    data class ExperienceError(
        val companyName: Boolean = false,
        val jobPosition: Boolean = false,
        val jobPositionDescription: Boolean = false,
        val sectorId: Boolean = false
    ){
        val hasError: Boolean
            get() = companyName
                .or(jobPosition)
                .or(jobPositionDescription)
                .or(sectorId)
    }
}

/**
 * Factory de CandidateExperienceViewModel
 * @param navController controlador de navegacion
 * @param id id de la experiencia
 */
class CandidateExperienceViewModelFactory(
    private val navController: NavController,
    private val id: UUID? = null
): ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return CandidateExperienceViewModel(navController, id) as T
    }
}