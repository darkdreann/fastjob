package com.fastjob.ui.viewmodels.search

import androidx.compose.foundation.lazy.LazyListState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.setValue
import androidx.core.text.isDigitsOnly
import androidx.lifecycle.viewModelScope
import com.fastjob.auth.AuthAPI
import com.fastjob.models.MinimalJobIN
import com.fastjob.network.Client
import com.fastjob.services.JobService
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
 * ViewModel para la busqueda de trabajos
 */
class JobSearchViewModel: SearchViewModel() {
    // static
    companion object {
        private const val LIMIT = 10
        private val jobService = Client.getInstance().getService(JobService::class.java)
        private val auth = AuthAPI.getInstance()
    }

    // keyword state
    private val _keyword = MutableStateFlow("")
    override val keyword: StateFlow<String> = _keyword.asStateFlow()

    // search state
    private val _searchState = MutableStateFlow(SearchState.START)
    override val searchState: StateFlow<SearchState> = _searchState.asStateFlow()

    // filters state
    private val _filters = MutableStateFlow(JobFilters())
    val filters: StateFlow<JobFilters> = _filters.asStateFlow()

    // search variables
    private var lastOffset by mutableIntStateOf(0)
    private val _jobList = MutableStateFlow<List<MinimalJobIN>>(emptyList())
    val jobList = _jobList.asStateFlow()

    // job list scroll
    val jobListScroll = MutableStateFlow(LazyListState())

    // job async search
    private var searchJob = MutableStateFlow<Job?>(null)

    /**
     * Cambia la palabra clave de la busqueda
     * @param keyword palabra clave
     */
    override fun setKeyword(keyword: String) {
        _keyword.value = keyword
    }

    /**
     * Cambia el estado de la busqueda
     * @param state estado de la busqueda
     */
    override fun setSearchState(state: SearchState) {
        _searchState.value = state
    }

    /**
     * Cambia el nombre de la categoria de sector
     * @param categoryName nombre de la categoria
     */
    fun setCategoryName(categoryName: String) {
        _filters.value = _filters.value.copy(sectorCategory = categoryName)
    }

    /**
     * Cambia el id de la categoria de sector
     * @param categoryId id de la categoria
     */
    fun setSectorId(sectorId: String) {
        _filters.value = _filters.value.copy(sectorId = sectorId)
    }

    /**
     * Cambia la provincia
     * @param province nombre de la provincia
     */
    fun setProvince(province: String) {
        _filters.value = _filters.value.copy(province = province)
    }

    /**
     * Cambia el nombre de la educacion
     * @param educationName nombre de la educacion
     */
    fun setEducationName(educationName: String) {
        _filters.value = _filters.value.copy(educationName = educationName)
    }

    /**
     * Cambia el id del nivel de educacion
     * @param educationLevelValue id del nivel de educacion
     */
    fun setEducationLevelValue(educationLevelValue: String) {
        _filters.value = _filters.value.copy(educationLevelValue = educationLevelValue)
    }

    /**
     * Cambia los idiomas
     * @param languages idiomas
     */
    fun setLanguages(languages: List<String>) {
        _filters.value = _filters.value.copy(languages = languages)
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
    fun getJobs() = runBlocking(Dispatchers.IO)  {
        cancelSearch() // cancela la busqueda anterior si existe

        // inicia la busqueda y guarda el job para poder cancelarlo
        searchJob.value = viewModelScope.launch(Dispatchers.IO) {
            // obtiene el token de autenticacion si existe
            val token = auth.getToken()

            // vacia la lista de trabajos y cambia el estado de la busqueda a loading
            _jobList.value = emptyList()
            _searchState.value = SearchState.LOADING

            // realiza la busqueda
            val response = jobService.getJobsMinimal(
                auth = token,
                limit = LIMIT,
                offset = 0,
                keyword = if(filters.value.sectorId.isEmpty()) keyword.value.let { it.ifEmpty { null } } else null,
                sectorCategory = filters.value.sectorCategory.let { it.ifEmpty { null } },
                sectorId = filters.value.sectorId.let { if(it.isEmpty()) null else UUID.fromString(it) },
                province = filters.value.province.let { it.ifEmpty { null } },
                educationLevel = filters.value.educationLevelValue.let { if(it.isEmpty() && it.isDigitsOnly()) null else it.toInt() },
                languages = filters.value.languages.let { if(it.isEmpty()) null else it.toSet() },
                educationName = filters.value.educationName.let { it.ifEmpty { null } }
            )

            when {
                // si la respuesta es correcta cambia el estado de la busqueda a done, guarda los trabajos y el offset
                response.isSuccessful -> {
                    val jobs = response.body()
                    _jobList.value = jobs?:emptyList()
                    lastOffset = jobs?.size?:0
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
    fun loadMoreJobs() = runBlocking(Dispatchers.IO) {
        cancelSearch() // cancela la busqueda anterior si existe

        // inicia la busqueda y guarda el job para poder cancelarlo
        searchJob.value = viewModelScope.launch(Dispatchers.IO) {
            // obtiene el token de autenticacion si existe
            val token = auth.getToken()

            // cambia el estado de la busqueda a loading
            _searchState.value = SearchState.LOADING

            // realiza la busqueda
            val response = jobService.getJobsMinimal(
                auth = token,
                limit = LIMIT,
                offset = lastOffset,
                keyword = keyword.value.let { it.ifEmpty { null } },
                sectorCategory = filters.value.sectorCategory.let { it.ifEmpty { null } },
                sectorId = filters.value.sectorId.let { if(it.isEmpty()) null else UUID.fromString(it) },
                province = filters.value.province.let { it.ifEmpty { null } },
                educationLevel = filters.value.educationLevelValue.let { if(it.isEmpty() && it.isDigitsOnly()) null else it.toInt() },
                languages = filters.value.languages.let { if(it.isEmpty()) null else it.toSet() },
                educationName = filters.value.educationName.let { it.ifEmpty { null } }
            )

            when {
                // si la respuesta es correcta cambia el estado de la busqueda a done, guarda los trabajos y el offset
                response.isSuccessful -> {
                    val jobs = response.body()
                    _jobList.value = _jobList.value.plus(jobs?:emptyList())
                    lastOffset = jobs?.size?:lastOffset
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
     * Clase que contiene los filtros de busqueda
     * @param sectorCategory categoria de sector
     * @param sectorId id del sector
     * @param province provincia
     * @param educationName nombre de la formacion
     * @param educationLevelValue id del nivel de formacion
     * @param languages idiomas
     */
    data class JobFilters(
        val sectorCategory: String = "",
        val sectorId: String = "",
        val province: String = "",
        val educationName: String = "",
        val educationLevelValue: String = "",
        val languages: List<String> = emptyList(),
    ){
        /**
         * Comprueba si todos los campos estan vacios
         * @return true si todos los campos estan vacios, false si alguno no lo esta
         */
        fun isEmpty(): Boolean {
            for (property in this::class.java.declaredFields) {
               property.get(this).let {
                   when(it) {
                       is String -> if(it.isNotEmpty()) return false
                       is List<*> -> if(it.isNotEmpty()) return false
                   }
               }
            }
            return true
        }
    }
}

