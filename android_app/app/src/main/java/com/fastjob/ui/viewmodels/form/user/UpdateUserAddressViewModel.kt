package com.fastjob.ui.viewmodels.form.user

import android.util.Log
import androidx.core.text.isDigitsOnly
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import androidx.navigation.NavController
import com.fastjob.auth.AuthAPI
import com.fastjob.models.AddressOUT
import com.fastjob.models.PartialCandidateOUT
import com.fastjob.models.PartialUserOUT
import com.fastjob.network.Client
import com.fastjob.services.CandidateService
import com.fastjob.services.CompanyService
import com.fastjob.ui.viewmodels.interfaces.AddressForm
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

/**
 * ViewModel para actualizar la dirección de un usuario
 * @param navController [NavController] controlador de navegación
 */
class UpdateUserAddressViewModel(
    val navController: NavController,
    currentAddress: Address
): ViewModel(), AddressForm {

    // static
    companion object{
        private val candidateService = Client.getInstance().getService(CandidateService::class.java)
        private val companyService = Client.getInstance().getService(CompanyService::class.java)
        val auth = AuthAPI.getInstance()
    }

    private val _address = MutableStateFlow(AddressOUT(
        postalCode = currentAddress.postalCode.toInt(),
        province = currentAddress.province,
        city = currentAddress.city,
        street = currentAddress.street
    ))
    override val address = _address.asStateFlow()

    // estado de error del formulario
    private val _addressError = MutableStateFlow(false)
    val addressError = _addressError.asStateFlow()

    // estado visibilidad del error
    private val _addressErrorVisibility = MutableStateFlow(false)
    val addressErrorVisibility = _addressErrorVisibility.asStateFlow()


    /**
     * Actualiza el código postal de la dirección
     * @param postalCode [String] código postal
     */
    override fun setAddressPostalCode(postalCode: String) {
        if (postalCode.isEmpty() || !postalCode.isDigitsOnly()) return
        _address.value = _address.value.copy(postalCode = postalCode.toInt())
    }

    /**
     * Actualiza la provincia de la dirección
     * @param province [String] provincia
     */
    override fun setAddressProvince(province: String) {
        _address.value = _address.value.copy(province = province)
    }

    /**
     * Actualiza la ciudad de la dirección
     * @param city [String] ciudad
     */
    override fun setAddressCity(city: String) {
        _address.value = _address.value.copy(city = city)
    }

    /**
     * Actualiza la calle de la dirección
     * @param street [String] calle
     */
    override fun setAddressStreet(street: String) {
        _address.value = _address.value.copy(street = street)
    }

    /**
     * Actualiza el estado de error del formulario
     * @param value [Boolean] estado de error
     */
    fun setErrorUserData(value: Boolean) {
        _addressError.value = value
    }

    /**
     * Actualiza el estado de visibilidad del error
     * @param value [Boolean] estado de visibilidad
     */
    fun setErrorUserDataVisibility(value: Boolean) {
        _addressErrorVisibility.value = value
    }

    /**
     * Valida la dirección
     * @return [Boolean] estado de la validación
     */
    private fun validateAddress(): Boolean {
        (_address.value.postalCode !in 10000..99999)
            .and(_address.value.province.isNotEmpty())
            .and(_address.value.city.isNotEmpty())
            .and(_address.value.street.isNotEmpty())
            .let {
                _addressError.value = it
                _addressErrorVisibility.value = it
                return it
            }
    }

    /**
     * Actualiza la dirección del candidato en el servidor
     */
    fun updateCandidateAddress() {
        // si no está autenticado o la dirección no es válida, no se actualiza
        if (!auth.isAuthenticated() || validateAddress()) return

        viewModelScope.launch(Dispatchers.IO) {
            // actualiza la dirección del candidato
            val response = candidateService.partialUpdateCandidate(
                auth = auth.getToken()!!,
                id = auth.getUserId()!!,
                candidate = PartialCandidateOUT(
                    user = PartialUserOUT(
                        address = _address.value
                    )
                )
            )

            // actualiza el estado de error
            _addressErrorVisibility.value = !response.isSuccessful
            // si la respuesta es correcta, se vuelve a la pantalla anterior
            if (response.isSuccessful){
                withContext(Dispatchers.Main){
                    navController.popBackStack()
                }
            }
        }

    }

    /**
     * Actualiza la dirección del candidato
     * @throws NotImplementedError
     */
    fun updateCompanyAddress() {
        throw NotImplementedError("Not implemented yet")
    }

    data class Address(
        val postalCode: String,
        val province: String,
        val city: String,
        val street: String
    ){
        companion object{
            fun fromString(addressString: String): Address {
                val address = addressString.split("-")
                return Address(
                    postalCode = address[0],
                    province = address[1],
                    city = address[2],
                    street = address[3]
                )
            }
        }

        override fun toString(): String {
            return "$postalCode-$province-$city-$street"
        }
    }


}

class UpdateUserAddressViewModelFactory(
    private val navController: NavController,
    private val address: UpdateUserAddressViewModel.Address
): ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return UpdateUserAddressViewModel(navController, address) as T
    }
}