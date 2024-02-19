package com.fastjob.ui.screens

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.IconButtonDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.fastjob.R
import com.fastjob.ui.components.basic.CompanyBottomBar
import com.fastjob.ui.components.basic.TopBar
import com.fastjob.ui.components.company.CompanyJobList
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.viewmodels.company.CompanyJobListViewModel
import kotlinx.coroutines.launch

/**
 * Pantalla de la lista de ofertas de trabajo creadas por la empresa
 * @param navController Controlador de navegación
 */
@Composable
fun CompanyJobsListScreen(
    navController: NavController
){
    // Si no esta autenticado se navega a la pantalla de inicio de sesión
    if(!CompanyJobListViewModel.auth.isAuthenticated()) navController.navigate(AppScreens.UserLoginScreen.route)

    // Se obtiene el viewmodel de la pantalla
    val viewModel = viewModel<CompanyJobListViewModel>()

    // Se obtiene el scope de la corrutina
    val coroutineScope = rememberCoroutineScope()

    Scaffold(
        modifier = Modifier.fillMaxSize(),
        topBar = {
            TopBar(navController)
        },
        bottomBar = {
            CompanyBottomBar(navController)
        },
        floatingActionButton = {
            IconButton(
                onClick = {
                    coroutineScope.launch {
                        viewModel.jobListScroll.value.animateScrollToItem(0)
                    }
                },
                colors = IconButtonDefaults.iconButtonColors(
                    containerColor = MaterialTheme.colorScheme.secondary,
                    contentColor = MaterialTheme.colorScheme.tertiary
                )
            ) {
                Icon(
                    painter = painterResource(id = R.drawable.up),
                    contentDescription = stringResource(id = R.string.job_list_screen_float_button_icon_desc),
                )
            }
        }
    ) {
        Column(
            modifier = Modifier.padding(it),
        ){
            CompanyJobList(
                itemsRefreshOffset = 3,
                viewModel = viewModel,
                navController = navController
            )
        }
    }
}