package com.fastjob.ui.viewmodels.user

import android.util.Log
import androidx.core.text.isDigitsOnly
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
 * ViewModel para actualizar los datos de un usuario
 * @param navController controlador de navegación
 */
class UpdateUserViewModel(
    currentUserData: UserData,
    val navController: NavController
): ViewModel() {
    // static
    companion object {
        private val candidateService = Client.getInstance().getService(CandidateService::class.java)
        private val companyService = Client.getInstance().getService(CompanyService::class.java)
        val auth = AuthAPI.getInstance()
    }

    // información del usuario
    private val _userData = MutableStateFlow(currentUserData)
    val userData = _userData.asStateFlow()

    // errores de los datos del usuario
    private val _userDataError = MutableStateFlow(UserDataError())
    val userDataError = _userDataError.asStateFlow()

    // visibilidad del mensaje de error
    private val _errorMessageVisibility = MutableStateFlow(false)
    val errorMessageVisibility = _errorMessageVisibility.asStateFlow()


    /**
     * Actualiza el nombre del usuario
     * @param name nombre del usuario
     */
    fun setUserName(name: String){
        _userData.value = _userData.value.copy(name = name)
    }

    /**
     * Actualiza el apellido del usuario
     * @param lastName apellido del usuario
     */
    fun setUserLastName(lastName: String){
        _userData.value = _userData.value.copy(surname = lastName)
    }

    /**
     * Actualiza el teléfono del usuario
     * @param phones teléfonos del usuario
     */
    fun setUserPhones(phones: List<String>){
        if(phones.isEmpty() || phones.all { !it.isDigitsOnly() }) return

        val intPhones = phones.map { it.toInt() }
        _userData.value = _userData.value.copy(phoneNumbers = intPhones)
    }

    /**
     * Actualiza el error de los datos del usuario
     * @param userError error de los datos del usuario
     */
    fun setDataError(userError: UserDataError){
        _userDataError.value = userError
    }

    /**
     * Actualiza la visibilidad del mensaje de error
     * @param visibility visibilidad del mensaje de error
     */
    fun setErrorVisibility(visibility: Boolean){
        _errorMessageVisibility.value = visibility
    }

    /**
     * Valida los datos del usuario y actualiza los errores y la visibilidad del mensaje de error
     */
    private fun validateUserData(){
        val name = _userData.value.name.isEmpty()
        val surname = _userData.value.surname.isEmpty()

        _userDataError.value = _userDataError.value.copy(
            name = name,
            surname = surname
        )

        _errorMessageVisibility.value = _userDataError.value.name || _userDataError.value.surname || _userDataError.value.phoneNumbers
    }

    /**
     * Actualiza los datos del usuario candidato en el servidor
     */
    fun updateCandidate(){
        // valida los datos del usuario
        validateUserData()

        // si no está autenticado o hay algún error en los datos del usuario no hace nada
        if(!auth.isAuthenticated() || userDataError.value.hasError()) return

        viewModelScope.launch(Dispatchers.IO) {
            // intenta actualizar los datos del usuario
            val response = candidateService.partialUpdateCandidate(
                auth = auth.getToken()!!,
                id = auth.getUserId()!!,
                candidate = PartialCandidateOUT(
                    user = PartialUserOUT(
                        name = userData.value.name,
                        surname = userData.value.surname,
                        phoneNumbers = userData.value.phoneNumbers
                    )
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
     * Actualiza los datos del usuario company en el servidor
     * @throws NotImplementedError
     */
    fun updateCompany(){
        // valida los datos del usuario
        validateUserData()

        // si no está autenticado o hay algún error en los datos del usuario no hace nada
        if(!auth.isAuthenticated() || userDataError.value.hasError()) return

        viewModelScope.launch(Dispatchers.IO) {
            // intenta actualizar los datos del usuario
            val response = companyService.partialUpdateCompany(
                auth = auth.getToken()!!,
                id = auth.getUserId()!!,
                company = PartialCompanyOUT(
                    user = PartialUserOUT(
                        name = userData.value.name,
                        surname = userData.value.surname,
                        phoneNumbers = userData.value.phoneNumbers
                    )
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
     * Datos de un usuario
     * @param name nombre del usuario
     * @param surname apellido del usuario
     * @param phoneNumbers teléfonos del usuario
     */
    data class UserData(
        val name: String,
        val surname: String,
        val phoneNumbers: List<Int>
    ){
        // static
        companion object{
            /**
             * Crea un objeto UserData a partir de un string
             * @param string string con los datos del usuario
             * @return objeto UserData
             */
            fun fromString(string: String): UserData {
                val data = string.split("-")
                val name = data[0]
                val surname = data[1]
                val phones = data[2].split(",").map { it.toInt() }
                return UserData(name, surname, phones)
            }
        }

        /**
         * Convierte el objeto UserData a un string
         * @return string con los datos del usuario
         */
        override fun toString(): String {
            return "$name-$surname-${phoneNumbers.joinToString(",")}"
        }
    }

    /**
     * Errores de los datos de un usuario
     * @param name indica si hay error en el nombre del usuario
     * @param surname indica si hay error en el apellido del usuario
     * @param phoneNumbers indica si hay error en los teléfonos del usuario
     */
    data class UserDataError(
        val name: Boolean = false,
        val surname: Boolean = false,
        val phoneNumbers: Boolean = false
    ){
        /**
         * Indica si hay algún error en los datos del usuario
         * @return true si hay algún error en los datos del usuario, false en caso contrario
         */
        fun hasError(): Boolean = name || surname || phoneNumbers
    }
}

class UpdateUserViewModelFactory(
    private val currentUserData: UpdateUserViewModel.UserData,
    private val navController: NavController
): ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return UpdateUserViewModel(currentUserData, navController) as T
    }
}