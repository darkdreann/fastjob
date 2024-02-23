package com.fastjob.ui.viewmodels.user

import androidx.lifecycle.viewModelScope
import com.fastjob.models.CompanyOUT
import com.fastjob.network.Client
import com.fastjob.services.CompanyService
import com.fastjob.ui.enums.RegisterState
import com.fastjob.ui.viewmodels.user.CreateCompanyViewModel.Companion.companyService
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

/**
 * ViewModel para el registro de una empresa
 * @property companyService servicio de empresas
 */
class CreateCompanyViewModel: CreateUserViewModel() {
    companion object {
        private val companyService = Client.getInstance().getService(CompanyService::class.java)
        val CIF_REGEX = Regex("(^[A-Z][0-9]{7}[0-9A-J]$)|(^[0-9]{8}[A-Z]$)")
    }

    // register state
    private val _registerState = MutableStateFlow(RegisterState.NOT_POSTED)
    val registerState = _registerState.asStateFlow()

    // error visibility state
    private val _errorVisibility = MutableStateFlow(false)
    val errorVisibility = _errorVisibility.asStateFlow()

    // company data state
    private val _companyData = MutableStateFlow(
        CompanyOUT(
            tin = "",
            companyName = "",
            user = userData.value
        )
    )
    val companyData = _companyData.asStateFlow()

    // company error state
    private val _companyError = MutableStateFlow(CompanyError())
    val companyError = _companyError.asStateFlow()


    /**
     * Establece el CIF de la empresa
     * @param tin String CIF
     */
    fun setTin(tin: String) {
        _companyData.value = _companyData.value.copy(tin = tin)
    }

    /**
     * Establece el nombre de la empresa
     * @param companyName String nombre de la empresa
     */
    fun setCompanyName(companyName: String) {
        _companyData.value = _companyData.value.copy(companyName = companyName)
    }

    /**
     * Establece el error de los datos de la empresa
     * @param error CompanyError error
     */
    fun setCompanyError(error: CompanyError) {
        _companyError.value = error
    }

    /**
     * Establece la visibilidad del dialogo de error
     * @param visibility Boolean visibilidad
     */
    fun setErrorVisibility(visibility: Boolean) {
        _errorVisibility.value = visibility
    }

    /**
     * Comprueba si los datos de la empresa son validos
     */
    private fun checkCompanyDataEmpty() {
        checkUserDataEmpty()
        _companyError.value = _companyError.value.copy(
            tin = !companyData.value.tin.matches(CIF_REGEX),
            companyName = companyData.value.companyName.isEmpty()
        )
    }

    /**
     * Registra una empresa en la base de datos si los datos son válidos
     */
    fun registerCompany() {
        checkCompanyDataEmpty()
        // si hay algún error en los datos del usuario, no se registra
        if(userError.value.anyTrue() || companyError.value.anyTrue()) {
            // mostrar error en el formulario y terminar la función
            _registerState.value = RegisterState.FORM_NOT_VALID
            return
        }

        // establecer el usuario de la empresa
        _companyData.value = _companyData.value.copy(user = userData.value)

        // registrar el candidato de forma asíncrona con dispatchers IO
        viewModelScope.launch(Dispatchers.IO) {
            val response = companyService.createCompany(companyData.value)
            

            _errorVisibility.value = !response.isSuccessful
            // comprobar el código de respuesta
            when(response.code()) {
                // si el registro es correcto, establecer el estado del registro a REGISTERED
                201 -> _registerState.value = RegisterState.REGISTERED
                // si el nombre de usuario o el email ya existen, establecer el estado del registro a DUPLICATED_USERNAME o DUPLICATED_EMAIL
                409 -> {
                    if(response.errorBody()?.string()?.contains("email") == false) {
                        _registerState.value = RegisterState.DUPLICATED_USERNAME
                    }else{
                        _registerState.value = RegisterState.DUPLICATED_EMAIL
                    }
                }
                // si ha ocurrido un error desconocido, establecer el estado del registro a UNKNOWN_ERROR
                else -> _registerState.value = RegisterState.UNKNOWN_ERROR
            }
        }
    }

    /**
     * Clase que representa los errores de los datos de la empresa
     * @property tin Boolean error del CIF
     * @property companyName Boolean error del nombre de la empresa
     */
    data class CompanyError(
        val tin: Boolean = false,
        val companyName: Boolean = false
    ){
        fun anyTrue() = tin || companyName
    }


}