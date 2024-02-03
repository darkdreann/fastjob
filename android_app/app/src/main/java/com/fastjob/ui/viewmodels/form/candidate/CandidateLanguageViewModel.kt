package com.fastjob.ui.viewmodels.form.candidate

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import androidx.navigation.NavController
import com.fastjob.auth.AuthAPI
import com.fastjob.models.LanguageWithLevelOUT
import com.fastjob.network.Client
import com.fastjob.services.CandidateLanguageService
import com.fastjob.ui.enums.LoadState
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.util.UUID

/**
 * ViewModel para el formulario de idioma del candidato
 * @param navController NavController para la navegacion
 * @param id id del idioma
 */
class CandidateLanguageViewModel(
    private val navController: NavController,
    private val id: UUID? = null
) : ViewModel() {
    // static
    companion object {
        private val candidateLanguageService = Client.getInstance().getService(CandidateLanguageService::class.java)
        val auth = AuthAPI.getInstance()
    }

    // estado de carga
    private val _loadState = MutableStateFlow(LoadState.LOADING)
    val loadState = _loadState.asStateFlow()

    // language
    private val _language = MutableStateFlow(CandidateLanguage())
    val language = _language.asStateFlow()

    // visibilidad de error
    private val _errorVisibility = MutableStateFlow(false)
    val errorVisibility = _errorVisibility.asStateFlow()

    // error del idioma
    private val _languageError = MutableStateFlow(CandidateLanguageError())
    val languageError = _languageError.asStateFlow()


    /**
     * Verifica si el idioma es nuevo
     * @return true si es para crear un nuevo idioma, false si no
     */
    fun isNewLanguage(): Boolean {
        return id == null
    }

    /**
     * Establece el idioma
     * @param candidateLanguage idioma del candidato
     */
    fun setLanguage(candidateLanguage: CandidateLanguage) {
        _language.value = candidateLanguage
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
        _languageError.value = CandidateLanguageError(
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

        if(id == null) {
            _loadState.value = LoadState.LOADED
            return
        }

        viewModelScope.launch(Dispatchers.IO){
            val response = candidateLanguageService.getCandidateLanguage(
                auth = auth.getToken()!!,
                candidateId = auth.getUserId()!!,
                id = id
            )

            if(response.isSuccessful) {
                response.body()?.let {
                    _language.value = CandidateLanguage(
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
        if(id == null) createLanguage()
        else updateEducation()
    }

    /**
     * Crea un idioma
     */
    private fun createLanguage() {
        if(!auth.isAuthenticated()) return

        if(!validateLanguage()) {
            _errorVisibility.value = true
            return
        }

        viewModelScope.launch(Dispatchers.IO){
            val response = candidateLanguageService.createCandidateLanguages(
                auth = auth.getToken()!!,
                candidateId = auth.getUserId()!!,
                language = LanguageWithLevelOUT(
                    language = language.value.languageId!!,
                    level = language.value.levelId!!
                )
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
    private fun updateEducation() {
        if(!auth.isAuthenticated() || id == null) return

        if(!validateLanguage()) {
            _errorVisibility.value = true
            return
        }

        viewModelScope.launch(Dispatchers.IO){
            val response = candidateLanguageService.updateCandidateLanguages(
                auth = auth.getToken()!!,
                candidateId = auth.getUserId()!!,
                id = id,
                languageLevelId = language.value.levelId!!
            )

            _errorVisibility.value = !response.isSuccessful
            if(response.isSuccessful) {
                withContext(Dispatchers.Main){ navController.popBackStack() }
            }
        }
    }

    /**
     * Data class que representa el idioma del candidato
     * @param languageId id del idioma
     * @param languageName nombre del idioma
     * @param levelId id del nivel
     * @param levelName nombre del nivel
     */
    data class CandidateLanguage(
        val languageId: UUID? = null,
        val languageName: String = "",
        val levelId: UUID? = null,
        val levelName: String = "",
    )

    /**
     * Data class que representa el error del idioma del candidato
     * @param languageId error del id del idioma
     * @param levelId error del id del nivel
     */
    data class CandidateLanguageError(
        val languageId: Boolean = false,
        val levelId: Boolean = false,
    ){
        val hasError: Boolean
            get() = languageId || levelId
    }
}

/**
* Factory para el view model de la lista de idiomas del candidato
* @param navController NavController para la navegacion
* @param id id del idioma
*/
class CandidateLanguageViewModelFactory(
    private val navController: NavController,
    private val id: UUID? = null
): ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return CandidateLanguageViewModel(navController, id) as T
    }
}