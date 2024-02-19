package com.fastjob.ui.effects

import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import com.fastjob.auth.AuthAPI
import com.fastjob.models.AddressNoStreetIN
import com.fastjob.models.AddressOUT
import com.fastjob.network.Client
import com.fastjob.services.AddressService
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

/**
 * Efecto que se encarga de obtener la dirección a partir del código postal
 * @param address dirección a la que se le asignará el código postal
 * @param setAddress función que se encarga de asignar la dirección obtenida
 */
@Composable
fun AddressByPostalCodeEffect(
    address: AddressOUT,
    setAddress: (AddressNoStreetIN) -> Unit
) {
    // obtenemos el servicio de direcciones y la instancia de autenticación
    val addresService = Client.getInstance().getService(AddressService::class.java)
    val auth = AuthAPI.getInstance()

    LaunchedEffect(address.postalCode){
        withContext(Dispatchers.IO){
            // si el código postal tiene más de 5 dígitos, se realiza la petición
            if(address.postalCode >= 5){
                val response = addresService.getAddressByPostalCode(
                    auth = auth.getToken(),
                    postalCode = address.postalCode
                )


                // si la respuesta es exitosa, se asigna la dirección
                if(response.isSuccessful){
                    response.body()?.let {
                        setAddress(it)
                    }
                }
            }
        }
    }
}