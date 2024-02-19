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
import com.fastjob.ui.components.company.CandidateLoader
import com.fastjob.ui.viewmodels.company.CandidateCardViewModel
import java.util.UUID

/**
 * Pantalla que muestra la información de un candidato.
 * @param index Índice del candidato
 * @param jobId UUID de la oferta
 * @param candidateId UUID del candidato
 * @param navController controlador de navegación
 */
@Composable
fun CandidateCardScreen(
    index: Int,
    jobId: UUID,
    candidateId: UUID,
    navController: NavController
){
    // view model
    val viewModel = viewModel<CandidateCardViewModel>()

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
            CandidateLoader(
                index = index,
                jobId = jobId,
                candidateId = candidateId,
                viewModel = viewModel,
                navController = navController
            )
        }
    }
}