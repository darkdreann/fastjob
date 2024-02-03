package com.fastjob.ui.components.form

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
import com.fastjob.models.Availability
import com.fastjob.ui.components.basic.BasicDialog
import com.fastjob.ui.components.basic.SelectableAvailability
import com.fastjob.ui.components.basic.TextFieldMultiple
import com.fastjob.ui.viewmodels.form.candidate.UpdateSkillAvailabilityViewModel

@Composable
fun UpdateSkillsAvailabilitiesForm(
    viewModel: UpdateSkillAvailabilityViewModel
) {

    // estado de las jornadas
    val availabilities by viewModel.availabilities.collectAsState()

    // estado de las habilidades
    val skills by viewModel.skills.collectAsState()

    // visibilidad del error
    val errorVisibility by viewModel.errorVisibility.collectAsState()

    // dialogo de error
    BasicDialog(
        title = stringResource(id = R.string.user_skill_availability_update_error_title),
        content = stringResource(id = R.string.user_skill_availability_update_error_msg),
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
        // nombre de usuario
        Text(
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 5.dp),
            text = stringResource(id = R.string.update_skill_availabilty),
            textAlign = TextAlign.Center,
            fontSize = 30.sp
        )

        Row(
            modifier = Modifier.imePadding(),
            horizontalArrangement = Arrangement.spacedBy(4.dp),
        ){
            // grupo de textfield de habilidades
            TextFieldMultiple(
                modifier = Modifier.weight(0.4f),
                label = stringResource(id = R.string.candidate_skill),
                buttonAddText = stringResource(id = R.string.candidate_skill_add),
                itemList = skills,
                setList = { viewModel.setSkills(it) },
                itemsCheck = { it.length <= 30 },
                maxListItems = 30,
                maxHeight = 300
            )

            // grupo de selección de disponibilidad
            SelectableAvailability(
                modifier = Modifier.weight(0.4f),
                label = stringResource(id = R.string.candidate_availability),
                buttonAddText = stringResource(id = R.string.candidate_availability_add),
                itemPossibilities = Availability.values().toList(),
                itemList = availabilities,
                setList = {
                    viewModel.setAvailabilities(it.toSet())
                },
                maxListItems = Availability.values().size,
                maxHeight = 300
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
                    viewModel.updateCandidateSkillsAvailabilities()
                }
            ) {
                Text(text = stringResource(id = R.string.update_button))
            }
        }


    }




}