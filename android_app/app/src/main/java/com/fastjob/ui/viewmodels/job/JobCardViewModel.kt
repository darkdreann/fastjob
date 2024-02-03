package com.fastjob.ui.viewmodels.job

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.fastjob.auth.AuthAPI
import com.fastjob.models.JobIN
import com.fastjob.network.Client
import com.fastjob.services.JobCandidateService
import com.fastjob.ui.enums.LoadState
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

/**
 * ViewModel para la tarjeta de oferta de trabajo
 */
class JobCardViewModel: ViewModel() {
    companion object{
        // instancia de autenticación
        val auth = AuthAPI.getInstance()
        val candidateJobService = Client.getInstance().getService(JobCandidateService::class.java)
    }

    // estado de carga de la oferta
    private val _loadState = MutableStateFlow(LoadState.LOADING)
    val loadState = _loadState.asStateFlow()

    // oferta
    private val _job = MutableStateFlow<JobIN?>(null)
    val job = _job.asStateFlow()

    // estado de candidatura
    private val _isApplied = MutableStateFlow(false)
    val isApplied = _isApplied.asStateFlow()

    // estado de carga de la candidatura
    private val _isAppliedLoading = MutableStateFlow(LoadState.LOADING)
    val isAppliedLoading = _isAppliedLoading.asStateFlow()


    /**
     * Establece el estado de carga de la oferta
     * @param state estado de carga
     */
    fun setLoadState(state: LoadState){
        _loadState.value = state
    }

    /**
     * Establece la oferta
     * @param job oferta
     */
    fun setJob(job: JobIN?){
        _job.value = job
    }

    /**
     * Establece el estado de candidatura
     * @param isApplied estado de candidatura
     */
    fun setIsApplied(isApplied: Boolean){
        _isApplied.value = isApplied
    }

    /**
     * Establece el estado de carga de la candidatura
     * @param state estado de carga
     */
    fun setIsAppliedLoading(state: LoadState){
        _isAppliedLoading.value = state
    }

    /**
     * Aplica o elimina la candidatura de la oferta
     */
    fun applyJob(){
        // si no está autenticado o no hay oferta, no hace nada
        if(!auth.isAuthenticated() || job.value == null) return

        // cambia el estado de carga de la candidatura
        viewModelScope.launch(Dispatchers.IO) {
            // cambia el estado de carga de la candidatura
            when (!isApplied.value) {
                true -> {
                    // aplica la candidatura
                    val response = candidateJobService.applyJob(
                        auth = auth.getToken()!!,
                        jobId = job.value!!.id,
                        candidateId = auth.getUserId()!!
                    )

                    // si la candidatura se ha aplicado correctamente, cambia el estado de candidatura
                    if(response.isSuccessful){
                        setIsApplied(true)
                    }
                }
                false -> {
                    // elimina la candidatura
                    val response = candidateJobService.removeJob(
                        auth = auth.getToken()!!,
                        jobId = job.value!!.id,
                        candidateId = auth.getUserId()!!
                    )

                    // si la candidatura se ha eliminado correctamente, cambia el estado de candidatura
                    if(response.isSuccessful){
                        setIsApplied(false)
                    }
                }
            }
        }
    }
}