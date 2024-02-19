package com.fastjob.ui.screens

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.fastjob.ui.components.basic.TopBar
import com.fastjob.ui.components.form.LoginUser
import com.fastjob.ui.viewmodels.login.LoginViewModel


@Composable
fun UserLoginScreen(
    navController: NavController
) {
    val viewModel = viewModel<LoginViewModel>()


    Scaffold(
        topBar = {
            TopBar(navController, true)
        },
    ){
        Box(
            modifier = Modifier.padding(it)
        ){
            LoginUser(
                viewModel = viewModel,
                navController = navController
            )
        }
    }
}