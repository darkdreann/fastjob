package com.fastjob.ui.components.form

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.expandVertically
import androidx.compose.animation.shrinkVertically
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.Checkbox
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.core.text.isDigitsOnly
import com.fastjob.R
import com.fastjob.models.Availability
import com.fastjob.ui.components.basic.SelectableAvailability
import com.fastjob.ui.components.basic.TextFieldAutocomplete
import com.fastjob.ui.components.basic.TextFieldMultiple
import com.fastjob.ui.components.basic.TextFieldPicker
import com.fastjob.ui.functions.keywords.management.SubcategoryPicker
import com.fastjob.ui.functions.keywords.management.getSectorCategoryKeyword
import com.fastjob.ui.functions.toUUID
import com.fastjob.ui.viewmodels.interfaces.JobForm

/**
 * Formulario básico de oferta de trabajo
 * @param viewModel ViewModel del formulario
 */
@Composable
fun BasicJobForm(
    viewModel: JobForm
){
    // estado del formulario de oferta de trabajo
    val jobData by viewModel.jobData.collectAsState()

    // estado de los errores del formulario de oferta de trabajo
    val jobDataError by viewModel.jobDataError.collectAsState()

    // picker de subcategorias para el autocomplete de subcategorias
    val subCategoryPicker = remember { SubcategoryPicker() }

    // estado de la subCategoria del sector
    val (subCategory, setSubCategory) = remember { mutableStateOf(jobData.sectorSubcategory) }


    Column(
        modifier = Modifier
            .fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    )
    {
        // textfield del titulo
        TextField(
            singleLine = true,
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(15.dp)),
            label = { Text(stringResource(id = R.string.job_form_title)) },
            value = jobData.title,
            onValueChange = {
                // si es un numero y tiene menos de 5 digitos se cambia el codigo postal
                if (it.length <= 30) {
                    viewModel.setJobData(jobData.copy(title = it))
                }
                // si el titulo esta vacio se muestra el error
                viewModel.setJobDataError(jobDataError.copy(title = it.isEmpty()))
            },
            isError = jobDataError.title,
        )
        if(jobDataError.title){
            Text(
                text = stringResource(id = R.string.job_form_title_error),
                color = MaterialTheme.colorScheme.error,
            )
        }

        // textfield de la descripcion
        TextField(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(15.dp)),
            label = { Text(stringResource(id = R.string.job_form_desc)) },
            value = jobData.description,
            onValueChange = {
                // si es un numero y tiene menos de 5 digitos se cambia el codigo postal
                if (it.length <= 200) {
                    viewModel.setJobData(jobData.copy(description = it))
                }
                // si el titulo esta vacio se muestra el error
                viewModel.setJobDataError(jobDataError.copy(description = it.isEmpty()))
            },
            isError = jobDataError.description,
        )
        if(jobDataError.description){
            Text(
                text = stringResource(id = R.string.job_form_desc_error),
                color = MaterialTheme.colorScheme.error,
            )
        }

        // textfield de la experiencia requerida
        TextField(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(15.dp)),
            label = { Text(stringResource(id = R.string.job_form_experience)) },
            value = jobData.requiredExperience,
            onValueChange = {
                // si es un numero y tiene menos de 5 digitos se cambia
                if (it.length <= 5 && it.isDigitsOnly()) {
                    viewModel.setJobData(jobData.copy(requiredExperience = it))
                }
            },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
        )

        Column(
            modifier = Modifier
                .fillMaxWidth(),
            verticalArrangement = Arrangement.spacedBy(6.dp)
        ){
            // campo de sector
            // animacion para el campo de categoria
            AnimatedVisibility(
                visible = jobData.sectorId == null,
                enter = expandVertically(),
                exit = shrinkVertically()
            ) {
                // campo de categoria
                TextFieldAutocomplete(
                    padding = 0.dp,
                    label = stringResource(id = R.string.job_filter_sector_category),
                    textState = Pair(jobData.sectorCategory) {
                        viewModel.setJobData(jobData.copy(sectorCategory = it))
                        subCategoryPicker.setCategory(it)
                    },
                    autoCompleteFunction = ::getSectorCategoryKeyword,
                    enabled = jobData.sectorId == null,
                    isError = jobDataError.sectorId,
                )
            }

            // animacion para el campo de subcategoria
            AnimatedVisibility(
                visible = jobData.sectorCategory.isNotEmpty(),
                enter = expandVertically(),
                exit = shrinkVertically()
            ) {
                // campo de subcategoria
                TextFieldPicker(
                    padding = 0.dp,
                    label = stringResource(id = R.string.job_filter_sector_subcategory),
                    setValue = {
                        viewModel.setJobData(
                            jobData.copy(
                                sectorId = subCategoryPicker.getSectorId(
                                    it
                                ).toUUID()
                            )
                        )
                    },
                    textState = Pair(subCategory) {
                        viewModel.setJobData(jobData.copy(sectorSubcategory = it))
                        setSubCategory(it)
                    },
                    autoCompleteFunction = subCategoryPicker::getSubcategories,
                    enabled = jobData.sectorCategory.isNotEmpty(),
                    isError = jobDataError.sectorId,
                )
            }
        }


        // grupo de textfield de habilidades
        TextFieldMultiple(
            label = stringResource(id = R.string.candidate_skill),
            buttonAddText = stringResource(id = R.string.candidate_skill_add),
            itemList = jobData.skills,
            setList = { viewModel.setJobData(jobData.copy(skills = it)) },
            itemsCheck = { it.length <= 30 },
            maxListItems = 20,
            maxHeight = 250
        )

        // selección de disponibilidad
        SelectableAvailability(
            label = stringResource(id = R.string.candidate_availability),
            buttonAddText = stringResource(id = R.string.candidate_availability_add),
            itemPossibilities = Availability.values().toList(),
            itemList = listOf(jobData.workSchedule),
            setList = {
                viewModel.setJobData(jobData.copy(workSchedule = if(it.isEmpty()) Availability.ANY else it.first()))
            },
            maxListItems = 0,
            maxHeight = 300
        )


        // checkbox oferta activa
        Row(
            modifier = Modifier
                .fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.Start
        ) {
            Checkbox(
                checked = jobData.active,
                onCheckedChange = { newChecked ->
                    viewModel.setJobData(jobData.copy(active = newChecked))
                }
            )
            Text(text = stringResource(id = R.string.job_form_active))
        }

    }
}