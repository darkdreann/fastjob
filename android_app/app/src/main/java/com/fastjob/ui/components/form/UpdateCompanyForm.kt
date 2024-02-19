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
import com.fastjob.R
import com.fastjob.ui.components.basic.BasicDialog
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.viewmodels.company.UpdateCompanyViewModel
import com.fastjob.ui.viewmodels.user.CreateCompanyViewModel

/**
 * Formulario de actualización de empresa
 * @param viewModel ViewModel del formulario
 */
@Composable
fun UpdateCompanyForm(
    viewModel: UpdateCompanyViewModel
) {
    if(!UpdateCompanyViewModel.auth.isAuthenticated()) viewModel.navController.navigate(AppScreens.UserLoginScreen.route)

    // información de la empresa
    val companyData by viewModel.companyData.collectAsState()

    // errores de los datos de la empresa
    val companyDataError by viewModel.companyDataError.collectAsState()

    // visibilidad del mensaje de error
    val errorMessageVisibility by viewModel.errorMessageVisibility.collectAsState()

    BasicDialog(
        title = stringResource(id = R.string.company_update_error_title),
        content = stringResource(id = R.string.company_update_error_msg),
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
            text = stringResource(id = R.string.company_update_form_title),
            textAlign = TextAlign.Center,
            fontSize = 30.sp
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
                    viewModel.setCompanyData(companyData.copy(tin = it))
                // si el cif no es valido
                viewModel.setDataError(companyDataError.copy(tin = !it.matches(CreateCompanyViewModel.CIF_REGEX)))
            },
            isError = companyDataError.tin,
        )
        if(companyDataError.tin){
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
                    viewModel.setCompanyData(companyData.copy(companyName = it))
                // si el nombre de la empresa no es valido
                viewModel.setDataError(companyDataError.copy(companyName = it.isEmpty()))
            },
            isError = companyDataError.companyName,
        )
        if(companyDataError.companyName){
            Text(
                text = stringResource(id = R.string.register_company_name_error),
                color = MaterialTheme.colorScheme.error,
            )
        }


        // botón de update
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .padding(top = 10.dp),
            contentAlignment = Alignment.BottomEnd
        ){
            TextButton(
                onClick = {
                    viewModel.updateCompany()
                }
            ) {
                Text(text = stringResource(id = R.string.update_button))
            }
        }



    }








}