package com.fastjob.ui.viewmodels.company

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import androidx.navigation.NavController
import com.fastjob.auth.AuthAPI
import com.fastjob.models.LanguageWithLevelOUT
import com.fastjob.network.Client
import com.fastjob.services.JobService
import com.fastjob.ui.enums.LoadState
import com.fastjob.ui.viewmodels.candidate.CandidateLanguageViewModel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.util.UUID

/**
 * ViewModel para el formulario de idioma de la oferta de trabajo
 * @param navController NavController para la navegacion
 * @param jobId id de la oferta de trabajo
 * @param languageId id del idioma
 */
class CompanyLanguageViewModel(
    private val navController: NavController,
    private val jobId: UUID,
    private val languageId: UUID?
) : ViewModel() {
    // static
    companion object {
        private val jobService = Client.getInstance().getService(JobService::class.java)
        val auth = AuthAPI.getInstance()
    }

    // estado de carga
    private val _loadState = MutableStateFlow(LoadState.LOADING)
    val loadState = _loadState.asStateFlow()

    // language
    private val _language = MutableStateFlow(JobLanguage())
    val language = _language.asStateFlow()

    // visibilidad de error
    private val _errorVisibility = MutableStateFlow(false)
    val errorVisibility = _errorVisibility.asStateFlow()

    // error del idioma
    private val _languageError = MutableStateFlow(JobLanguageError())
    val languageError = _languageError.asStateFlow()


    /**
     * Verifica si el idioma es nuevo
     * @return true si es para crear un nuevo idioma, false si no
     */
    fun isNewLanguage(): Boolean {
        return languageId == null
    }

    /**
     * Establece el idioma
     * @param jobLanguage idioma de la oferta de trabajo
     */
    fun setLanguage(jobLanguage: JobLanguage) {
        _language.value = jobLanguage
    }


    /**
     * Establece la visibilidad del error
     * @param value valor de la visibilidad
     */
    fun setErrorVisibility(value: Boolean) {
        _errorVisibility.value = value
    }


    /**
     * Valida el idioma
     * @return true si es valido, false si no
     */
    private fun validateLanguage(): Boolean {
        _languageError.value = JobLanguageError(
            languageId = language.value.languageId == null,
            levelId = language.value.levelId == null
        )
        return !_languageError.value.hasError
    }



    /**
     * Carga el idioma
     */
    fun loadLanguage(setLanguage: (String) -> Unit) {
        if(!auth.isAuthenticated()) {
            _loadState.value = LoadState.ERROR
            return
        }

        if(languageId == null) {
            _loadState.value = LoadState.LOADED
            return
        }

        viewModelScope.launch(Dispatchers.IO){
            val response = jobService.getJobLanguage(
                auth = auth.getToken()!!,
                id = jobId,
                languageId = languageId
            )

            if(response.isSuccessful) {
                response.body()?.let {
                    _language.value = JobLanguage(
                        languageId = it.language.id,
                        languageName = it.language.name,
                        levelId = it.level.id,
                        levelName = it.level.name
                    )
                    setLanguage(it.language.name)

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
     * Guarda el idioma
     */
    fun saveLanguage() {
        if(languageId == null) createLanguage()
        else updateLanguage()
    }

    /**
     * Crea un idioma
     */
    private fun createLanguage() {
        if(!CandidateLanguageViewModel.auth.isAuthenticated()) return

        if(!validateLanguage()) {
            _errorVisibility.value = true
            return
        }

        viewModelScope.launch(Dispatchers.IO){
            val response = jobService.addJobLanguage(
                auth = CandidateLanguageViewModel.auth.getToken()!!,
                id = jobId,
                language = LanguageWithLevelOUT(
                    language = language.value.languageId!!,
                    level = language.value.levelId!!
                ),
            )

            _errorVisibility.value = !response.isSuccessful
            if(response.isSuccessful) {
                withContext(Dispatchers.Main){ navController.popBackStack() }
            }
        }
    }

    /**
     * Actualiza un idioma
     */
    private fun updateLanguage() {
        if(!auth.isAuthenticated()) return


        if(!validateLanguage()) {
            _errorVisibility.value = true
            return
        }

        viewModelScope.launch(Dispatchers.IO){
            val response = jobService.updateJobLanguage(
                auth = auth.getToken()!!,
                id = jobId,
                languageId = languageId!!,
                languageLevelId = language.value.levelId!!
            )

            _errorVisibility.value = !response.isSuccessful
            if(response.isSuccessful) {
                withContext(Dispatchers.Main){ navController.popBackStack() }
            }
        }
    }

    /**
     * Data class que representa el idioma de la oferta de trabajo
     * @param languageId id del idioma
     * @param languageName nombre del idioma
     * @param levelId id del nivel
     * @param levelName nombre del nivel
     */
    data class JobLanguage(
        val languageId: UUID? = null,
        val languageName: String = "",
        val levelId: UUID? = null,
        val levelName: String = "",
    )

    /**
     * Data class que representa el error del idioma de la oferta de trabajo
     * @param languageId error del id del idioma
     * @param levelId error del id del nivel
     */
    data class JobLanguageError(
        val languageId: Boolean = false,
        val levelId: Boolean = false,
    ){
        val hasError: Boolean
            get() = languageId || levelId
    }
}

/**
* Factory para el view model de la lista de idiomas de la oferta de trabajo
* @param navController NavController para la navegacion
 * @param jobId id de la oferta de trabajo
 * @param languageId id del idioma
*/
class CompanyLanguageViewModelFactory(
    private val navController: NavController,
    private val jobId: UUID,
    private val languageId: UUID? = null
): ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return CompanyLanguageViewModel(navController, jobId, languageId) as T
    }
}