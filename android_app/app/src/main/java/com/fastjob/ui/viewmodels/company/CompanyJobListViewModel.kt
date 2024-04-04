package com.fastjob.ui.viewmodels.company

import android.util.Log
import androidx.compose.foundation.lazy.LazyListState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.fastjob.auth.AuthAPI
import com.fastjob.models.MinimalJobIN
import com.fastjob.network.Client
import com.fastjob.services.CompanyService
import com.fastjob.services.JobService
import com.fastjob.ui.enums.LoadState
import com.fastjob.ui.viewmodels.candidate.EducationListViewModel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.cancelAndJoin
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking
import java.util.UUID


/**
 * ViewModel para la lista de ofertas de trabajo creadas por la empresa
 */
class CompanyJobListViewModel: ViewModel() {
    // static
    companion object {
        private const val LIMIT = 10
        private val companyService = Client.getInstance().getService(CompanyService::class.java)
        private val jobService = Client.getInstance().getService(JobService::class.java)
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
     * Cancela la actualizacion de la lista de ofertas
     */
    private suspend fun cancelSearch() {
        updateListJob.value?.let {
            if(it.isActive) {
                it.cancelAndJoin()
            }
        }
    }

    /**
     * Obtiene las ofertas de trabajo creadas por la empresa
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

            // realiza la petición de las ofertas de trabajo creadas por la empresa
            val response = companyService.getCompanyJobs(
                auth.getToken()!!,
                auth.getUserId()!!,
                LIMIT,
                0
            )

            when {
                // si la respuesta es correcta cambia el estado de la carga a loaded, guarda las ofertas y el offset
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

            when {
                // si la respuesta es correcta cambia el estado de la carga a loaded, guarda las ofertas y el offset
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
     * Carga mas ofertas de trabajo creadas por la empresa
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



            // realiza la carga de mas ofertas de trabajo creadas por la empresa
            val response = companyService.getCompanyJobs(
                auth.getToken()!!,
                auth.getUserId()!!,
                LIMIT,
                lastOffset
            )



            when {
                // si la respuesta es correcta cambia el estado de la carga a loaded, guarda las ofertas y el offset
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

    /**
     * Elimina una oferta de trabajo
     * @param id Identificador de la oferta de trabajo
     */
    fun deleteJob(id: UUID){
        // si no esta autenticado no hace nada
        if(!auth.isAuthenticated()) return

        viewModelScope.launch(Dispatchers.IO) {
            // realiza la petición para eliminar la oferta de trabajo
            val response = jobService.deleteJob(
                auth = EducationListViewModel.auth.getToken()!!,
                id = id
            )

            // si la respuesta es correcta elimina la oferta de trabajo de la lista
            if(response.isSuccessful){
                lastOffset--
                _jobList.value = _jobList.value.filter { it.id != id }
            }
        }
    }


}