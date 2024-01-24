package com.fastjob.ui.effects

import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import com.fastjob.auth.AuthAPI
import com.fastjob.models.AddressIN
import com.fastjob.models.AddressOUT
import com.fastjob.network.Client
import com.fastjob.services.AddressService
import com.fastjob.services.JobService
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

@Composable
fun AddressByPostalCodeEffect(
    address: AddressOUT,
    setAddress: (AddressIN) -> Unit
) {
    // obtenemos el servicio de trabajos y la instancia de autenticación
    val addresService = Client.getInstance().getService(AddressService::class.java)
    val auth = AuthAPI.getInstance()

    LaunchedEffect(address.postalCode){
        withContext(Dispatchers.IO){
            if(address.postalCode >= 5){
                val response = addresService.getAddressByPostalCode(
                    auth = auth.getToken(),
                    postalCode = address.postalCode
                )

                if(response.isSuccessful){
                    response.body()?.let {
                        setAddress(it)
                    }
                }
            }
        }
    }
}