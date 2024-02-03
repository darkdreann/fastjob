package com.fastjob.ui.viewmodels.form.user

import androidx.core.text.isDigitsOnly
import androidx.lifecycle.ViewModel
import com.fastjob.models.AddressOUT
import com.fastjob.models.UserOUT
import com.fastjob.ui.viewmodels.interfaces.AddressForm
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

/**
 * ViewModel para el formulario de creación de usuarios
 * @property userData MutableStateFlow<UserOUT> flujo de datos del usuario
 * @property userError MutableStateFlow<UserError> flujo de datos de los errores del usuario
 */
open class CreateUserViewModel: ViewModel(), AddressForm {

    // estado de la dirección
    private val _userAddress = MutableStateFlow(AddressOUT(
        postalCode = 0,
        province = "",
        city = "",
        street = ""
    ))
    override val address = _userAddress.asStateFlow()

    // user data state
    private val _userData = MutableStateFlow(UserOUT(
        username = "",
        email = "",
        name = "",
        surname = "",
        password = "",
        phoneNumbers = emptyList(),
        address = _userAddress.value
    ))
    val userData: StateFlow<UserOUT> = _userData.asStateFlow()

    // user error state
    private val _userError = MutableStateFlow(UserError())
    val userError: StateFlow<UserError> = _userError.asStateFlow()

    /**
     * Establece el nombre de usuario
     * @param username String nombre de usuario
     */
    fun setUsername(username: String) {
        _userData.value = _userData.value.copy(username = username)
    }

    /**
     * Establece el email
     * @param email String email
     */
    fun setEmail(email: String) {
        _userData.value = _userData.value.copy(email = email)
    }

    /**
     * Establece el nombre
     * @param name String nombre
     */
    fun setName(name: String) {
        _userData.value = _userData.value.copy(name = name)
    }

    /**
     * Establece el apellido
     * @param surname String apellido
     */
    fun setSurname(surname: String) {
        _userData.value = _userData.value.copy(surname = surname)
    }

    /**
     * Establece la contraseña
     * @param password String contraseña
     */
    fun setPassword(password: String) {
        _userData.value = _userData.value.copy(password = password)
    }

    /**
     * Establece los números de teléfono
     * @param phoneNumbers List<String> números de teléfono
     */
    fun setPhoneNumbers(phoneNumbers: List<String>) {
        if (phoneNumbers.any { it.isEmpty() || !it.isDigitsOnly() }) return

        val phoneNumbersInt = phoneNumbers.map { it.toInt() }
        _userData.value = _userData.value.copy(phoneNumbers = phoneNumbersInt)
    }

    /**
     * Establece el código postal
     * @param postalCode String código postal
     */
    override fun setAddressPostalCode(postalCode: String) {
        if (postalCode.isEmpty() || !postalCode.isDigitsOnly()) return

        val postalCodeInt = postalCode.toInt()
        _userData.value = _userData.value.copy(address = _userData.value.address.copy(postalCode = postalCodeInt))
    }

    /**
     * Establece la provincia
     * @param province String provincia
     */
    override fun setAddressProvince(province: String) {
        _userData.value = _userData.value.copy(address = _userData.value.address.copy(province = province))
    }

    /**
     * Establece la ciudad
     * @param city String ciudad
     */
    override fun setAddressCity(city: String) {
        _userData.value = _userData.value.copy(address = _userData.value.address.copy(city = city))
    }

    /**
     * Establece la calle
     * @param street String calle
     */
    override fun setAddressStreet(street: String) {
        _userData.value = _userData.value.copy(address = _userData.value.address.copy(street = street))
    }

    /**
     * Establece los errores del usuario
     * @param userError UserError errores del usuario
     */
    fun setErrorUserData(userError: UserError) {
        _userError.value = userError
    }

    /**
     * Comprueba que los campos no estén vacíos
     * Si los campos están vacíos se establece el error correspondiente
     */
    protected fun checkUserDataEmpty(){
        // establecer la dirección del usuario
        _userData.value = _userData.value.copy(address = _userAddress.value)

        // comprobar que los campos no estén vacíos
        if(userData.value.username.isEmpty()) _userError.value = _userError.value.copy(username = true)
        if(userData.value.email.isEmpty()) _userError.value = _userError.value.copy(email = true)
        if(userData.value.name.isEmpty()) _userError.value = _userError.value.copy(name = true)
        if(userData.value.surname.isEmpty()) _userError.value = _userError.value.copy(surname = true)
        if(userData.value.password.isEmpty()) _userError.value = _userError.value.copy(password = true)
        // comprobar que los campos de la dirección no estén vacíos
        if(userData.value.address.postalCode == 0 || userData.value.address.province.isEmpty() || userData.value.address.city.isEmpty() || userData.value.address.street.isEmpty())
            _userError.value = _userError.value.copy(address = true)
    }

    /**
     * Clase que representa los errores del usuario
     * @property username Boolean indica si el nombre de usuario es válido
     * @property email Boolean indica si el email es válido
     * @property name Boolean indica si el nombre es válido
     * @property surname Boolean indica si el apellido es válido
     * @property password Boolean indica si la contraseña es válida
     * @property phoneNumbers Boolean indica si los números de teléfono son válidos
     * @property address Boolean indica si la dirección es válida
     */
    data class UserError(
        val username: Boolean = false,
        val email: Boolean = false,
        val name: Boolean = false,
        val surname: Boolean = false,
        val password: Boolean = false,
        val phoneNumbers: Boolean = false,
        val address:Boolean = false
    ){
        /**
         * Indica si hay algún error
         * @return Boolean true si hay algún error, false en caso contrario
         */
        fun anyTrue(): Boolean {
            return username || email || name || surname || password || phoneNumbers || address
        }
    }

}


