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
import com.fastjob.ui.components.basic.CustomDatePicker
import com.fastjob.ui.components.basic.ErrorItem
import com.fastjob.ui.components.basic.LoadingItem
import com.fastjob.ui.components.basic.TextFieldPicker
import com.fastjob.ui.enums.LoadState
import com.fastjob.ui.functions.keywords.management.EducationPicker
import com.fastjob.ui.functions.toUUID
import com.fastjob.ui.viewmodels.candidate.CandidateEducationViewModel
import java.time.LocalDate

/**
 * Formulario de formacion del candidato
 * @param viewModel ViewModel del formulario de formaciones
 */
@Composable
fun CandidateEducationForm(
    viewModel: CandidateEducationViewModel
) {

    // estado de la formacion
    val education by viewModel.education.collectAsState()

    // estado de error de la formacion
    val educationError by viewModel.educationError.collectAsState()

    // estado de carga
    val loadState by viewModel.loadState.collectAsState()

    // estado del dialogo de error
    val errorVisibility by viewModel.errorVisibility.collectAsState()

    // picker de formaciones para el autocomplete de formaciones
    val educationPicker = remember { EducationPicker() }

    // estado nombre formacion
    val (educationName, setEducationName) = remember { mutableStateOf("") }

    // carga de la formacion
    LaunchedEffect(Unit){
        viewModel.loadEducation(setEducationName)
    }

    // item de carga y error
    when (loadState) {
        // item de carga
        LoadState.LOADING -> {
            Box(
                modifier = Modifier
                    .fillMaxSize(),
                contentAlignment = Alignment.Center
            ){
                LoadingItem("")
            }
        }
        // item de error de carga
        LoadState.ERROR -> {
            Box(
                modifier = Modifier
                    .fillMaxSize(),
                contentAlignment = Alignment.Center
            ){
                ErrorItem(
                    text = stringResource(id = R.string.list_error)
                )
            }
        }
        LoadState.LOADED -> {
            BasicDialog(
                title = stringResource(id = R.string.candidate_education_error_title),
                content = stringResource(id = R.string.candidate_education_error_msg),
                icon = painterResource(id = R.drawable.error),
                visibilityState = Pair(errorVisibility, viewModel::setErrorVisibility)
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
                        .padding(bottom = 16.dp, top = 10.dp),
                    text = stringResource(id = R.string.education_list_title),
                    fontSize = 25.sp,
                    textAlign = TextAlign.Center
                )

                // campo de formacion
                TextFieldPicker(
                    padding = 0.dp,
                    label = stringResource(id = R.string.candidate_education),
                    setValue = { viewModel.setEducation(education.copy(educationId = educationPicker.getEducationId(it).toUUID()))},
                    textState = Pair(educationName){
                        viewModel.setEducation(education.copy(educationQualification = it))
                        setEducationName(it)
                    },
                    autoCompleteFunction = educationPicker::getEducations,
                    readOnly = !viewModel.isNewEducation(),
                    isError = educationError.educationId,
                )

                // campo de fecha de finalizacion de la formacion
                CustomDatePicker(
                    label = stringResource(id = R.string.candidate_education_completion_date),
                    initialDate = education.completionDate,
                    setDate = { viewModel.setEducation(education.copy(completionDate = it)) },
                    validator = { it.isAfter(LocalDate.now()) },
                    errorMsg = stringResource(id = R.string.candidate_education_start_date_error),
                )

                // botón de guardar
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 10.dp),
                    contentAlignment = Alignment.BottomEnd
                ){
                    TextButton(
                        onClick = {
                            viewModel.saveEducation()
                        }
                    ) {
                        Text(text = stringResource(id = R.string.save_button))
                    }
                }
            }

        }
        // else para acabar el when
        else -> {}
    }



}