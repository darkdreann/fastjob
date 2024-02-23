package com.fastjob.ui.viewmodels.search

import androidx.compose.foundation.lazy.LazyListState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.fastjob.auth.AuthAPI
import com.fastjob.models.MinimalCandidateIN
import com.fastjob.network.Client
import com.fastjob.services.JobCandidateService
import com.fastjob.ui.functions.isDigit
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.cancelAndJoin
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking
import java.util.UUID

/**
 * ViewModel para la busqueda de candidatos
 * @param jobId id del trabajo
 */
class CandidateSearchViewModel(
    private val jobId: UUID
): SearchViewModel() {
    // static
    companion object {
        private const val LIMIT = 10
        private val jobCandidateService = Client.getInstance().getService(JobCandidateService::class.java)
        val auth = AuthAPI.getInstance()
    }

    // search state
    private val _searchState = MutableStateFlow(SearchState.START)
    override val searchState: StateFlow<SearchState> = _searchState.asStateFlow()

    // la busqueda de candidatos no usa keywords
    override val keyword: StateFlow<String>
        get() = TODO("Not yet implemented")
    override fun setKeyword(keyword: String) {
        TODO("Not yet implemented")
    }

    // filters state
    private val _filters = MutableStateFlow(CandidateFilters())
    val filters: StateFlow<CandidateFilters> = _filters.asStateFlow()

    // search variables
    private var lastOffset by mutableIntStateOf(0)
    private val _candidatesList = MutableStateFlow<List<MinimalCandidateIN>>(emptyList())
    val candidatesList = _candidatesList.asStateFlow()

    // job list scroll
    val jobListScroll = MutableStateFlow(LazyListState())

    // job async search
    private var searchJob = MutableStateFlow<Job?>(null)


    /**
     * Obtiene el id del trabajo
     * @return id del trabajo
     */
    fun getJobId(): UUID {
        return jobId
    }

    /**
     * Cambia el estado de la busqueda
     * @param state estado de la busqueda
     */
    override fun setSearchState(state: SearchState) {
        _searchState.value = state
    }

    /**
     * Cambia los filtros
     * @param candidateFilters filtros
     */
    fun setCandidateFilters(candidateFilters: CandidateFilters){
        _filters.value = candidateFilters
    }

    /**
     * Cancela la busqueda si esta activa
     */
    private suspend fun cancelSearch() {
        searchJob.value?.let {
            if(it.isActive) {
                it.cancelAndJoin()
                _searchState.value = SearchState.CANCELLED
            }
        }
    }

    /**
     * Realiza una busqueda de trabajos
     */
    fun getCandidates() = runBlocking(Dispatchers.IO)  {
        if(!auth.isAuthenticated()) return@runBlocking

        cancelSearch() // cancela la busqueda anterior si existe

        // inicia la busqueda y guarda el job para poder cancelarlo
        searchJob.value = viewModelScope.launch(Dispatchers.IO) {
            // obtiene el token de autenticacion si existe
            val token = auth.getToken()

            // vacia la lista de trabajos y cambia el estado de la busqueda a loading
            _candidatesList.value = emptyList()
            _searchState.value = SearchState.LOADING

            // sector
            val sector = filters.value.sectorId.ifEmpty { filters.value.sectorCategory.ifEmpty { null } }

            // realiza la busqueda
            val response = jobCandidateService.getJobCandidatesMinimal(
                auth = token!!,
                jobId = jobId,
                limit = LIMIT,
                offset = 0,
                postalCode = if(filters.value.address.isDigit() && filters.value.address.length == 5) filters.value.address.toInt() else null,
                province = if(!filters.value.address.isDigit()) filters.value.address else null,
                experienceMonths = if(filters.value.experienceMonths.isDigit()) filters.value.experienceMonths.toInt() else null,
                experienceSector = sector,
                language = filters.value.languages.ifEmpty { null },
                languageLevel = if(filters.value.languages.isNotEmpty() && filters.value.languageLevel.isDigit()) filters.value.languageLevel.toInt() else null,
                educationName = filters.value.educationName.ifEmpty { null },
                educationLevel = if(filters.value.educationName.isEmpty() && filters.value.educationLevelValue.isDigit()) filters.value.educationLevelValue.toInt() else null,
                educationSector = if(filters.value.educationName.isEmpty()) sector else null,
                skills = filters.value.skills.ifEmpty { null },
                availability = filters.value.availability.ifEmpty { null }
            )


            when {
                // si la respuesta es correcta cambia el estado de la busqueda a done, guarda los trabajos y el offset
                response.isSuccessful -> {
                    val candidates = response.body()
                    _candidatesList.value = candidates?:emptyList()
                    lastOffset = candidates?.size?:0
                    _searchState.value = SearchState.DONE
                }
                // si la respuesta es 404 cambia el estado de la busqueda a not found
                response.code() == 404 -> {
                    _searchState.value = SearchState.NOT_FOUND
                }
                // si la respuesta es otra cambia el estado de la busqueda a error
                else -> {
                    _searchState.value = SearchState.ERROR
                }
            }
        }
    }

    /**
     * Carga mas trabajos en la lista
     */
    fun loadMoreCandidates() = runBlocking(Dispatchers.IO) {
        if(!auth.isAuthenticated()) return@runBlocking

        cancelSearch() // cancela la busqueda anterior si existe

        // inicia la busqueda y guarda el job para poder cancelarlo
        searchJob.value = viewModelScope.launch(Dispatchers.IO) {
            // obtiene el token de autenticacion si existe
            val token = auth.getToken()

            // cambia el estado de la busqueda a loading
            _searchState.value = SearchState.LOADING

            // sector
            val sector = filters.value.sectorId.ifEmpty { filters.value.sectorCategory.ifEmpty { null } }

            // realiza la busqueda
            val response = jobCandidateService.getJobCandidatesMinimal(
                auth = token!!,
                jobId = jobId,
                limit = LIMIT,
                offset = lastOffset,
                postalCode = if(filters.value.address.isDigit() && filters.value.address.length == 5) filters.value.address.toInt() else null,
                province = if(!filters.value.address.isDigit()) filters.value.address else null,
                experienceMonths = if(filters.value.experienceMonths.isDigit()) filters.value.experienceMonths.toInt() else null,
                experienceSector = sector,
                language = filters.value.languages.ifEmpty { null },
                languageLevel = if(filters.value.languages.isNotEmpty() && filters.value.languageLevel.isDigit()) filters.value.languageLevel.toInt() else null,
                educationName = filters.value.educationName.ifEmpty { null },
                educationLevel = if(filters.value.educationName.isEmpty() && filters.value.educationLevelValue.isDigit()) filters.value.educationLevelValue.toInt() else null,
                educationSector = if(filters.value.educationName.isEmpty()) sector else null,
                skills = filters.value.skills.ifEmpty { null },
                availability = filters.value.availability.ifEmpty { null }
            )

            when {
                // si la respuesta es correcta cambia el estado de la busqueda a done, guarda los trabajos y el offset
                response.isSuccessful -> {
                    val candidates = response.body()
                    _candidatesList.value = _candidatesList.value.plus(candidates?:emptyList())
                    lastOffset = candidates?.size?:lastOffset
                    _searchState.value = SearchState.DONE
                }
                // si la respuesta es 404 cambia el estado de la busqueda a end of list
                response.code() == 404 -> _searchState.value = SearchState.END_OF_LIST
                // si la respuesta es otra cambia el estado de la busqueda a error
                else -> {
                    _searchState.value = SearchState.ERROR
                }
            }
        }
    }


    /**
     * Filtros para buscar candidatos.
     */
    data class CandidateFilters(
        val address: String = "",
        val experienceMonths: String = "",
        val sectorCategory: String = "",
        val sectorId: String = "",
        val educationName: String = "",
        val educationLevelValue: String = "",
        val languages: String = "",
        val languageLevel: String = "",
        val skills: Set<String> = emptySet(),
        val availability: String = ""
    )
}

/**
 * Factory para el ViewModel
 * @param jobId id del trabajo
 */
class CandidateSearchViewModelFactory(
    private val jobId: UUID
): ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return CandidateSearchViewModel(jobId) as T
    }
}