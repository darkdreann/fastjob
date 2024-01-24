package com.fastjob.ui.viewmodels.form.user

import android.util.Log
import androidx.compose.runtime.collectAsState
import androidx.lifecycle.viewModelScope
import com.fastjob.models.Availability
import com.fastjob.models.CandidateOUT
import com.fastjob.network.Client
import com.fastjob.services.CandidateService
import com.fastjob.ui.enums.RegisterState
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class CreateCandidateViewModel: CreateUserViewModel() {
    companion object {
        private val candidateService = Client.getInstance().getService(CandidateService::class.java)
    }

    // register state
    private val _registerState = MutableStateFlow(RegisterState.NOT_POSTED)
    val registerState = _registerState.asStateFlow()

    // candidate data state
    private val _candidateData = MutableStateFlow(
        CandidateOUT(
            skills = emptyList(),
            availabilities = emptyList(),
            user = userData.value
        )
    )
    val candidateData = _candidateData.asStateFlow()


    fun setSkills(skills: List<String>) {
        _candidateData.value = _candidateData.value.copy(skills = skills)
    }

    fun setAvailabilities(availabilities: Set<Availability>) {
        _candidateData.value = _candidateData.value.copy(availabilities = availabilities.toList())
    }


    fun registerCandidate() {
        if(userError.value.anyTrue()) {
            _registerState.value = RegisterState.FORM_NOT_VALID
            return
        }

        _candidateData.value = _candidateData.value.copy(user = userData.value)

        viewModelScope.launch(Dispatchers.IO) {
            val response = candidateService.createCandidate(candidateData.value)

            when(response.code()) {
                201 -> _registerState.value = RegisterState.REGISTERED
                409 -> {
                    if(response.errorBody()?.string()?.contains("email") == false) {
                        _registerState.value = RegisterState.DUPLICATED_USERNAME
                    }else{
                        _registerState.value = RegisterState.DUPLICATED_EMAIL
                    }
                }
                else -> _registerState.value = RegisterState.UNKNOWN_ERROR
            }
        }
    }
}