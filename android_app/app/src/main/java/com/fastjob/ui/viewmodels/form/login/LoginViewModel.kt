package com.fastjob.ui.viewmodels.form.login

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.fastjob.auth.AuthAPI
import com.fastjob.models.UserType
import com.fastjob.ui.enums.LoginState
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

/**
 * ViewModel de la pantalla de login
 */
class LoginViewModel: ViewModel() {

    companion object{
        val auth = AuthAPI.getInstance()
    }

    // estado del login
    private val _loginState = MutableStateFlow(LoginState.NOT_LOGGED)
    val loginState = _loginState.asStateFlow()

    // estado del username
    private val _username = MutableStateFlow("")
    val username = _username.asStateFlow()

    // estado del password
    private val _password = MutableStateFlow("")
    val password = _password.asStateFlow()

    // estado de error del username
    private val _usernameError = MutableStateFlow(false)
    val usernameError = _usernameError.asStateFlow()

    // estado de error del password
    private val _passwordError = MutableStateFlow(false)
    val passwordError = _passwordError.asStateFlow()

    // estado visibilidad error
    private val _errorVisibility = MutableStateFlow(false)
    val errorVisibility = _errorVisibility.asStateFlow()

    /**
     * Establece el username
     * @param username username
     */
    fun setUsername(username: String) {
        _username.value = username
    }

    /**
     * Establece el password
     * @param password password
     */
    fun setPassword(password: String) {
        _password.value = password
    }

    /**
     * Establece el estado del login
     * @param state estado del login
     */
    fun setUsernameError(error: Boolean) {
        _usernameError.value = error
    }

    /**
     * Establece el estado del login
     * @param state estado del login
     */
    fun setPasswordError(error: Boolean) {
        _passwordError.value = error
    }

    /**
     * Establece el estado del login
     * @param state estado del login
     */
    fun setErrorVisibility(visibility: Boolean) {
        _errorVisibility.value = visibility
    }

    /**
     * Realiza el login del usuario con las credenciales establecidas
     */
    fun login() {
        viewModelScope.launch {
            val loginResult = auth.login(username.value, password.value, saveCredentials = true)

            // si el login es exitoso, navegar a la pantalla de búsqueda de empleo
            if(loginResult){
                // si el usuario es admin, mostrar un dialogo de error
                if(auth.getUserType() == UserType.ADMIN) _errorVisibility.value = true
                _loginState.value = LoginState.SUCCESS

            } else {
                // si el login falla, mostrar un dialogo de error
                _loginState.value = LoginState.ERROR
                _usernameError.value = true
                _passwordError.value = true
                _errorVisibility.value = true
            }
        }
    }
}