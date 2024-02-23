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
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.fastjob.R
import com.fastjob.models.UserType
import com.fastjob.ui.components.basic.BasicDialog
import com.fastjob.ui.viewmodels.user.UpdateUserAddressViewModel
import com.fastjob.ui.viewmodels.user.UpdateUserViewModel

/**
 * Formulario de actualización de dirección de usuario
 * @param viewModel ViewModel del formulario
 */
@Composable
fun UpdateUserAddressForm(
    viewModel: UpdateUserAddressViewModel
) {
    // estado de error del formulario
    val userDataError by viewModel.addressError.collectAsState()

    // estado de la visibilidad del error
    val userDataErrorVisibility by viewModel.addressErrorVisibility.collectAsState()


    // dialogo de error
    BasicDialog(
        title = stringResource(id = R.string.user_address_update_error_title),
        content = stringResource(id = R.string.user_address_update_error_msg),
        icon = painterResource(id = R.drawable.error),
        visibilityState = Pair(userDataErrorVisibility, viewModel::setErrorUserDataVisibility)
    )


    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
            .imePadding()
            .verticalScroll(rememberScrollState()),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(10.dp)
    ) {

        // imagen de usuario
        Image(
            modifier = Modifier
                .fillMaxWidth(),
            painter = painterResource(id = R.drawable.user_img),
            contentDescription = stringResource(id = R.string.user_image_desc),
        )
        Text(
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 5.dp),
            text = stringResource(id = R.string.update_address),
            textAlign = TextAlign.Center,
            fontSize = 30.sp
        )

        // campo de la direccion
        AddressForm(
            viewModel = viewModel,
            addressErrorState = Pair(userDataError, viewModel::setErrorUserData)
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
                    if(UpdateUserViewModel.auth.getUserType() == UserType.CANDIDATE) viewModel.updateCandidateAddress()
                    else viewModel.updateCompanyAddress()
                }
            ) {
                Text(text = stringResource(id = R.string.update_button))
            }
        }


    }



}