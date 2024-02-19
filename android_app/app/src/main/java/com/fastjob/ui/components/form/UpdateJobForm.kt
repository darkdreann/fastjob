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
import androidx.compose.runtime.LaunchedEffect
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
import com.fastjob.ui.components.basic.BasicDialog
import com.fastjob.ui.components.basic.ErrorItem
import com.fastjob.ui.components.basic.LoadingItem
import com.fastjob.ui.enums.LoadState
import com.fastjob.ui.viewmodels.company.UpdateCompanyJobViewModel

/**
 * Formulario básico de oferta de trabajo
 * @param viewModel ViewModel del formulario
 */
@Composable
fun UpdateJobForm(
    viewModel: UpdateCompanyJobViewModel
) {
    // estado de carga
    val loadState by viewModel.loadState.collectAsState()

    // estado del error de la dirección de la oferta de trabajo
    val addressError by viewModel.addressError.collectAsState()

    // estado de la visibilidad del error
    val errorVisibility by viewModel.jobDialogVisibility.collectAsState()

    // carga de la oferta de trabajo
    LaunchedEffect(Unit){
        viewModel.loadJob()
    }

    // item de carga y error
    when (loadState) {
        // item de carga
        LoadState.LOADING -> {
            Box(
                modifier = Modifier
                    .fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                LoadingItem("")
            }
        }
        // item de error de carga
        LoadState.ERROR -> {
            Box(
                modifier = Modifier
                    .fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                ErrorItem(
                    text = stringResource(id = R.string.list_error)
                )
            }
        }

        LoadState.LOADED -> {
            BasicDialog(
                title = stringResource(id = R.string.job_form_error_title),
                content = stringResource(id = R.string.job_form_error_msg),
                icon = painterResource(id = R.drawable.error),
                visibilityState = Pair(errorVisibility, viewModel::setJobDialogVisibility)
            )

            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .verticalScroll(rememberScrollState())
                    .padding(horizontal = 12.dp)
                    .imePadding(),
                verticalArrangement = Arrangement.spacedBy(10.dp)
            ) {

                // imagen
                Image(
                    modifier = Modifier
                        .fillMaxWidth(),
                    painter = painterResource(id = R.drawable.job_first),
                    contentDescription = stringResource(id = R.string.job_image_desc),
                )
                // titulo formulario
                Text(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(bottom = 16.dp, top = 10.dp),
                    text = stringResource(id = R.string.update_job_form_title),
                    fontSize = 25.sp,
                    textAlign = TextAlign.Center
                )

                // formulario de datos basicos de una oferta de trabajo
                BasicJobForm(
                    viewModel = viewModel
                )


                // formulario de dirección de la oferta de trabajo
                AddressForm(
                    viewModel = viewModel,
                    addressErrorState = Pair(addressError, viewModel::setAddressError)
                )

                // botón de actualizar oferta de trabajo
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 10.dp),
                    contentAlignment = Alignment.BottomEnd
                ) {
                    TextButton(
                        onClick = {
                            viewModel.updateJob()
                        }
                    ) {
                        Text(text = stringResource(id = R.string.save_button))
                    }
                }


            }
        }


        else -> {}
    }
}