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
import com.fastjob.ui.components.company.CandidateCardExperienceList
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.viewmodels.candidate.ExperienceListViewModel
import com.fastjob.ui.viewmodels.company.CandidateCardExperienceListViewModel
import com.fastjob.ui.viewmodels.company.CandidateCardExperienceListViewModelFactory
import java.util.UUID

/**
 * Pantalla que muestra la información de una oferta de trabajo.
 * @param navController controlador de navegación
 * @param jobId id de la oferta de trabajo
 * @param candidateId id del candidato
 */
@Composable
fun CandidateCardExperiencesScreen(
    navController: NavController,
    jobId: UUID,
    candidateId: UUID
){
    // si no esta autenticado redirigir a login
    if(!ExperienceListViewModel.auth.isAuthenticated()) navController.navigate(AppScreens.UserLoginScreen.route)

    // view model
    val viewModel: CandidateCardExperienceListViewModel = viewModel(
        factory = CandidateCardExperienceListViewModelFactory(
            jobId = jobId,
            candidateId = candidateId
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
            CandidateCardExperienceList(
                itemsRefreshOffset = 3,
                viewModel = viewModel
            )
        }
    }
}