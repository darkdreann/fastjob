package com.fastjob.ui.viewmodels.job

import androidx.compose.foundation.lazy.LazyListState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.fastjob.auth.AuthAPI
import com.fastjob.models.MinimalJobIN
import com.fastjob.network.Client
import com.fastjob.services.CandidateService
import com.fastjob.ui.enums.LoadState
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.cancelAndJoin
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking

/**
 * ViewModel para la lista de trabajos de un candidato
 */
class CandidateJobListViewModel: ViewModel() {
    // static
    companion object {
        private const val LIMIT = 10
        private val candidateService = Client.getInstance().getService(CandidateService::class.java)
        val auth = AuthAPI.getInstance()
    }

    // list load state
    private val _loadState = MutableStateFlow(LoadState.START)
    val loadState = _loadState.asStateFlow()

    // list state
    private var lastOffset by mutableIntStateOf(0)
    private val _jobList = MutableStateFlow<List<MinimalJobIN>>(emptyList())
    val jobList = _jobList.asStateFlow()

    // job list scroll
    val jobListScroll = MutableStateFlow(LazyListState())

    // job async search
    private var updateListJob = MutableStateFlow<Job?>(null)

    /**
     * Cancela la actualizacion de la lista de trabajos
     */
    private suspend fun cancelSearch() {
        updateListJob.value?.let {
            if(it.isActive) {
                it.cancelAndJoin()
            }
        }
    }

    /**
     * Obtiene las ofertas aplicadas del candidato
     */
    fun getJobs() = runBlocking(Dispatchers.IO)  {
        // si no esta autenticado cambia el estado de la carga a error
        if(!auth.isAuthenticated()) {
            _loadState.value = LoadState.ERROR
            return@runBlocking
        }

        // cancela la carga anterior si existe
        cancelSearch()

        _loadState.value = LoadState.LOADING

        // inicia la carga y guarda el job para poder cancelarlo
        updateListJob.value = viewModelScope.launch(Dispatchers.IO) {

            // realiza la petición de las ofertas aplicadas del candidato
            val response = candidateService.getCandidateJobs(
                auth.getToken()!!,
                auth.getUserId()!!,
                LIMIT,
                0
            )

            when {
                // si la respuesta es correcta cambia el estado de la carga a loaded, guarda los trabajos y el offset
                response.isSuccessful -> {
                    val jobs = response.body()
                    _jobList.value = jobs?:emptyList()
                    lastOffset = jobs?.size?:0
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
     * Carga mas trabajos del candidato
     */
    fun loadMoreJobs() = runBlocking(Dispatchers.IO) {
        // si no esta autenticado cambia el estado de la busqueda a error
        if(!auth.isAuthenticated()) {
            _loadState.value = LoadState.ERROR
            return@runBlocking
        }

        cancelSearch() // cancela la carga anterior si existe

        _loadState.value = LoadState.LOADING

        // inicia la carga y guarda el job para poder cancelarlo
        updateListJob.value = viewModelScope.launch(Dispatchers.IO) {


            // realiza la carga de mas trabajos del candidato
            val response = candidateService.getCandidateJobs(
                auth.getToken()!!,
                auth.getUserId()!!,
                LIMIT,
                lastOffset
            )

            when {
                // si la respuesta es correcta cambia el estado de la carga a loaded, guarda los trabajos y el offset
                response.isSuccessful -> {
                    val jobs = response.body()
                    _jobList.value = _jobList.value.plus(jobs?:emptyList())
                    lastOffset = jobs?.size?.let{ lastOffset + it }?:lastOffset
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