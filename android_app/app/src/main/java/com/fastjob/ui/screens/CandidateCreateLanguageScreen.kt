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
import com.fastjob.ui.components.form.CandidateLanguageForm
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.viewmodels.candidate.CandidateEducationViewModel
import com.fastjob.ui.viewmodels.candidate.CandidateLanguageViewModel
import com.fastjob.ui.viewmodels.candidate.CandidateLanguageViewModelFactory
import java.util.UUID

/**
 * Pantalla para crear o editar el idioma del candidato
 * @param navController controlador de navegación
 * @param experienceId id de la experiencia
 */
@Composable
fun CandidateCreateLanguageScreen(
    navController: NavController,
    experienceId: UUID? = null
) {
    // si no esta autenticado redirigir a login
    if(!CandidateEducationViewModel.auth.isAuthenticated()) navController.navigate(AppScreens.UserLoginScreen.route)

    // view model
    val viewModel: CandidateLanguageViewModel = viewModel(
        factory = CandidateLanguageViewModelFactory(
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
            CandidateLanguageForm(
                viewModel = viewModel,
            )
        }
    }
}