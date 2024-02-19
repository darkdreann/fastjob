package com.fastjob.ui.viewmodels.user

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import androidx.navigation.NavController
import com.fastjob.auth.AuthAPI
import com.fastjob.models.PartialCandidateOUT
import com.fastjob.models.PartialCompanyOUT
import com.fastjob.models.PartialUserOUT
import com.fastjob.network.Client
import com.fastjob.services.CandidateService
import com.fastjob.services.CompanyService
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

/**
 * ViewModel del formulario de actualizacion de contrasena
 */
class UpdatePasswordViewModel(
    val navController: NavController
): ViewModel() {
    companion object{
        private val candidateService = Client.getInstance().getService(CandidateService::class.java)
        private val companyService = Client.getInstance().getService(CompanyService::class.java)
        val auth = AuthAPI.getInstance()
    }

    // estado de la contrasena
    private val _password = MutableStateFlow("")
    val password = _password.asStateFlow()

    // estado del error de la contrasena
    private val _passwordError = MutableStateFlow(false)
    val passwordError = _passwordError.asStateFlow()

    // visibilidad del error de la contrasena
    private val _passwordErrorVisibility = MutableStateFlow(false)
    val passwordErrorVisibility = _passwordErrorVisibility.asStateFlow()


    /**
     * Actualiza el estado de la contrasena
     * @param password [String] contrasena
     */
    fun setPassword(password: String) {

        _password.value = password
    }

    /**
     * Actualiza el estado del error de la contrasena
     * @param passwordError [Boolean] estado del error de la contrasena
     */
    fun setPasswordError(passwordError: Boolean){
        _passwordError.value = passwordError
    }

    /**
     * Actualiza el estado de la visibilidad del error de la contrasena
     * @param passwordErrorVisibility [Boolean] estado de la visibilidad del error de la contrasena
     */
    fun setPasswordErrorVisibility(passwordErrorVisibility: Boolean) {
        _passwordErrorVisibility.value = passwordErrorVisibility
    }


    /**
     * Actualiza la contrasena del candidato
     */
    fun updateCandidatePassword() {
        // si no esta autenticado no se hace nada
        if(!auth.isAuthenticated()) return

        if(password.value.isEmpty()){
            _passwordError.value = true
            _passwordErrorVisibility.value = true
            return
        }

        viewModelScope.launch(Dispatchers.IO) {
            val response = candidateService.partialUpdateCandidate(
                auth = auth.getToken()!!,
                id = auth.getUserId()!!,
                candidate = PartialCandidateOUT(
                    user = PartialUserOUT(
                        password = password.value
                    )
                )
            )

            // si la respuesta es exitosa se actualiza la contrasena de la instancia de autenticacion
            if (response.isSuccessful) {
                auth.updatePassword(password.value)

                withContext(Dispatchers.Main){
                    navController.popBackStack()
                }

            } else {
                _passwordErrorVisibility.value = true
            }


        }


    }

    /**
     * Actualiza la contrasena de la empresa
     */
    fun updateCompanyPassword() {
        // si no esta autenticado no se hace nada
        if(!auth.isAuthenticated()) return

        if(password.value.isEmpty()){
            _passwordError.value = true
            _passwordErrorVisibility.value = true
            return
        }

        viewModelScope.launch(Dispatchers.IO) {
            val response = companyService.partialUpdateCompany(
                auth = auth.getToken()!!,
                id = auth.getUserId()!!,
                company = PartialCompanyOUT(
                    user = PartialUserOUT(
                        password = password.value
                    )
                )
            )

            // si la respuesta es exitosa se actualiza la contrasena de la instancia de autenticacion
            if (response.isSuccessful) {
                auth.updatePassword(password.value)

                withContext(Dispatchers.Main){
                    navController.popBackStack()
                }

            } else {
                _passwordErrorVisibility.value = true
            }


        }
    }

}

class UpdatePasswordViewModelFactory(
    private val navController: NavController
): ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return UpdatePasswordViewModel(navController) as T
    }
}