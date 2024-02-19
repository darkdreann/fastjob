package com.fastjob.ui.viewmodels.company

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import androidx.navigation.NavController
import com.fastjob.auth.AuthAPI
import com.fastjob.models.PartialCompanyOUT
import com.fastjob.models.PartialUserOUT
import com.fastjob.network.Client
import com.fastjob.services.CompanyService
import com.fastjob.ui.viewmodels.user.CreateCompanyViewModel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

/**
 * ViewModel de la pantalla de actualización de datos de la empresa
 * @param currentCompanyData datos actuales de la empresa
 * @param navController controlador de navegación
 */
class UpdateCompanyViewModel(
    currentCompanyData: CompanyData,
    val navController: NavController
): ViewModel() {
    // static
    companion object {
        private val companyService = Client.getInstance().getService(CompanyService::class.java)
        val auth = AuthAPI.getInstance()
        val CIF_REGEX = Regex("(^[A-Z][0-9]{7}[0-9A-J]$)|(^[0-9]{8}[A-Z]$)")
    }

    // información de la empresa
    private val _companyData = MutableStateFlow(currentCompanyData)
    val companyData = _companyData.asStateFlow()

    // errores de los datos de la empresa
    private val _companyDataError = MutableStateFlow(CompanyDataError())
    val companyDataError = _companyDataError.asStateFlow()

    // visibilidad del mensaje de error
    private val _errorMessageVisibility = MutableStateFlow(false)
    val errorMessageVisibility = _errorMessageVisibility.asStateFlow()


    /**
     * Actualiza los datos de la empresa
     * @param companyData datos de la empresa
     */
    fun setCompanyData(companyData: CompanyData){
        _companyData.value = companyData
    }

    /**
     * Actualiza los errores de los datos de la empresa
     * @param companyError errores de los datos de la empresa
     */
    fun setDataError(companyError: CompanyDataError){
        _companyDataError.value = companyError
    }

    /**
     * Actualiza la visibilidad del mensaje de error
     * @param visibility visibilidad del mensaje de error
     */
    fun setErrorVisibility(visibility: Boolean){
        _errorMessageVisibility.value = visibility
    }

    /**
     * Valida los datos de la empresa y actualiza los errores
     */
    private fun validateCompanyData(){
        val tin = !_companyData.value.tin.matches(CreateCompanyViewModel.CIF_REGEX)
        val companyName = _companyData.value.companyName.isEmpty()

        _companyDataError.value = _companyDataError.value.copy(
            tin = tin,
            companyName = companyName
        )

        _errorMessageVisibility.value = tin || companyName
    }


    /**
     * Actualiza los datos de la empresa
     */
    fun updateCompany(){
        // valida los datos del usuario
        validateCompanyData()

        // si no está autenticado o hay algún error en los datos de la empresa, no hace nada
        if(!auth.isAuthenticated() || companyDataError.value.hasError()) return

        viewModelScope.launch(Dispatchers.IO) {
            // intenta actualizar los datos del usuario
            val response = companyService.partialUpdateCompany(
                auth = auth.getToken()!!,
                id = auth.getUserId()!!,
                company = PartialCompanyOUT(
                    tin = companyData.value.tin,
                    companyName = companyData.value.companyName
                )
            )

            // si la respuesta no es exitosa muestra el mensaje de error
            _errorMessageVisibility.value = !response.isSuccessful

            withContext(Dispatchers.Main){
                // si la respuesta es exitosa finaliza la pantalla actual
                if(response.isSuccessful)
                    navController.popBackStack()
            }

        }
    }

    /**
     * Datos de una empresa
     * @param tin número de identificación tributaria de la empresa
     * @param companyName nombre de la empresa
     */
    data class CompanyData(
        val tin: String,
        val companyName: String,
    )

    /**
     * Error en los datos de una empresa
     * @param tin indica si hay error en el número de identificación tributaria
     * @param companyName indica si hay error en el nombre de la empresa
     */
    data class CompanyDataError(
        val tin: Boolean = false,
        val companyName: Boolean = false,
    ){
        /**
         * Indica si hay algún error en los datos de la empresa
         * @return true si hay algún error, false en caso contrario
         */
        fun hasError(): Boolean = tin || companyName
    }
}


/**
 * Factoría para crear un ViewModel de UpdateCompanyViewModel
 * @param currentCompanyData datos actuales de la empresa
 * @param navController controlador de navegación
 */
class UpdateCompanyViewModelFactory(
    private val currentCompanyData: UpdateCompanyViewModel.CompanyData,
    private val navController: NavController
): ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return UpdateCompanyViewModel(currentCompanyData, navController) as T
    }
}