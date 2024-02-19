package com.fastjob.ui.components.form

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
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
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import com.fastjob.R
import com.fastjob.ui.components.basic.BasicDialog
import com.fastjob.ui.enums.RegisterState
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.viewmodels.user.CreateCompanyViewModel

/**
 * Formulario de registro de candidato
 * @param viewModel ViewModel del formulario
 * @param navController controlador de navegación
 */
@Composable
fun CreateCompanyForm(
    viewModel: CreateCompanyViewModel,
    navController: NavController
){

    // estado del formulario de registro
    val registerState by viewModel.registerState.collectAsState()

    // estado del formulario de candidato
    val companyData by viewModel.companyData.collectAsState()

    // estado mensajes error
    val errorVisibility by viewModel.errorVisibility.collectAsState()

    // estado de los errores del formulario
    val companyError by viewModel.companyError.collectAsState()

    // dialogo de error o navegación a login si el registro es correcto
    when(registerState){
        // si el registro es correcto, navegar a login
        RegisterState.REGISTERED -> {
            navController.navigate(AppScreens.UserLoginScreen.route)
        }
        // mostrar dialogo de error si la información del formulario no es válida
        RegisterState.FORM_NOT_VALID -> {
            BasicDialog(
                title = stringResource(id = R.string.candidate_register_error_title),
                content = stringResource(id = R.string.candidate_register_no_form_valid),
                icon = painterResource(id = R.drawable.error),
                visibilityState = Pair(errorVisibility, viewModel::setErrorVisibility)
            )
        }
        // mostrar dialogo de error si el nombre de usuario ya existe
        RegisterState.DUPLICATED_USERNAME -> {
            BasicDialog(
                title = stringResource(id = R.string.candidate_register_error_title),
                content = stringResource(id = R.string.candidate_register_error_username),
                icon = painterResource(id = R.drawable.error),
                visibilityState = Pair(errorVisibility, viewModel::setErrorVisibility)
            )
        }
        // mostrar dialogo de error si el email ya existe
        RegisterState.DUPLICATED_EMAIL -> {
            BasicDialog(
                title = stringResource(id = R.string.candidate_register_error_title),
                content = stringResource(id = R.string.candidate_register_error_email),
                icon = painterResource(id = R.drawable.error),
                visibilityState = Pair(errorVisibility, viewModel::setErrorVisibility)
            )
        }
        // mostrar dialogo de error si ha ocurrido un error desconocido
        RegisterState.UNKNOWN_ERROR -> {
            BasicDialog(
                title = stringResource(id = R.string.candidate_register_error_title),
                content = stringResource(id = R.string.candidate_register_error),
                icon = painterResource(id = R.drawable.error),
                visibilityState = Pair(errorVisibility, viewModel::setErrorVisibility)
            )
        }
        else -> {}
    }


    // formulario de registro
    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .imePadding(),
        verticalArrangement = Arrangement.spacedBy(15.dp),
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
            text = stringResource(id = R.string.company_form_title),
            textAlign = TextAlign.Center,
            fontSize = 30.sp
        )

        // formulario de usuario
        CreateUserForm(
            viewModel = viewModel
        )

        // CIF
        TextField(
            singleLine = true,
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(15.dp)),
            label = { Text(stringResource(id = R.string.register_company_tin)) },
            value = companyData.tin,
            onValueChange = {
                // si tiene menos de 10 caracteres se actualiza el estado
                if(it.length <= 9)
                    viewModel.setTin(it)
                // si el cif no es valido
                viewModel.setCompanyError(companyError.copy(tin = !it.matches(CreateCompanyViewModel.CIF_REGEX)))
            },
            isError = companyError.tin,
        )
        if(companyError.tin){
            Text(
                text = stringResource(id = R.string.register_company_tin_error),
                color = MaterialTheme.colorScheme.error,
            )
        }

        // nombre de la empresa
        TextField(
            singleLine = true,
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(15.dp)),
            label = { Text(stringResource(id = R.string.register_company_name)) },
            value = companyData.companyName,
            onValueChange = {
                // si tiene menos de 30 caracteres se actualiza el estado
                if(it.length <= 30)
                    viewModel.setCompanyName(it)
                // si el nombre de la empresa no es valido
                viewModel.setCompanyError(companyError.copy(companyName = it.isEmpty()))
            },
            isError = companyError.companyName,
        )
        if(companyError.companyName){
            Text(
                text = stringResource(id = R.string.register_company_name_error),
                color = MaterialTheme.colorScheme.error,
            )
        }

        // botón de registro
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .padding(top = 10.dp),
            contentAlignment = Alignment.BottomEnd
        ){
            TextButton(
                onClick = {
                    viewModel.registerCompany()
                }
            ) {
                Text(text = stringResource(id = R.string.user_register_button))
            }
        }

    }
}