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
import com.fastjob.ui.components.basic.CandidateBottomBar
import com.fastjob.ui.components.basic.TopBar
import com.fastjob.ui.components.candidate.ExperienceList
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.viewmodels.form.candidate.ExperienceListViewModel

/**
 * Pantalla que muestra la información de una oferta de trabajo.
 */
@Composable
fun CandidateExperiencesScreen(
    navController: NavController
){
    // si no esta autenticado redirigir a login
    if(!ExperienceListViewModel.auth.isAuthenticated()) navController.navigate(AppScreens.UserLoginScreen.route)

    // view model
    val viewModel = viewModel<ExperienceListViewModel>()

    Scaffold(
        topBar = {
            TopBar(navController)
        },
        bottomBar = {
            CandidateBottomBar(navController)
        },
        floatingActionButton = {
            IconButton(
                onClick = {
                    navController.navigate(AppScreens.CandidateEditExperienceScreen.route)
                },
                colors = IconButtonDefaults.iconButtonColors(
                    containerColor = MaterialTheme.colorScheme.secondary,
                    contentColor = MaterialTheme.colorScheme.tertiary
                )
            ) {
                Icon(
                    painter = painterResource(id = R.drawable.add),
                    contentDescription = stringResource(id = R.string.candidate_experience_button_create),
                )
            }
        }
    ) {
        Box(
            modifier = Modifier.padding(it)
        ){
            ExperienceList(
                itemsRefreshOffset = 3,
                viewModel = viewModel,
                navController = navController
            )
        }
    }
}