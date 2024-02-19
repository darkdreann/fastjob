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
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.core.text.isDigitsOnly
import com.fastjob.R
import com.fastjob.ui.components.basic.CreatePasswordField
import com.fastjob.ui.components.basic.TextFieldMultiple
import com.fastjob.ui.functions.isEmail
import com.fastjob.ui.theme.FastjobTheme
import com.fastjob.ui.viewmodels.user.CreateUserViewModel

/**
 * Formulario para crear un usuario
 * @param viewModel [CreateUserViewModel] ViewModel del formulario
 */
@Composable
fun CreateUserForm(
    viewModel: CreateUserViewModel
){
    // estado del formulario de usuario
    val userData by viewModel.userData.collectAsState()

    // estado del error del formulario de usuario
    val userDataError by viewModel.userError.collectAsState()




    // formulario de usuario
    Column(
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {

        // campo de username
        TextField(
            singleLine = true,
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(15.dp)),
            label = { Text(stringResource(id = R.string.register_user_username)) },
            value = userData.username,
            onValueChange = {
                // si el username tiene menos de 16 caracteres se actualiza el estado
                if(it.length <= 16)
                    viewModel.setUsername(it)
                // si el username tiene menos de 4 caracteres se muestra el error
                viewModel.setErrorUserData(userDataError.copy(username = it.length < 4))
            },
            isError = userDataError.username,
        )
        if(userDataError.username){
            Text(
                text = stringResource(id = R.string.register_user_username_error),
                color = MaterialTheme.colorScheme.error,
            )
        }

        // campo de email
        TextField(
            singleLine = true,
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(15.dp)),
            label = { Text(stringResource(id = R.string.register_user_email)) },
            value = userData.email,
            onValueChange = {
                viewModel.setEmail(it)
                // si el email no es valido se muestra el error
                viewModel.setErrorUserData(userDataError.copy(email = !it.isEmail()))
            },
            isError = userDataError.email,
        )
        if(userDataError.email){
            Text(
                text = stringResource(id = R.string.register_user_email_error),
                color = MaterialTheme.colorScheme.error,
            )
        }

        // campo de nombre
        TextField(
            singleLine = true,
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(15.dp)),
            label = { Text(stringResource(id = R.string.register_user_name)) },
            value = userData.name,
            onValueChange = {
                // si el nombre tiene menos de 25 caracteres se actualiza el estado
                if (it.length <= 25)
                    viewModel.setName(it)
                // si el nombre esta vacio se muestra el error
                viewModel.setErrorUserData(userDataError.copy(name = it.isEmpty()))
            },
            isError = userDataError.name,
        )
        if(userDataError.name){
            Text(
                text = stringResource(id = R.string.register_user_name_error),
                color = MaterialTheme.colorScheme.error,
            )
        }

        // campo de apellido
        TextField(
            singleLine = true,
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(15.dp)),
            label = { Text(stringResource(id = R.string.register_user_surname)) },
            value = userData.surname,
            onValueChange = {
                // si el apellido tiene menos de 25 caracteres se actualiza el estado
                if (it.length <= 25)
                    viewModel.setSurname(it)
                // si el apellido esta vacio se muestra el error
                viewModel.setErrorUserData(userDataError.copy(surname = it.isEmpty()))
            },
            isError = userDataError.surname,
        )
        if(userDataError.surname){
            Text(
                text = stringResource(id = R.string.register_user_surname_error),
                color = MaterialTheme.colorScheme.error,
            )
        }

        // campo de contraseña
        CreatePasswordField(
            maxLength = 30,
            errorState = Pair(userDataError.password){ viewModel.setErrorUserData(userDataError.copy(password = it)) },
            setPassword = viewModel::setPassword
        )

        // campo de los telefonos
        TextFieldMultiple(
            label = stringResource(id = R.string.register_user_phones),
            setError = { viewModel.setErrorUserData(userDataError.copy(phoneNumbers = it)) },
            checkError = { it.isNotEmpty() && it.length != 9 },
            buttonAddText = stringResource(id = R.string.register_user_button_add_tlf),
            itemList = userData.phoneNumbers.map { if (it > 0) it.toString() else "" },
            setList = viewModel::setPhoneNumbers,
            itemsCheck = { item -> item.isDigitsOnly() && item.length <= 9 },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
            maxHeight = 300,
            errorMsg = stringResource(id = R.string.register_user_phone_error),
        )

        // campo de la direccion
        AddressForm(
            viewModel = viewModel,
            addressErrorState = Pair(userDataError.address){ viewModel.setErrorUserData(userDataError.copy(address = it)) }
        )

    }
}

@Preview(showBackground = true)
@Composable
fun CreateUserPreview() {
    FastjobTheme {
        CreateUserForm(
            viewModel = CreateUserViewModel()
        )
    }
}
