package com.fastjob.ui.screens

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.fastjob.models.Availability
import com.fastjob.ui.components.basic.CandidateBottomBar
import com.fastjob.ui.components.basic.TopBar
import com.fastjob.ui.components.form.UpdateSkillsAvailabilitiesForm
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.viewmodels.candidate.UpdateSkillAvailabilityViewModel
import com.fastjob.ui.viewmodels.candidate.UpdateSkillAvailabilityViewModelFactory
import com.fastjob.ui.viewmodels.profile.CandidateProfileViewModel

/**
 * Pantalla de actualización de habilidades y disponibilidad del candidato
 * @param navController controlador de navegación
 * @param skills lista de habilidades del candidato
 * @param availabilities lista de disponibilidades del candidato
 */
@Composable
fun CandidateSkillsAvailabilitiesUpdateScreen(
    navController: NavController,
    skills: List<String>,
    availabilities: List<Availability>,
) {
    // Si no esta autenticado se navega a la pantalla de inicio de sesión
    if(!CandidateProfileViewModel.auth.isAuthenticated()) navController.navigate(AppScreens.UserLoginScreen.route)

    // viewmodel de la pantalla
    val viewModel: UpdateSkillAvailabilityViewModel = viewModel(
        factory = UpdateSkillAvailabilityViewModelFactory(
            navController = navController,
            currentAvailabilities = availabilities,
            currentSkills = skills
        )
    )

    Scaffold(
        modifier = Modifier.fillMaxSize(),
        topBar = {
            TopBar(navController)
        },
        bottomBar = {
            CandidateBottomBar(navController)
        },
    ){
        Box(
            modifier = Modifier.padding(it)
        ){
            UpdateSkillsAvailabilitiesForm(viewModel)
        }
    }
}