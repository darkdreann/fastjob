package com.fastjob.ui.viewmodels.company

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import androidx.navigation.NavController
import com.fastjob.auth.AuthAPI
import com.fastjob.models.PartialUpdateJobOUT
import com.fastjob.network.Client
import com.fastjob.services.JobService
import com.fastjob.ui.enums.LoadState
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.viewmodels.candidate.CandidateExperienceViewModel
import com.fastjob.ui.viewmodels.interfaces.JobEducation
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.util.UUID

/**
 * ViewModel para la pantalla de actualización de la formación de la oferta de trabajo
 * @param navController NavController controlador de navegación
 * @param jobId UUID identificador de la oferta de trabajo
 */
class UpdateCompanyJobEducationViewModel(
    val navController: NavController,
    private val jobId: UUID
) : ViewModel(){
    // static
    companion object {
        private val jobService = Client.getInstance().getService(JobService::class.java)
        val auth = AuthAPI.getInstance()
    }

    // estado de carga
    private val _loadState = MutableStateFlow(LoadState.LOADING)
    val loadState = _loadState.asStateFlow()

    // estado de la formacion
    private val _jobEducationId = MutableStateFlow<UUID?>(null)
    val jobEducationId = _jobEducationId.asStateFlow()
    private val _jobEducationName = MutableStateFlow("")
    val jobEducationName = _jobEducationName.asStateFlow()

    // dialogo de la oferta de trabajo
    private val _jobDialogVisibility = MutableStateFlow(false)
    val jobDialogVisibility = _jobDialogVisibility.asStateFlow()


    /**
     * Establece la visibilidad del dialogo de la oferta
     * @param visibility Boolean visibilidad del dialogo
     */
    fun setJobDialogVisibility(visibility: Boolean) {
        _jobDialogVisibility.value = visibility
    }

    /**
     * Establece el identificador de la formacion de la oferta de trabajo
     * @param id UUID identificador de la formacion
     */
    fun setJobEducationId(id: UUID?){
        _jobEducationId.value = id
    }

    /**
     * Establece el nombre de la formacion de la oferta de trabajo
     * @param name String nombre de la formacion
     */
    fun setJobEducationName(name: String){
        _jobEducationName.value = name
    }

    /**
     * Carga la formacion de la oferta de trabajo
     */
    fun loadJobEducation() {
        if(!auth.isAuthenticated()) {
            _loadState.value = LoadState.ERROR
            return
        }

        viewModelScope.launch(Dispatchers.IO){
            val response = jobService.getJobEducation(
                auth = CandidateExperienceViewModel.auth.getToken()!!,
                id = jobId
            )

            if(response.isSuccessful) {
                response.body()?.let {
                    _jobEducationId.value = it.id
                    _jobEducationName.value = it.qualification

                    _loadState.value = LoadState.LOADED
                } ?: run {
                    _loadState.value = LoadState.ERROR
                }

            } else {
                _loadState.value = if(response.code() != 404) LoadState.ERROR else LoadState.LOADED
            }
        }
    }

    /**
     * Actualiza la oferta de trabajo
     */
    fun updateJobEducation(){
        if(!auth.isAuthenticated()) return
        if(_jobEducationId.value == null) {
            deleteJobEducation()
            return
        }

        viewModelScope.launch(Dispatchers.IO) {
            val response = jobService.partialUpdateJob(
                auth = auth.getToken()!!,
                id = jobId,
                job = PartialUpdateJobOUT(
                    requiredEducation = _jobEducationId.value
                )
            )

            _jobDialogVisibility.value = !response.isSuccessful
            if(response.isSuccessful){
                withContext(Dispatchers.Main){ navController.popBackStack() }
            }
        }
    }

    /**
     * Elimina la formacion de la oferta de trabajo
     */
    private fun deleteJobEducation(){
        if(!auth.isAuthenticated()) return

        viewModelScope.launch(Dispatchers.IO) {
            val response = jobService.deleteJobEducation(
                auth = auth.getToken()!!,
                id = jobId,
            )

            if(response.isSuccessful || response.code() == 404){
                withContext(Dispatchers.Main){ navController.popBackStack() }
            }
        }
    }
}

/**
 * Factoria de la vista modelo de la formacion de la oferta de trabajo
 * @param navController NavController controlador de navegación
 * @param jobId UUID identificador de la oferta de trabajo
 */
class UpdateCompanyJobEducationViewModelFactory(
    private val navController: NavController,
    private val jobId: UUID
): ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return UpdateCompanyJobEducationViewModel(navController, jobId) as T
    }
}




