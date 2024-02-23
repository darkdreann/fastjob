package com.fastjob.ui.screens

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.fastjob.ui.components.basic.TopBar
import com.fastjob.ui.components.form.CreateCompanyForm
import com.fastjob.ui.viewmodels.user.CreateCompanyViewModel

/**
 * Pantalla de creación de usuario company
 * @param navController controlador de navegación
 */
@Composable
fun UserCompanyRegisterScreen(
    navController: NavController
){
    // viewmodel de la pantalla de creación de usuario
    val viewModel = viewModel<CreateCompanyViewModel>()

    Scaffold(
        topBar = {
            TopBar(navController)
        },
    ){
        // Se muestra el formulario de creación de company
        Box(
            modifier = Modifier
                .padding(it)
                .padding(vertical = 5.dp, horizontal = 10.dp)
        ){
            CreateCompanyForm(
                viewModel = viewModel,
                navController = navController
            )
        }
    }




}


