package com.fastjob.ui.screens

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.fastjob.ui.components.basic.CandidateBottomBar
import com.fastjob.ui.components.basic.CompanyBottomBar
import com.fastjob.ui.components.basic.TopBar
import com.fastjob.ui.components.form.CreateJobForm
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.viewmodels.candidate.CandidateExperienceViewModel
import com.fastjob.ui.viewmodels.candidate.CandidateExperienceViewModelFactory
import com.fastjob.ui.viewmodels.company.CreateCompanyJobViewModel
import com.fastjob.ui.viewmodels.company.CreateCompanyJobViewModelFactory

@Composable
fun CompanyCreateJobScreen(
    navController: NavController
) {
    // si no esta autenticado redirigir a login
    if(!CreateCompanyJobViewModel.auth.isAuthenticated()) navController.navigate(AppScreens.UserLoginScreen.route)

    // view model
    val viewModel: CreateCompanyJobViewModel = viewModel(
        factory = CreateCompanyJobViewModelFactory(
            navController = navController
        )
    )

    Scaffold(
        topBar = {
            TopBar(navController)
        },
        bottomBar = {
            CompanyBottomBar(navController)
        }
    ) {
        Box(
            modifier = Modifier.padding(it)
        ){
            CreateJobForm(
                viewModel = viewModel,
            )
        }
    }
}