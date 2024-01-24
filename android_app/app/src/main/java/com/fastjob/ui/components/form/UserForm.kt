package com.fastjob.ui.components.form

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
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
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.core.text.isDigitsOnly
import com.fastjob.R
import com.fastjob.ui.components.basic.PasswordField
import com.fastjob.ui.components.basic.TextFieldMultiple
import com.fastjob.ui.functions.isEmail
import com.fastjob.ui.theme.FastjobTheme
import com.fastjob.ui.viewmodels.form.user.CreateUserViewModel

@Composable
fun CreateUserForm(
    viewModel: CreateUserViewModel
){
    // estado del formulario de usuario
    val userData by viewModel.userData.collectAsState()

    // estado del error del formulario de usuario
    val userDataError by viewModel.userError.collectAsState()


    // estados de error de los campos del formulario de usuario
    var usernameError by remember { mutableStateOf(false) }
    var emailError by remember { mutableStateOf(false) }
    var nameError by remember { mutableStateOf(false) }
    var surnameError by remember { mutableStateOf(false) }
    var passwordError by remember { mutableStateOf(false) }


    Column(
        verticalArrangement = Arrangement.spacedBy(7.dp),
    ) {

        TextField(
            singleLine = true,
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(15.dp)),
            label = { Text(stringResource(id = R.string.register_user_username)) },
            value = userData.username,
            onValueChange = {
                if(it.length <= 16)
                    viewModel.setUsername(it)
                usernameError = it.length < 4
                viewModel.setErrorUserData(userDataError.copy(username = usernameError))
            },
            isError = usernameError,
            supportingText = {
                if (userDataError.username)
                    Text(stringResource(id = R.string.register_user_username_error))
            }
        )

        TextField(
            singleLine = true,
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(15.dp)),
            label = { Text(stringResource(id = R.string.register_user_email)) },
            value = userData.email,
            onValueChange = {
                viewModel.setEmail(it)
                emailError = !it.isEmail()
                viewModel.setErrorUserData(userDataError.copy(email = emailError))
            },
            isError = emailError,
            supportingText = {
                if (userDataError.email)
                    Text(stringResource(id = R.string.register_user_email_error))
            }
        )

        TextField(
            singleLine = true,
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(15.dp)),
            label = { Text(stringResource(id = R.string.register_user_name)) },
            value = userData.name,
            onValueChange = {
                if (it.length <= 25)
                    viewModel.setName(it)
                nameError = it.isEmpty()
                viewModel.setErrorUserData(userDataError.copy(name = nameError))
            },
            isError = nameError,
            supportingText = {
                if (userDataError.name)
                    Text(stringResource(id = R.string.register_user_name_error))
            }
        )

        TextField(
            singleLine = true,
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(15.dp)),
            label = { Text(stringResource(id = R.string.register_user_surname)) },
            value = userData.surname,
            onValueChange = {
                if (it.length <= 25)
                    viewModel.setSurname(it)
                surnameError = it.isEmpty()
                viewModel.setErrorUserData(userDataError.copy(surname = surnameError))
            },
            isError = surnameError,
            supportingText = {
                if (userDataError.surname)
                    Text(stringResource(id = R.string.register_user_surname_error))
            }
        )

        PasswordField(
            label = stringResource(id = R.string.register_user_password),
            maxLength = 30,
            errorState = Pair(passwordError){
                passwordError = it
                viewModel.setErrorUserData(userDataError.copy(password = passwordError))
            },
            passwordState = Pair(userData.password, viewModel::setPassword)
        )

        TextFieldMultiple(
            label = stringResource(id = R.string.register_user_phones),
            setError = { viewModel.setErrorUserData(userDataError.copy(phoneNumbers = it)) },
            buttonAddText = stringResource(id = R.string.register_user_button_add_tlf),
            itemList = userData.phoneNumbers.map { if (it > 0) it.toString() else "" },
            setList = viewModel::setPhoneNumbers,
            itemsCheck = { item -> item.isDigitsOnly() && item.length <= 9 },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
            maxHeight = 300,
            errorMsg = stringResource(id = R.string.register_user_phone_error),
        )

        CreateAddressForm(
            setError = { viewModel.setErrorUserData(userDataError.copy(address = it)) },
            viewModel = viewModel
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
