package com.fastjob.ui.viewmodels.form.candidate

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import androidx.navigation.NavController
import com.fastjob.auth.AuthAPI
import com.fastjob.models.Availability
import com.fastjob.models.PartialCandidateOUT
import com.fastjob.network.Client
import com.fastjob.services.CandidateService
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

/**
 * ViewModel para la actualizacion de habilidades y jornadas de un candidato
 * @param navController controlador de navegacion
 * @param currentAvailabilities jornadas actuales del candidato
 * @param currentSkills habilidades actuales del candidato
 */
class UpdateSkillAvailabilityViewModel(
    val navController: NavController,
    currentAvailabilities: List<Availability>,
    currentSkills: List<String>
) : ViewModel() {
    // static
    companion object{
        private val candidateService = Client.getInstance().getService(CandidateService::class.java)
        val auth = AuthAPI.getInstance()
    }

    // estado de las jornadas
    private val _availabilities = MutableStateFlow(currentAvailabilities)
    val availabilities = _availabilities.asStateFlow()

    // estado de las habilidades
    private val _skills = MutableStateFlow(currentSkills)
    val skills = _skills.asStateFlow()

    // visibilidad del error
    private val _errorVisibility = MutableStateFlow(false)
    val errorVisibility = _errorVisibility.asStateFlow()

    /**
     * Actualiza las jornadas del candidato
     * @param availabilities jornadas del candidato
     */
    fun setAvailabilities(availabilities: Set<Availability>){
        _availabilities.value = availabilities.toList()
    }

    /**
     * Actualiza las habilidades  del candidato
     * @param skills habilidades del candidato
     */
    fun setSkills(skills: List<String>){
        _skills.value = skills
    }

    /**
     * Actualiza la visibilidad del error
     * @param visibility visibilidad del error
     */
    fun setErrorVisibility(visibility: Boolean){
        _errorVisibility.value = visibility
    }

    /**
     * Actualiza las habilidades y jornadas del candidato
     */
    fun updateCandidateSkillsAvailabilities(){
        if(!auth.isAuthenticated()) return

        viewModelScope.launch(Dispatchers.IO) {
            // se actualiza el candidato
            val response = candidateService.partialUpdateCandidate(
                auth = auth.getToken()!!,
                id = auth.getUserId()!!,
                candidate = PartialCandidateOUT(
                    skills = skills.value,
                    availabilities = availabilities.value
                )
            )

            // se muestra el error si no fue exitoso
            _errorVisibility.value = !response.isSuccessful
            // se navega a la pantalla anterior si fue exitoso
            if(response.isSuccessful){
                withContext(Dispatchers.Main){ navController.popBackStack() }
            }



        }

    }

}

/**
 * Factory para la creacion del ViewModel
 * @param navController controlador de navegacion
 * @param currentAvailabilities jornadas actuales del candidato
 * @param currentSkills habilidades actuales del candidato
 */
class UpdateSkillAvailabilityViewModelFactory(
    private val navController: NavController,
    private val currentAvailabilities: List<Availability>,
    private val currentSkills: List<String>
): ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return UpdateSkillAvailabilityViewModel(navController, currentAvailabilities, currentSkills) as T
    }
}