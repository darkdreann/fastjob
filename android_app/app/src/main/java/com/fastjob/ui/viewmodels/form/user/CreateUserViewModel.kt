package com.fastjob.ui.viewmodels.form.user

import androidx.core.text.isDigitsOnly
import androidx.lifecycle.ViewModel
import com.fastjob.models.AddressOUT
import com.fastjob.models.UserOUT
import com.fastjob.ui.functions.isEmail
import com.fastjob.ui.functions.isPasswordSecure
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

open class CreateUserViewModel: ViewModel() {
    // user data state
    private val _userData = MutableStateFlow(UserOUT(
        username = "",
        email = "",
        name = "",
        surname = "",
        password = "",
        phoneNumbers = emptyList(),
        address = AddressOUT(
            postalCode = 0,
            province = "",
            city = "",
            street = ""
        )
    ))
    val userData: StateFlow<UserOUT> = _userData.asStateFlow()

    // user error state
    private val _userError = MutableStateFlow(UserError())
    val userError: StateFlow<UserError> = _userError.asStateFlow()

    fun setUsername(username: String) {
        _userData.value = _userData.value.copy(username = username)
    }

    fun setEmail(email: String) {
        _userData.value = _userData.value.copy(email = email)
    }

    fun setName(name: String) {
        _userData.value = _userData.value.copy(name = name)
    }

    fun setSurname(surname: String) {
        _userData.value = _userData.value.copy(surname = surname)
    }

    fun setPassword(password: String) {
        _userData.value = _userData.value.copy(password = password)
    }

    fun setPhoneNumbers(phoneNumbers: List<String>) {
        if (phoneNumbers.any { it.isEmpty() || !it.isDigitsOnly() }) return

        val phoneNumbersInt = phoneNumbers.map { it.toInt() }
        _userData.value = _userData.value.copy(phoneNumbers = phoneNumbersInt)
    }

    fun setAddressPostalCode(postalCode: String) {
        if (postalCode.isEmpty() || !postalCode.isDigitsOnly()) return

        val postalCodeInt = postalCode.toInt()
        _userData.value = _userData.value.copy(address = _userData.value.address.copy(postalCode = postalCodeInt))
    }

    fun setAddressProvince(province: String) {
        _userData.value = _userData.value.copy(address = _userData.value.address.copy(province = province))
    }

    fun setAddressCity(city: String) {
        _userData.value = _userData.value.copy(address = _userData.value.address.copy(city = city))
    }

    fun setAddressStreet(street: String) {
        _userData.value = _userData.value.copy(address = _userData.value.address.copy(street = street))
    }

    fun setErrorUserData(userError: UserError) {
        _userError.value = userError
    }

    data class UserError(
        val username: Boolean = true,
        val email: Boolean = true,
        val name: Boolean = true,
        val surname: Boolean = true,
        val password: Boolean = true,
        val phoneNumbers: Boolean = true,
        val address:Boolean = true
    ){
        fun anyTrue(): Boolean {
            return username || email || name || surname || password || phoneNumbers || address
        }
    }

}


