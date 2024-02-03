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
import com.fastjob.ui.components.basic.TopBar
import com.fastjob.ui.components.form.UpdatePasswordForm
import com.fastjob.ui.components.form.UpdateUserForm
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.viewmodels.form.user.UpdatePasswordViewModel
import com.fastjob.ui.viewmodels.form.user.UpdatePasswordViewModelFactory
import com.fastjob.ui.viewmodels.profile.CandidateProfileViewModel

@Composable
fun UpdateUserPasswordScreen(
    navController: NavController
) {
    // Si no esta autenticado se navega a la pantalla de inicio de sesión
    if(!CandidateProfileViewModel.auth.isAuthenticated()) navController.navigate(AppScreens.UserLoginScreen.route)

    // viewmodel de la pantalla
    val viewModel: UpdatePasswordViewModel = viewModel(
        factory = UpdatePasswordViewModelFactory(
            navController = navController,
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
            UpdatePasswordForm(viewModel)
        }
    }
}