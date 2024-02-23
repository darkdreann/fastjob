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
import com.fastjob.ui.components.form.ExperienceForm
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.viewmodels.candidate.CandidateExperienceViewModel
import com.fastjob.ui.viewmodels.candidate.CandidateExperienceViewModelFactory
import com.fastjob.ui.viewmodels.candidate.ExperienceListViewModel
import java.util.UUID

/**
 * Pantalla para crear o editar la experiencia del candidato
 * @param navController controlador de navegación
 * @param experienceId id de la experiencia
 */
@Composable
fun CandidateCreateExperienceScreen(
    navController: NavController,
    experienceId: UUID? = null
) {
    // si no esta autenticado redirigir a login
    if(!ExperienceListViewModel.auth.isAuthenticated()) navController.navigate(AppScreens.UserLoginScreen.route)

    // view model
    val viewModel: CandidateExperienceViewModel = viewModel(
        factory = CandidateExperienceViewModelFactory(
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
            ExperienceForm(
                viewModel = viewModel,
            )
        }
    }
}