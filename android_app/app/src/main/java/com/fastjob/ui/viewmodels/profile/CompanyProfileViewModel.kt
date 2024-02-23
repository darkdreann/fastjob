package com.fastjob.ui.viewmodels.profile

import androidx.lifecycle.ViewModel
import com.fastjob.auth.AuthAPI
import com.fastjob.models.CompanyIN
import com.fastjob.network.Client
import com.fastjob.services.CompanyService
import com.fastjob.ui.enums.LoadState
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow

/**
 * ViewModel para la pantalla de perfil de empresa
 */
class CompanyProfileViewModel: ViewModel() {
    companion object {
        private val companyService = Client.getInstance().getService(CompanyService::class.java)
        val auth = AuthAPI.getInstance()
    }

    private val _companyLoadState = MutableStateFlow(LoadState.LOADING)
    val companyLoadState = _companyLoadState.asStateFlow()

    private val _company = MutableStateFlow<CompanyIN?>(null)
    val company = _company.asStateFlow()


    suspend fun loadCompany(){
        if(!auth.isAuthenticated()) {
            _companyLoadState.value = LoadState.ERROR
            return
        }

        val response = companyService.getCompany(
            auth = auth.getToken()!!,
            id = auth.getUserId()!!
        )

        if(response.isSuccessful){
            response.body()?.let {
                _company.value = it
                _companyLoadState.value = LoadState.LOADED

            } ?: run {
                _companyLoadState.value = LoadState.ERROR
            }
        } else {
            _companyLoadState.value = LoadState.ERROR
        }


    }









}