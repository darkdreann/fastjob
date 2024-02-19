package com.fastjob.ui.screens

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.fastjob.ui.components.basic.CandidateBottomBar
import com.fastjob.ui.components.basic.CompanyBottomBar
import com.fastjob.ui.components.basic.TopBar
import com.fastjob.ui.components.profile.CompanyProfile
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.viewmodels.profile.CompanyProfileViewModel

/**
 * Pantalla de perfil de empresa
 * @param navController controlador de navegación
 */
@Composable
fun CompanyProfileScreen(
    navController: NavController
) {
    // Si no esta autenticado se navega a la pantalla de inicio de sesión
    if(!CompanyProfileViewModel.auth.isAuthenticated()) navController.navigate(AppScreens.UserLoginScreen.route)

    // viewmodel de la pantalla
    val viewModel = viewModel<CompanyProfileViewModel>()

    Scaffold(
        modifier = Modifier.fillMaxSize(),
        topBar = {
            TopBar(navController)
        },
        bottomBar = {
            CompanyBottomBar(navController)
        },
    ){
        Box(
            modifier = Modifier.padding(it)
        ){
            CompanyProfile(navController, viewModel)
        }
    }
}