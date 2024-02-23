package com.fastjob.ui.viewmodels.profile

import androidx.lifecycle.ViewModel
import com.fastjob.auth.AuthAPI
import com.fastjob.models.CandidateIN
import com.fastjob.network.Client
import com.fastjob.services.CandidateService
import com.fastjob.ui.enums.LoadState
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow

/**
 * ViewModel para la pantalla de perfil de candidato
 */
class CandidateProfileViewModel: ViewModel() {
    companion object {
        private val candidateService = Client.getInstance().getService(CandidateService::class.java)
        val auth = AuthAPI.getInstance()
    }

    private val candidateLoadState = MutableStateFlow(LoadState.LOADING)
    val candidateLoad = candidateLoadState.asStateFlow()

    private val _candidate = MutableStateFlow<CandidateIN?>(null)
    val candidate = _candidate.asStateFlow()


    suspend fun loadCandidate(){
        if(!auth.isAuthenticated()) {
            candidateLoadState.value = LoadState.ERROR
            return
        }

        val response = candidateService.getCandidate(
            auth = auth.getToken()!!,
            id = auth.getUserId()!!,
            extraFields = emptySet()
        )

        if(response.isSuccessful){
            response.body()?.let {
                _candidate.value = it
                candidateLoadState.value = LoadState.LOADED

            } ?: run {
                candidateLoadState.value = LoadState.ERROR
            }
        } else {
            candidateLoadState.value = LoadState.ERROR
        }


    }









}