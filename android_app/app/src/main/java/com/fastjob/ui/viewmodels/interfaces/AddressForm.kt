package com.fastjob.ui.viewmodels.interfaces

import com.fastjob.models.AddressOUT
import kotlinx.coroutines.flow.StateFlow


/**
 * Interfaz para el formulario de direccion
 */
interface AddressForm {
    val address: StateFlow<AddressOUT>
    fun setAddressPostalCode(postalCode: String)
    fun setAddressProvince(province: String)
    fun setAddressCity(city: String)
    fun setAddressStreet(street: String)
}