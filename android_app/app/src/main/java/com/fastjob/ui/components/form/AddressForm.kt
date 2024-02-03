package com.fastjob.ui.components.form

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.core.text.isDigitsOnly
import com.fastjob.R
import com.fastjob.ui.effects.AddressByPostalCodeEffect
import com.fastjob.ui.viewmodels.interfaces.AddressForm

/**
 * Formulario de direccion
 * @param viewModel ViewModel del formulario
 * @param addressErrorState Estado del error del formulario de direccion
 */
@Composable
fun AddressForm(
    viewModel: AddressForm,
    addressErrorState: Pair<Boolean, (Boolean) -> Unit> = Pair(false) {}
){
    // user data state
    val address by viewModel.address.collectAsState()

    // estado del error del formulario de direccion
    val (addressError, setAddressError) = addressErrorState

    // estado que indica si se ha cambiado la direccion con el efecto
    var addressChanged by remember { mutableStateOf(false) }

    // estado del texto del codigo postal
    var addressText by remember { mutableStateOf(if(address.postalCode > 0) address.postalCode.toString() else "") }

    // errores del formulario de direccion
    var postalCodeError by remember { mutableStateOf(false) }
    var provinceError by remember { mutableStateOf(false) }
    var cityError by remember { mutableStateOf(false) }
    var streetError by remember { mutableStateOf(false) }


    // efecto que muestra los errores del formulario
    LaunchedEffect(addressError){
        if(addressError) {
            postalCodeError = addressText.length < 5
            provinceError = address.province.isEmpty()
            cityError = address.city.isEmpty()
            streetError = address.street.isEmpty()
        }else{
            postalCodeError = false
            provinceError = false
            cityError = false
            streetError = false
        }
    }


    // efecto que obtiene la direccion por el codigo postal
    AddressByPostalCodeEffect(
        address = address,
        setAddress = {
            viewModel.setAddressCity(it.city)
            viewModel.setAddressProvince(it.province)
            viewModel.setAddressStreet(it.street)
            addressChanged = true
        }
    )

    Column(
        verticalArrangement = Arrangement.spacedBy(8.dp)
    )
    {
        // textfield del codigo postal
        TextField(
            singleLine = true,
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(15.dp)),
            label = { Text(stringResource(id = R.string.register_user_postal_code)) },
            value = addressText,
            onValueChange = {
                // si es un numero y tiene menos de 5 digitos se cambia el codigo postal
                if (it.isDigitsOnly() && it.length <= 5) {
                    addressText = it
                    viewModel.setAddressPostalCode(it)
                }
                // si se ha cambiado la direccion con el efecto se borra la direccion
                if(addressChanged){
                    addressChanged = false
                    viewModel.setAddressCity("")
                    viewModel.setAddressProvince("")
                    viewModel.setAddressStreet("")
                }
                // si el codigo postal tiene menos de 5 digitos se muestra el error
                setAddressError(it.length < 5)
            },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
            isError = postalCodeError,
        )
        if(postalCodeError){
            Text(
                text = stringResource(id = R.string.register_user_postal_code_error),
                color = MaterialTheme.colorScheme.error,
            )
        }


        // textfields de la provincia
        TextField(
            singleLine = true,
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(15.dp)),
            label = { Text(stringResource(id = R.string.register_user_province)) },
            value = address.province,
            onValueChange = {
                // si la longitud es menor o igual a 20 se cambia la provincia
                if(it.length <= 20)
                    viewModel.setAddressProvince(it)
                // si no hay texto se muestra el error
                setAddressError(it.isEmpty())
            },
            isError = provinceError,
        )
        if(provinceError){
            Text(
                text = stringResource(id = R.string.register_user_province_error),
                color = MaterialTheme.colorScheme.error,
            )
        }

        // textfields de la ciudad
        TextField(
            singleLine = true,
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(15.dp)),
            label = { Text(stringResource(id = R.string.register_user_city)) },
            value = address.city,
            onValueChange = {
                // si la longitud es menor o igual a 20 se cambia la ciudad
                if(it.length <= 20)
                    viewModel.setAddressCity(it)
                // si no hay texto se muestra el error
                setAddressError(it.isEmpty())
            },
            isError = cityError,
        )
        if(cityError){
            Text(
                text = stringResource(id = R.string.register_user_city_error),
                color = MaterialTheme.colorScheme.error,
            )
        }

        // textfields de la calle
        TextField(
            singleLine = true,
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(15.dp)),
            label = { Text(stringResource(id = R.string.register_user_street)) },
            value = address.street,
            onValueChange = {
                // si la longitud es menor o igual a 30 se cambia la calle
                if(it.length <= 30)
                    viewModel.setAddressStreet(it)
                // si no hay texto se muestra el error
                setAddressError(it.isEmpty())
            },
            isError = streetError,
        )
        if(streetError){
            Text(
                text = stringResource(id = R.string.register_user_street_error),
                color = MaterialTheme.colorScheme.error,
            )
        }
    }
}