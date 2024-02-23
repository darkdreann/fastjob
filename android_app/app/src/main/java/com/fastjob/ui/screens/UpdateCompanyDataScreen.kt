package com.fastjob.ui.screens

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.fastjob.ui.components.basic.CompanyBottomBar
import com.fastjob.ui.components.basic.TopBar
import com.fastjob.ui.components.form.UpdateCompanyForm
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.viewmodels.company.UpdateCompanyViewModel
import com.fastjob.ui.viewmodels.company.UpdateCompanyViewModel.CompanyData
import com.fastjob.ui.viewmodels.company.UpdateCompanyViewModelFactory

/**
 * Pantalla de actualización de datos de empresa
 * @param navController controlador de navegación
 * @param currentTin NIT actual de la empresa
 * @param currentCompanyName nombre actual de la empresa
 */
@Composable
fun UpdateCompanyDataScreen(
    navController: NavController,
    currentTin: String,
    currentCompanyName: String
) {
    // Si no esta autenticado se navega a la pantalla de inicio de sesión
    if(!UpdateCompanyViewModel.auth.isAuthenticated()) navController.navigate(AppScreens.UserLoginScreen.route)

    // viewmodel de la pantalla
    val viewModel: UpdateCompanyViewModel = viewModel(
        factory = UpdateCompanyViewModelFactory(
            navController = navController,
            currentCompanyData = CompanyData(
                tin = currentTin,
                companyName = currentCompanyName
            )
        )
    )

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
            UpdateCompanyForm(viewModel)
        }
    }
}