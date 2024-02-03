package com.fastjob.ui.components.form

import android.util.Log
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.expandVertically
import androidx.compose.animation.shrinkVertically
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Checkbox
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import com.fastjob.R
import com.fastjob.ui.components.basic.BasicDialog
import com.fastjob.ui.components.basic.CustomDatePicker
import com.fastjob.ui.components.basic.ErrorItem
import com.fastjob.ui.components.basic.LoadingItem
import com.fastjob.ui.components.basic.TextFieldAutocomplete
import com.fastjob.ui.components.basic.TextFieldPicker
import com.fastjob.ui.enums.LoadState
import com.fastjob.ui.functions.keywords.management.SubcategoryPicker
import com.fastjob.ui.functions.keywords.management.getSectorCategoryKeyword
import com.fastjob.ui.functions.toUUID
import com.fastjob.ui.viewmodels.form.candidate.CandidateExperienceViewModel
import java.time.LocalDate

/**
 * Formulario de experiencia laboral
 * @param viewModel ViewModel del formulario de experiencia
 */
@Composable
fun ExperienceForm(
    viewModel: CandidateExperienceViewModel
) {

    // estado de la experiencia
    val experience by viewModel.experience.collectAsState()

    // estado de error de la experiencia
    val experienceError by viewModel.experienceError.collectAsState()

    // estado de carga
    val loadState by viewModel.loadState.collectAsState()

    // estado del dialogo de error
    val errorVisibility by viewModel.errorVisibility.collectAsState()

    // picker de subcategorias para el autocomplete de subcategorias
    val subCategoryPicker = remember { SubcategoryPicker() }

    // estado checkbox de no fecha de fin
    val notEndDate by viewModel.noEndDateState.collectAsState()

    // estado de la subcategoria
    val (subcategory, setSubcategory) = remember { mutableStateOf(experience.sectorSubcategory) }

    // carga de la experiencia
    LaunchedEffect(Unit){
        viewModel.loadExperience(setSubcategory)
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
                title = stringResource(id = R.string.candidate_experience_error_title),
                content = stringResource(id = R.string.candidate_experience_error_msg),
                icon = painterResource(id = R.drawable.error),
                visibilityState = Pair(errorVisibility, viewModel::setErrorVisibility))

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

                // campo de puesto
                TextField(
                    singleLine = true,
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(15.dp)),
                    label = { Text(stringResource(id = R.string.candidate_experience_job_position)) },
                    value = experience.jobPosition,
                    onValueChange = {
                        // si es menor a 25 caracteres
                        if (it.length <= 25)
                            viewModel.setExperience(experience.copy(jobPosition = it))
                    },
                    isError = experienceError.jobPosition,
                )

                // campo de descripcion del puesto
                TextField(
                    singleLine = true,
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(15.dp)),
                    label = { Text(stringResource(id = R.string.candidate_experience_job_position_desc)) },
                    value = experience.jobPositionDescription,
                    onValueChange = {
                        // si es menor a 200 caracteres
                        if (it.length <= 200)
                            viewModel.setExperience(experience.copy(jobPositionDescription = it))
                    },
                    isError = experienceError.jobPositionDescription,
                )

                // campo de nombre de la empresa
                TextField(
                    singleLine = true,
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(15.dp)),
                    label = { Text(stringResource(id = R.string.candidate_experience_company_name)) },
                    value = experience.companyName,
                    onValueChange = {
                        // si es menor a 30 caracteres
                        if (it.length <= 30)
                            viewModel.setExperience(experience.copy(companyName = it))
                    },
                    isError = experienceError.companyName,
                )

                // campo de sector
                // animacion para el campo de categoria
                AnimatedVisibility(
                    visible = experience.sectorId == null,
                    enter = expandVertically(),
                    exit = shrinkVertically()
                ){
                    // campo de categoria
                    TextFieldAutocomplete(
                        padding = 0.dp,
                        label = stringResource(id = R.string.job_filter_sector_category),
                        textState = Pair(experience.sectorCategory) {
                            viewModel.setExperience(experience.copy(sectorCategory = it))
                            subCategoryPicker.setCategory(it)
                        },
                        autoCompleteFunction = ::getSectorCategoryKeyword,
                        enabled = experience.sectorId == null,
                        isError = experienceError.sectorId,
                    )
                }

                // animacion para el campo de subcategoria
                AnimatedVisibility(
                    visible = experience.sectorCategory.isNotEmpty(),
                    enter = expandVertically(),
                    exit = shrinkVertically()
                ){
                    // campo de subcategoria
                    TextFieldPicker(
                        padding = 0.dp,
                        label = stringResource(id = R.string.job_filter_sector_subcategory),
                        setValue = { viewModel.setExperience(experience.copy(sectorId = subCategoryPicker.getSectorId(it).toUUID()))},
                        textState = Pair(subcategory){
                            viewModel.setExperience(experience.copy(sectorSubcategory = it))
                            setSubcategory(it)
                        },
                        autoCompleteFunction = subCategoryPicker::getSubcategories,
                        enabled = experience.sectorCategory.isNotEmpty(),
                        isError = experienceError.sectorId,
                    )
                }

                // campo de fecha de inicio
                CustomDatePicker(
                    label = stringResource(id = R.string.candidate_experience_start_date),
                    initialDate = experience.startDate,
                    setDate = { viewModel.setExperience(experience.copy(startDate = it)) },
                    validator = { it.isAfter(LocalDate.now()) && it.isAfter(experience.endDate) },
                    errorMsg = stringResource(id = R.string.candidate_experience_start_date_error),
                )

                // campo de fecha de fin
                AnimatedVisibility(
                    visible = !notEndDate,
                    enter = expandVertically(),
                    exit = shrinkVertically()
                ){
                    CustomDatePicker(
                        label = stringResource(id = R.string.candidate_experience_end_date),
                        initialDate = experience.endDate,
                        setDate = { viewModel.setExperience(experience.copy(endDate = it)) },
                        validator = { it.isAfter(LocalDate.now()) },
                        errorMsg = stringResource(id = R.string.candidate_experience_end_date_error),
                    )
                }
                Row(
                    modifier = Modifier
                        .fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.Start
                ) {
                    Checkbox(
                        checked = notEndDate,
                        onCheckedChange = { newChecked ->
                            viewModel.setNoEndDateState(newChecked)
                            viewModel.setExperience(experience.copy(endDate = null))
                        }
                    )
                    Text(text = stringResource(id = R.string.candidate_experience_no_end_date))
                }
                // botón de guardar
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 10.dp),
                    contentAlignment = Alignment.BottomEnd
                ){
                    TextButton(
                        onClick = {
                            viewModel.saveExperience()
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