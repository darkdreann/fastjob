package com.fastjob.ui.components.form

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
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
import com.fastjob.ui.viewmodels.form.user.CreateUserViewModel


@Composable
fun CreateAddressForm(
    viewModel: CreateUserViewModel,
    setError: (Boolean) -> Unit =  {},
){
    // user data state
    val userData by viewModel.userData.collectAsState()

    // estado que indica si se ha cambiado la direccion con el efecto
    var addressChanged by remember { mutableStateOf(false) }

    // estado del texto del codigo postal
    var addressText by remember {
        mutableStateOf(if(userData.address.postalCode > 0) userData.address.postalCode.toString() else "")
    }

    // errores del formulario de direccion
    var postalCodeError by remember { mutableStateOf(false) }
    var provinceError by remember { mutableStateOf(false) }
    var cityError by remember { mutableStateOf(false) }
    var streetError by remember { mutableStateOf(false) }

    AddressByPostalCodeEffect(
        address = userData.address,
        setAddress = {
            viewModel.setAddressCity(it.city)
            viewModel.setAddressProvince(it.province)
            viewModel.setAddressStreet(it.street)
            addressChanged = true
        }
    )

    Column(
        verticalArrangement = Arrangement.spacedBy(4.dp)
    )
    {
        TextField(
            singleLine = true,
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(15.dp)),
            label = { Text(stringResource(id = R.string.register_user_postal_code)) },
            value = addressText,
            onValueChange = {
                if (it.isDigitsOnly() && it.length <= 5) {
                    addressText = it
                    viewModel.setAddressPostalCode(it)
                }
                if(addressChanged){
                    addressChanged = false
                    viewModel.setAddressCity("")
                    viewModel.setAddressProvince("")
                    viewModel.setAddressStreet("")
                }
                postalCodeError = it.length < 5
                setError(postalCodeError)
            },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
            isError = postalCodeError,
            supportingText = {
                if (postalCodeError)
                    Text(stringResource(id = R.string.register_user_postal_code_error))
            }

        )

        TextField(
            singleLine = true,
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(15.dp)),
            label = { Text(stringResource(id = R.string.register_user_province)) },
            value = userData.address.province,
            onValueChange = {
                if(it.length <= 20)
                    viewModel.setAddressProvince(it)
                provinceError = it.isEmpty()
                setError(provinceError)
            },
            isError = provinceError,
            supportingText = {
                if (provinceError)
                    Text(stringResource(id = R.string.register_user_province_error))
            }
        )

        TextField(
            singleLine = true,
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(15.dp)),
            label = { Text(stringResource(id = R.string.register_user_city)) },
            value = userData.address.city,
            onValueChange = {
                if(it.length <= 20)
                    viewModel.setAddressCity(it)
                cityError = it.isEmpty()
                setError(cityError)
            },
            isError = cityError,
            supportingText = {
                if (cityError)
                    Text(stringResource(id = R.string.register_user_city_error))
            }

        )

        TextField(
            singleLine = true,
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(15.dp)),
            label = { Text(stringResource(id = R.string.register_user_street)) },
            value = userData.address.street,
            onValueChange = {
                if(it.length <= 30)
                    viewModel.setAddressStreet(it)
                streetError = it.isEmpty()
                setError(streetError)
            },
            isError = streetError,
            supportingText = {
                if (streetError)
                    Text(stringResource(id = R.string.register_user_street_error))
            }
        )
    }





}