package com.fastjob.ui.components.form

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
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
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.fastjob.R
import com.fastjob.ui.components.basic.BasicDialog
import com.fastjob.ui.components.basic.LanguageWithLevelPicker
import com.fastjob.ui.components.basic.TextFieldPicker
import com.fastjob.ui.functions.keywords.management.EducationPicker
import com.fastjob.ui.functions.toUUID
import com.fastjob.ui.viewmodels.company.CreateCompanyJobViewModel

/**
 * Formulario básico de oferta de trabajo
 * @param viewModel ViewModel del formulario
 */
@Composable
fun CreateJobForm(
    viewModel: CreateCompanyJobViewModel
){

    // estado de la formación de la oferta de trabajo
    val jobEducation by viewModel.jobEducation.collectAsState()
    val (jobEducationName, setJobEducationName) = remember { mutableStateOf(jobEducation.educationQualification) }

    // estado de los errores de la formación de la oferta de trabajo
    val jobDataError by viewModel.jobEducationError.collectAsState()

    // estado del error de la dirección de la oferta de trabajo
    val addressError by viewModel.addressError.collectAsState()

    // picker de formación
    val educationPicker = remember { EducationPicker() }

    // estado de la visibilidad del error
    val errorVisibility by viewModel.jobDialogVisibility.collectAsState()

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
            text = stringResource(id = R.string.create_job_form_title),
            fontSize = 25.sp,
            textAlign = TextAlign.Center
        )

        // formulario de datos basicos de una oferta de trabajo
        BasicJobForm(
            viewModel = viewModel
        )

        // campo de formación
        TextFieldPicker(
            padding = 0.dp,
            label = stringResource(id = R.string.job_education),
            setValue = { viewModel.setJobEducation(jobEducation.copy(educationId = educationPicker.getEducationId(it).toUUID()))},
            textState = Pair(jobEducationName){
                viewModel.setJobEducation(jobEducation.copy(educationQualification = it))
                setJobEducationName(it)
            },
            autoCompleteFunction = educationPicker::getEducations,
            isError = jobDataError,
        )

        // picker de idiomas
        LanguageWithLevelPicker(
            viewModel = viewModel
        )

        // formulario de dirección de la oferta de trabajo
        AddressForm(
            viewModel = viewModel,
            addressErrorState = Pair(addressError, viewModel::setAddressError)
        )

        // botón de crear oferta de trabajo
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .padding(top = 10.dp),
            contentAlignment = Alignment.BottomEnd
        ){
            TextButton(
                onClick = {
                    viewModel.createJob()
                }
            ) {
                Text(text = stringResource(id = R.string.save_button))
            }
        }



    }



}