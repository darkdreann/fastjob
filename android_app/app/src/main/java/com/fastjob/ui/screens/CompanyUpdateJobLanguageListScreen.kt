package com.fastjob.ui.screens

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.IconButtonDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.fastjob.R
import com.fastjob.ui.components.basic.CompanyBottomBar
import com.fastjob.ui.components.basic.TopBar
import com.fastjob.ui.components.company.JobLanguageList
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.viewmodels.company.JobLanguageListViewModel
import com.fastjob.ui.viewmodels.company.JobLanguageListViewModelFactory
import java.util.UUID

/**
 * Pantalla de lista de idiomas de un trabajo
 * @param navController controlador de navegación
 * @param jobId id del trabajo
 */
@Composable
fun CompanyJobLanguageListScreen(
    navController: NavController,
    jobId: UUID
) {
    // si no esta autenticado redirigir a login
    if(!JobLanguageListViewModel.auth.isAuthenticated()) navController.navigate(AppScreens.UserLoginScreen.route)

    // view model
    val viewModel: JobLanguageListViewModel = viewModel(
        factory = JobLanguageListViewModelFactory(
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
            IconButton(
                onClick = {
                    navController.navigate(AppScreens.CompanyUpdateJobLanguageScreen.route + "/$jobId")
                },
                colors = IconButtonDefaults.iconButtonColors(
                    containerColor = MaterialTheme.colorScheme.secondary,
                    contentColor = MaterialTheme.colorScheme.tertiary
                )
            ) {
                Icon(
                    painter = painterResource(id = R.drawable.add),
                    contentDescription = stringResource(id = R.string.candidate_language_button_create),
                )
            }
        }
    ) {
        Box(
            modifier = Modifier.padding(it)
        ){
            JobLanguageList(
                itemsRefreshOffset = 3,
                viewModel = viewModel,
                navController = navController
            )
        }
    }
}