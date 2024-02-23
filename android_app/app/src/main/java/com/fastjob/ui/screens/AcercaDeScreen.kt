package com.fastjob.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.fastjob.R
import com.fastjob.auth.AuthAPI
import com.fastjob.models.UserType
import com.fastjob.ui.components.basic.CandidateBottomBar
import com.fastjob.ui.components.basic.CompanyBottomBar
import com.fastjob.ui.components.basic.TopBar

/**
 * Pantalla de Acerca de
 * @param navController controlador de navegación
 */
@Composable
fun AcercaDeScreen(
    navController: NavController,
){
    // instancia de AuthAPI
    val auth = AuthAPI.getInstance()

    Scaffold(
        topBar = {
            TopBar(navController)
        },
        bottomBar = {
            if(auth.getUserType() == UserType.CANDIDATE) CandidateBottomBar(navController)
            else CompanyBottomBar(navController)
        }
    ) {
        Box(
            modifier = Modifier.padding(it)
        ){
            Column(
                modifier = Modifier.padding(horizontal = 16.dp, vertical = 30.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ){
                Text(text = stringResource(id = R.string.alumno))
                Text(text = stringResource(id = R.string.centro))
            }
        }
    }
}