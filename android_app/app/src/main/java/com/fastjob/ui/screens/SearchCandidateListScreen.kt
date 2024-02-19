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
import com.fastjob.ui.components.company.CandidateFilter
import com.fastjob.ui.components.company.SearchCandidateList
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.viewmodels.search.CandidateSearchViewModel
import com.fastjob.ui.viewmodels.search.CandidateSearchViewModelFactory
import java.util.UUID

/**
 * Pantalla de la lista de candidatos
 * @param navController Controlador de navegacion
 * @param jobId Id de la oferta de trabajo
 */
@Composable
fun SearchCandidateListScreen(
    navController: NavController,
    jobId: UUID
) {
    // si no esta autenticado redirigir a login
    if(!CandidateSearchViewModel.auth.isAuthenticated()) navController.navigate(AppScreens.UserLoginScreen.route)

    // view model
    val viewModel: CandidateSearchViewModel = viewModel(
        factory = CandidateSearchViewModelFactory(
            jobId = jobId
        )
    )

    Scaffold(
        topBar = {
            TopBar(navController)
        },
        bottomBar = {
            CompanyBottomBar(navController)
        },
        floatingActionButton = {
            CandidateFilter(
                viewModel = viewModel
            )
        }
    ) {
        Box(
            modifier = Modifier.padding(it)
        ){
            SearchCandidateList(
                itemsRefreshOffset = 3,
                candidateSearchViewModel = viewModel,
                navController = navController
            )
        }
    }
}