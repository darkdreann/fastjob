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
import com.fastjob.ui.components.form.JobLanguageForm
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.viewmodels.company.CompanyLanguageViewModel
import com.fastjob.ui.viewmodels.company.CompanyLanguageViewModelFactory
import java.util.UUID

/**
 * Pantalla de creación de idiomas de una oferta de trabajo
 * @param navController Controlador de navegación
 * @param jobId Identificador de la oferta de trabajo
 */
@Composable
fun CompanyCreateJobLanguageScreen(
    navController: NavController,
    jobId: UUID
) {
    // si no esta autenticado redirigir a login
    if(!CompanyLanguageViewModel.auth.isAuthenticated()) navController.navigate(AppScreens.UserLoginScreen.route)

    // view model
    val viewModel: CompanyLanguageViewModel = viewModel(
        factory = CompanyLanguageViewModelFactory(
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
            JobLanguageForm(
                viewModel = viewModel
            )
        }
    }
}