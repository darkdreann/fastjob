package com.fastjob.ui.components.form

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import com.fastjob.R
import com.fastjob.models.Availability
import com.fastjob.ui.components.basic.BasicDialog
import com.fastjob.ui.components.basic.SelectableAvailability
import com.fastjob.ui.components.basic.TextFieldMultiple
import com.fastjob.ui.enums.RegisterState
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.viewmodels.form.user.CreateCandidateViewModel

@Composable
fun CreateCandidateForm(
    viewModel: CreateCandidateViewModel,
    navController: NavController
){

    // estado del formulario de registro
    val registerState by viewModel.registerState.collectAsState()

    // estado del formulario de candidato
    val candidateData by viewModel.candidateData.collectAsState()

    // estado mensajes error
    val (errorVisibility, setErrorVisibility) = remember { mutableStateOf(false) }
    
    when(registerState){
        RegisterState.REGISTERED -> {
            navController.navigate(AppScreens.UserLoginScreen.route)
        }
        RegisterState.FORM_NOT_VALID -> {
            setErrorVisibility(true)
            BasicDialog(
                title = stringResource(id = R.string.candidate_register_error_title),
                content = stringResource(id = R.string.candidate_register_no_form_valid),
                icon = painterResource(id = R.drawable.error),
                visibility = Pair(errorVisibility, setErrorVisibility)
            )
        }
        RegisterState.DUPLICATED_USERNAME -> {
            setErrorVisibility(true)
            BasicDialog(
                title = stringResource(id = R.string.candidate_register_error_title),
                content = stringResource(id = R.string.candidate_register_error_username),
                icon = painterResource(id = R.drawable.error),
                visibility = Pair(errorVisibility, setErrorVisibility)
            )
        }
        RegisterState.DUPLICATED_EMAIL -> {
            setErrorVisibility(true)
            BasicDialog(
                title = stringResource(id = R.string.candidate_register_error_title),
                content = stringResource(id = R.string.candidate_register_error_email),
                icon = painterResource(id = R.drawable.error),
                visibility = Pair(errorVisibility, setErrorVisibility)
            )
        }
        RegisterState.UNKNOWN_ERROR -> {
            setErrorVisibility(true)
            BasicDialog(
                title = stringResource(id = R.string.candidate_register_error_title),
                content = stringResource(id = R.string.candidate_register_error),
                icon = painterResource(id = R.drawable.error),
                visibility = Pair(errorVisibility, setErrorVisibility)
            )
        }
        else -> {}
    }


    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState()),
    ) {
        Image(
            painter = painterResource(id = R.drawable.user_img),
            contentDescription = ""
        )
        Text(
            modifier = Modifier.fillMaxWidth(),
            text = stringResource(id = R.string.candidate_form_title),
            textAlign = TextAlign.Center,
            fontSize = 30.sp
        )

        CreateUserForm(
            viewModel = viewModel
        )

        Row(
            modifier = Modifier.imePadding(),
            horizontalArrangement = Arrangement.spacedBy(4.dp),
        ){
            TextFieldMultiple(
                modifier = Modifier.weight(0.4f),
                label = stringResource(id = R.string.candidate_skill),
                buttonAddText = stringResource(id = R.string.candidate_skill_add),
                itemList = candidateData.skills,
                setList = { viewModel.setSkills(it) },
                itemsCheck = { it.length <= 30 },
                maxListItems = 30,
                maxHeight = 300
            )

            SelectableAvailability(
                modifier = Modifier.weight(0.4f),
                label = stringResource(id = R.string.candidate_availability),
                buttonAddText = stringResource(id = R.string.candidate_availability_add),
                itemPossibilities = Availability.values().toList(),
                itemList = candidateData.availabilities,
                setList = {
                    viewModel.setAvailabilities(it.toSet())
                },
                maxListItems = Availability.values().size,
                maxHeight = 300
            )
        }

        Button(
            onClick = {
                viewModel.registerCandidate()
            }
        ) {
            Text(text = stringResource(id = R.string.user_register_button))
        }

    }
}