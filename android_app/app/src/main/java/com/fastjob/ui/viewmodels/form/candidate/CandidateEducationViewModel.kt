package com.fastjob.ui.viewmodels.form.candidate

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import androidx.navigation.NavController
import com.fastjob.auth.AuthAPI
import com.fastjob.models.CandidateEducationOUT
import com.fastjob.network.Client
import com.fastjob.services.CandidateEducationService
import com.fastjob.ui.enums.LoadState
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.time.LocalDate
import java.util.UUID

class CandidateEducationViewModel(
    private val navController: NavController,
    private val id: UUID? = null
) : ViewModel() {
    // static
    companion object {
        private val candidateEducationService = Client.getInstance().getService(CandidateEducationService::class.java)
        val auth = AuthAPI.getInstance()
    }

    // estado de carga
    private val _loadState = MutableStateFlow(LoadState.LOADING)
    val loadState = _loadState.asStateFlow()

    // experiencia
    private val _education = MutableStateFlow(CandidateEducation())
    val education = _education.asStateFlow()

    // visibilidad de error
    private val _errorVisibility = MutableStateFlow(false)
    val errorVisibility = _errorVisibility.asStateFlow()

    // error de la experiencia
    private val _educationError = MutableStateFlow(CandidateEducationError())
    val educationError = _educationError.asStateFlow()


    /**
     * Verifica si la formacion es nueva
     * @return true si es para crear una nueva formacion, false si no
     */
    fun isNewEducation(): Boolean {
        return id == null
    }

    /**
     * Establece la formacion
     * @param candidateEducation formacion
     */
    fun setEducation(candidateEducation: CandidateEducation) {
        _education.value = candidateEducation
    }


    /**
     * Establece la visibilidad del error
     * @param value valor de la visibilidad
     */
    fun setErrorVisibility(value: Boolean) {
        _errorVisibility.value = value
    }


    /**
     * Valida la formacion
     * @return true si es valida, false si no
     */
    private fun validateEducation(): Boolean {
        _educationError.value = CandidateEducationError(
            educationId = education.value.educationId == null,
            completionDate = education.value.completionDate == null
        )
        return !_educationError.value.hasError
    }


    /**
     * Carga la formacion
     * Si el id es null carga una nueva formacion
     */
    fun loadEducation(setEducationName: (String) -> Unit) {
        if(!auth.isAuthenticated()) {
            _loadState.value = LoadState.ERROR
            return
        }

        if(id == null) {
            _loadState.value = LoadState.LOADED
            return
        }

        viewModelScope.launch(Dispatchers.IO){
            val response = candidateEducationService.getCandidateEducation(
                auth = auth.getToken()!!,
                candidateId = auth.getUserId()!!,
                id = id
            )

            if(response.isSuccessful) {
                response.body()?.let {
                    _education.value = CandidateEducation(
                        educationId = it.education.id,
                        educationQualification = it.education.qualification,
                        completionDate = it.completionDate
                    )
                    setEducationName(it.education.qualification)

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
     * Guarda la formacion
     * Si el id es null crea una nueva formacion
     * Si el id no es null actualiza la formacion
     */
    fun saveEducation() {
        if(id == null) createEducation()
        else updateEducation()
    }

    /**
     * Crea una formacion
     */
    private fun createEducation() {
        if(!auth.isAuthenticated()) return

        if(!validateEducation()) {
            _errorVisibility.value = true
            return
        }

        viewModelScope.launch(Dispatchers.IO){
            val response = candidateEducationService.createCandidateEducations(
                auth = auth.getToken()!!,
                candidateId = auth.getUserId()!!,
                candidateEducation = CandidateEducationOUT(
                    education = education.value.educationId!!,
                    completionDate = education.value.completionDate!!
                )
            )

            _errorVisibility.value = !response.isSuccessful
            if(response.isSuccessful) {
                withContext(Dispatchers.Main){ navController.popBackStack() }
            }
        }
    }

    /**
     * Actualiza una formacion
     */
    private fun updateEducation() {
        if(!auth.isAuthenticated() || id == null) return

        if(!validateEducation()) {
            _errorVisibility.value = true
            return
        }

        viewModelScope.launch(Dispatchers.IO){
            val response = candidateEducationService.updateCandidateEducations(
                auth = auth.getToken()!!,
                candidateId = auth.getUserId()!!,
                id = id,
                candidateEducationCompletionDate = education.value.completionDate!!
            )

            _errorVisibility.value = !response.isSuccessful
            if(response.isSuccessful) {
                withContext(Dispatchers.Main){ navController.popBackStack() }
            }
        }
    }

    /**
     * Data class que representa la formacion del candidato
     * @param educationId id de la formacion
     * @param educationQualification nombre de la formacion
     * @param completionDate fecha de finalizacion
     */
    data class CandidateEducation(
        val educationId: UUID? = null,
        val educationQualification: String = "",
        val completionDate: LocalDate? = null,
    )

    /**
     * Data class que representa los errores de la formacion
     * @param educationId error del id de la formacion
     * @param completionDate error de la fecha de finalizacion
     */
    data class CandidateEducationError(
        val educationId: Boolean = false,
        val completionDate: Boolean = false,
    ){
        val hasError: Boolean
            get() = educationId || completionDate
    }
}

/**
 * Factory para el view model de la formacion del candidato
 * @param navController controlador de navegacion
 * @param id id de la formacion
 */
class CandidateEducationViewModelFactory(
    private val navController: NavController,
    private val id: UUID? = null
): ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return CandidateEducationViewModel(navController, id) as T
    }
}