package com.fastjob.ui.viewmodels.company

import androidx.lifecycle.ViewModel
import com.fastjob.auth.AuthAPI
import com.fastjob.models.CandidateIN
import com.fastjob.ui.enums.LoadState
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow

/**
 * ViewModel para la pantalla de información de un candidato.
 */
class CandidateCardViewModel: ViewModel() {
    companion object{
        // instancia de autenticación
        val auth = AuthAPI.getInstance()
    }

    // estado de carga de la oferta
    private val _loadState = MutableStateFlow(LoadState.LOADING)
    val loadState = _loadState.asStateFlow()

    // candidato
    private val _candidate = MutableStateFlow<CandidateIN?>(null)
    val candidate = _candidate.asStateFlow()


    /**
     * Establece el estado de carga del candidato
     * @param state estado de carga
     */
    fun setLoadState(state: LoadState){
        _loadState.value = state
    }

    /**
     * Establece el candidato
     * @param candidate candidato
     */
    fun setCandidate(candidate: CandidateIN?){
        _candidate.value = candidate
    }
}