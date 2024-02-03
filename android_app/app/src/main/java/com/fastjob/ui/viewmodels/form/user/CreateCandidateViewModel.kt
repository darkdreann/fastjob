package com.fastjob.ui.viewmodels.form.user

import androidx.lifecycle.viewModelScope
import com.fastjob.models.Availability
import com.fastjob.models.CandidateOUT
import com.fastjob.network.Client
import com.fastjob.services.CandidateService
import com.fastjob.ui.enums.RegisterState
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

/**
 * ViewModel para el formulario de creación de candidatos
 * @property registerState MutableStateFlow<RegisterState> flujo de datos del estado del registro
 * @property candidateData MutableStateFlow<CandidateOUT> flujo de datos del candidato
 * @property candidateService CandidateService servicio de candidatos
 */
class CreateCandidateViewModel: CreateUserViewModel() {
    companion object {
        private val candidateService = Client.getInstance().getService(CandidateService::class.java)
    }

    // register state
    private val _registerState = MutableStateFlow(RegisterState.NOT_POSTED)
    val registerState = _registerState.asStateFlow()

    // error visibility state
    private val _errorVisibility = MutableStateFlow(false)
    val errorVisibility = _errorVisibility.asStateFlow()

    // candidate data state
    private val _candidateData = MutableStateFlow(
        CandidateOUT(
            skills = emptyList(),
            availabilities = emptyList(),
            user = userData.value
        )
    )
    val candidateData = _candidateData.asStateFlow()

    /**
     * Establece las habilidades
     * @param skills List<String> habilidades
     */
    fun setSkills(skills: List<String>) {
        _candidateData.value = _candidateData.value.copy(skills = skills)
    }

    /**
     * Establece las disponibilidades
     * @param availabilities Set<Availability> disponibilidades
     */
    fun setAvailabilities(availabilities: Set<Availability>) {
        _candidateData.value = _candidateData.value.copy(availabilities = availabilities.toList())
    }

    /**
     * Establece la visibilidad del dialogo de error
     * @param visibility Boolean visibilidad
     */
    fun setErrorVisibility(visibility: Boolean) {
        _errorVisibility.value = visibility
    }

    /**
     * Registra un candidato en la base de datos si los datos son válidos
     */
    fun registerCandidate() {
        // comprobar si los datos del usuario están vacíos
        checkUserDataEmpty()
        // si hay algún error en los datos del usuario, no se registra
        if(userError.value.anyTrue()) {
            // mostrar error en el formulario y terminar la función
            _registerState.value = RegisterState.FORM_NOT_VALID
            return
        }

        // establecer el usuario del candidato
        _candidateData.value = _candidateData.value.copy(user = userData.value)

        // registrar el candidato de forma asíncrona con dispatchers IO
        viewModelScope.launch(Dispatchers.IO) {
            val response = candidateService.createCandidate(candidateData.value)

            _errorVisibility.value = !response.isSuccessful
            // comprobar el código de respuesta
            when(response.code()) {
                // si el registro es correcto, establecer el estado del registro a REGISTERED
                201 -> _registerState.value = RegisterState.REGISTERED
                // si el nombre de usuario o el email ya existen, establecer el estado del registro a DUPLICATED_USERNAME o DUPLICATED_EMAIL
                409 -> {
                    if(response.errorBody()?.string()?.contains("email") == false) {
                        _registerState.value = RegisterState.DUPLICATED_USERNAME
                    }else{
                        _registerState.value = RegisterState.DUPLICATED_EMAIL
                    }
                }
                // si ha ocurrido un error desconocido, establecer el estado del registro a UNKNOWN_ERROR
                else -> _registerState.value = RegisterState.UNKNOWN_ERROR
            }
        }
    }
}