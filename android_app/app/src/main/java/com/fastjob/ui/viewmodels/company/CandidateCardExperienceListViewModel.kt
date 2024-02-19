package com.fastjob.ui.viewmodels.company

import androidx.compose.foundation.lazy.LazyListState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.fastjob.auth.AuthAPI
import com.fastjob.models.ExperienceIN
import com.fastjob.network.Client
import com.fastjob.services.CandidateExperienceService
import com.fastjob.services.JobCandidateService
import com.fastjob.ui.enums.LoadState
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.cancelAndJoin
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking
import java.util.UUID

/**
 * ViewModel para la lista de experiencias del candidato
 * @param jobId id de la oferta de trabajo
 * @param candidateId id del candidato
 */
class CandidateCardExperienceListViewModel(
    private val jobId: UUID,
    private val candidateId: UUID
): ViewModel() {
    // static
    companion object {
        private const val LIMIT = 10
        private val jobCandidateService = Client.getInstance().getService(JobCandidateService::class.java)
        val auth = AuthAPI.getInstance()
    }

    // list load state
    private val _loadState = MutableStateFlow(LoadState.START)
    val loadState = _loadState.asStateFlow()

    // list state
    private var lastOffset by mutableIntStateOf(0)
    private val _experienceList = MutableStateFlow<List<ExperienceIN>>(emptyList())
    val experienceList = _experienceList.asStateFlow()

    // list scroll
    val listScroll = MutableStateFlow(LazyListState())

    // job async search
    private var updateListJob = MutableStateFlow<Job?>(null)



    /**
     * Cancela la actualizacion de la lista de trabajos
     */
    private suspend fun cancelLoad() {
        updateListJob.value?.let {
            if(it.isActive) {
                it.cancelAndJoin()
            }
        }
    }

    /**
     * Obtiene las experiencias del candidato
     */
    fun getExperiences() = runBlocking(Dispatchers.IO)  {
        // si no esta autenticado cambia el estado de la carga a error
        if(!auth.isAuthenticated()) {
            _loadState.value = LoadState.ERROR
            return@runBlocking
        }

        // cancela la carga anterior si existe
        cancelLoad()

        _loadState.value = LoadState.LOADING

        // inicia la carga y guarda el job para poder cancelarlo
        updateListJob.value = viewModelScope.launch(Dispatchers.IO) {

            // realiza la petición de las ofertas aplicadas del candidato
            val response = jobCandidateService.getJobCandidateExperiences(
                auth = auth.getToken()!!,
                jobId = jobId,
                candidateId = candidateId,
                limit = LIMIT,
                offset = 0
            )

            when {
                // si la respuesta es correcta cambia el estado de la carga a loaded, guarda las experiencias y el offset
                response.isSuccessful -> {
                    val experiences = response.body()
                    _experienceList.value = experiences?:emptyList()
                    lastOffset = experiences?.size?:0
                    _loadState.value = LoadState.LOADED
                }
                // si la respuesta es 404 cambia el estado de la carga a not found
                response.code() == 404 -> {
                    _loadState.value = LoadState.NOT_FOUND
                }
                // si la respuesta es otra cambia el estado de la carga a error
                else -> {
                    _loadState.value = LoadState.ERROR
                }
            }
        }
    }

    /**
     * Carga mas experiencias del candidato
     */
    fun loadMoreExperiences() = runBlocking(Dispatchers.IO) {
        // si no esta autenticado cambia el estado de la carga a error
        if(!auth.isAuthenticated()) {
            _loadState.value = LoadState.ERROR
            return@runBlocking
        }

        cancelLoad() // cancela la carga anterior si existe

        _loadState.value = LoadState.LOADING

        // inicia la carga y guarda el job para poder cancelarlo
        updateListJob.value = viewModelScope.launch(Dispatchers.IO) {


            // realiza la petición de las experiencias del candidato
            val response = jobCandidateService.getJobCandidateExperiences(
                auth = auth.getToken()!!,
                jobId = jobId,
                candidateId = candidateId,
                limit = LIMIT,
                offset = lastOffset
            )

            when {
                // si la respuesta es correcta cambia el estado de la carga a loaded, guarda las experiencias y el offset
                response.isSuccessful -> {
                    val experiences = response.body()
                    _experienceList.value = _experienceList.value.plus(experiences?:emptyList())
                    lastOffset = experiences?.size?:lastOffset
                    _loadState.value = LoadState.LOADED
                }
                // si la respuesta es 404 cambia el estado de la carga a end of list
                response.code() == 404 -> _loadState.value = LoadState.END_OF_LIST
                // si la respuesta es otra cambia el estado de la carga a error
                else -> {
                    _loadState.value = LoadState.ERROR
                }
            }
        }
    }

}

/**
 * Factory para el ViewModel
 * @param jobId id de la oferta de trabajo
 * @param candidateId id del candidato
 */
class CandidateCardExperienceListViewModelFactory(
    private val jobId: UUID,
    private val candidateId: UUID
): ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return CandidateCardExperienceListViewModel(jobId, candidateId) as T
    }
}