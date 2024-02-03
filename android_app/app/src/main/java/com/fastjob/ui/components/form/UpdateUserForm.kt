package com.fastjob.ui.components.form

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.text.isDigitsOnly
import com.fastjob.R
import com.fastjob.models.UserType
import com.fastjob.ui.components.basic.BasicDialog
import com.fastjob.ui.components.basic.TextFieldMultiple
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.viewmodels.form.user.UpdateUserViewModel

@Composable
fun UpdateUserForm(
    viewModel: UpdateUserViewModel
) {
    if(!UpdateUserViewModel.auth.isAuthenticated()) viewModel.navController.navigate(AppScreens.UserLoginScreen.route)

    // información del usuario
    val userData by viewModel.userData.collectAsState()

    // errores de los datos del usuario
    val userDataError by viewModel.userDataError.collectAsState()

    // visibilidad del mensaje de error
    val errorMessageVisibility by viewModel.errorMessageVisibility.collectAsState()

    BasicDialog(
        title = stringResource(id = R.string.user_update_error_title),
        content = stringResource(id = R.string.user_update_error_msg),
        icon = painterResource(id = R.drawable.error),
        visibilityState = Pair(errorMessageVisibility,viewModel::setErrorVisibility)
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
            .imePadding()
            .verticalScroll(rememberScrollState()),
    ) {

        // imagen y titulo
        Image(
            painter = painterResource(id = R.drawable.user_img),
            contentDescription = stringResource(id = R.string.user_image_desc)
        )
        Text(
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 5.dp),
            text = stringResource(id = R.string.candidate_form_title),
            textAlign = TextAlign.Center,
            fontSize = 30.sp
        )


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
                    viewModel.setUserName(it)
                // si el nombre esta vacio se muestra el error
                viewModel.setDataError(userDataError.copy(name = it.isEmpty()))
            },
            isError = userDataError.name,
            supportingText = {
                // si hay error en el nombre se muestra el mensaje de error
                if (userDataError.name)
                    Text(stringResource(id = R.string.register_user_name_error))
            }
        )

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
                    viewModel.setUserLastName(it)
                // si el apellido esta vacio se muestra el error
                viewModel.setDataError(userDataError.copy(surname = it.isEmpty()))
            },
            isError = userDataError.surname,
            supportingText = {
                // si hay error en el apellido se muestra el mensaje de error
                if (userDataError.surname)
                    Text(stringResource(id = R.string.register_user_surname_error))
            }
        )

        // campo de los telefonos
        TextFieldMultiple(
            label = stringResource(id = R.string.register_user_phones),
            setError = { viewModel.setDataError(userDataError.copy(phoneNumbers = it)) },
            checkError = { it.isNotEmpty() && it.length != 9 },
            buttonAddText = stringResource(id = R.string.register_user_button_add_tlf),
            itemList = userData.phoneNumbers.map { if (it > 0) it.toString() else "" },
            setList = viewModel::setUserPhones,
            itemsCheck = { item -> item.isDigitsOnly() && item.length <= 9 },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
            maxHeight = 300,
            errorMsg = stringResource(id = R.string.register_user_phone_error),
        )




        // botón de update
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .padding(top = 10.dp),
            contentAlignment = Alignment.BottomEnd
        ){
            TextButton(
                onClick = {
                    if(UpdateUserViewModel.auth.getUserType() == UserType.CANDIDATE) viewModel.updateCandidate()
                    else viewModel.updateCompany()
                }
            ) {
                Text(text = stringResource(id = R.string.update_button))
            }
        }



    }








}