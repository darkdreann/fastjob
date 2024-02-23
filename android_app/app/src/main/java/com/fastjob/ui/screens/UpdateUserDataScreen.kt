package com.fastjob.ui.screens

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.fastjob.models.UserType
import com.fastjob.ui.components.basic.CandidateBottomBar
import com.fastjob.ui.components.basic.CompanyBottomBar
import com.fastjob.ui.components.basic.TopBar
import com.fastjob.ui.components.form.UpdateUserForm
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.viewmodels.profile.CandidateProfileViewModel
import com.fastjob.ui.viewmodels.user.UpdateUserViewModel
import com.fastjob.ui.viewmodels.user.UpdateUserViewModelFactory

/**
 * Pantalla de actualización de datos de usuario
 * @param currentUserData Datos del usuario actual
 * @param navController Controlador de navegación
 */
@Composable
fun UpdateUserDataScreen(
    currentUserData: UpdateUserViewModel.UserData,
    navController: NavController
) {
    // Si no esta autenticado se navega a la pantalla de inicio de sesión
    if(!CandidateProfileViewModel.auth.isAuthenticated()) navController.navigate(AppScreens.UserLoginScreen.route)

    // viewmodel de la pantalla
    val viewModel: UpdateUserViewModel = viewModel(
        factory = UpdateUserViewModelFactory(
            navController = navController,
            currentUserData = currentUserData
        )
    )

    Scaffold(
        modifier = Modifier.fillMaxSize(),
        topBar = {
            TopBar(navController)
        },
        bottomBar = {
            if(CandidateProfileViewModel.auth.getUserType() == UserType.CANDIDATE) CandidateBottomBar(navController)
            else CompanyBottomBar(navController)
        },
    ){
        Box(
            modifier = Modifier.padding(it)
        ){
            UpdateUserForm(viewModel)
        }
    }
}