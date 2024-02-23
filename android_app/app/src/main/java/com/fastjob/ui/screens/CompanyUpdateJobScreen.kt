package com.fastjob.ui.screens

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.fastjob.ui.components.basic.CompanyBottomBar
import com.fastjob.ui.components.basic.TopBar
import com.fastjob.ui.components.form.UpdateJobForm
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.viewmodels.company.UpdateCompanyJobViewModel
import com.fastjob.ui.viewmodels.company.UpdateCompanyJobViewModelFactory
import java.util.UUID

/**
 * Pantalla de actualización de un trabajo
 * @param navController controlador de navegación
 * @param jobId id del trabajo
 */
@Composable
fun CompanyUpdateJobScreen(
    navController: NavController,
    jobId: UUID
) {
    // si no esta autenticado redirigir a login
    if(!UpdateCompanyJobViewModel.auth.isAuthenticated()) navController.navigate(AppScreens.UserLoginScreen.route)

    // view model
    val viewModel: UpdateCompanyJobViewModel = viewModel(
        factory = UpdateCompanyJobViewModelFactory(
            navController = navController,
            jobId = jobId
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
            UpdateJobForm(
                viewModel = viewModel,
            )
        }
    }
}