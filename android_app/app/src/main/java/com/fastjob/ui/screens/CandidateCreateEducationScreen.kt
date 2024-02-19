package com.fastjob.ui.screens

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.fastjob.ui.components.basic.CandidateBottomBar
import com.fastjob.ui.components.basic.TopBar
import com.fastjob.ui.components.form.CandidateEducationForm
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.viewmodels.candidate.CandidateEducationViewModel
import com.fastjob.ui.viewmodels.candidate.CandidateEducationViewModelFactory
import java.util.UUID

@Composable
fun CandidateCreateEducationScreen(
    navController: NavController,
    experienceId: UUID? = null
) {
    // si no esta autenticado redirigir a login
    if(!CandidateEducationViewModel.auth.isAuthenticated()) navController.navigate(AppScreens.UserLoginScreen.route)

    // view model
    val viewModel: CandidateEducationViewModel = viewModel(
        factory = CandidateEducationViewModelFactory(
            navController = navController,
            id = experienceId
        )
    )
    Scaffold(
        topBar = {
            TopBar(navController)
        },
        bottomBar = {
            CandidateBottomBar(navController)
        }
    ) {
        Box(
            modifier = Modifier.padding(it)
        ){
            CandidateEducationForm(
                viewModel = viewModel,
            )
        }
    }
}