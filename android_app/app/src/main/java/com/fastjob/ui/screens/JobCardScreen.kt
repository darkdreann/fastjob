package com.fastjob.ui.screens

import android.content.res.Configuration
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.fastjob.auth.AuthAPI
import com.fastjob.models.UserType
import com.fastjob.ui.components.basic.CandidateBottomBar
import com.fastjob.ui.components.job.JobLoader
import com.fastjob.ui.components.basic.TopBar
import com.fastjob.ui.theme.FastjobTheme
import java.util.UUID

/**
 * Pantalla que muestra la información de una oferta de trabajo.
 * @param index Índice de la posición de la oferta de trabajo en la lista.
 * @param jobUUID UUID de la oferta de trabajo.
 */
@Composable
fun JobCardScreen(
    index: Int,
    jobUUID: UUID?,
    navController: NavController
){
    // Se obtiene la instancia de autenticación
    val auth = AuthAPI.getInstance()

    Scaffold(
        topBar = {
            TopBar(navController)
        },
        bottomBar = {
            if(auth.isAuthenticated()) {
                // si esta autenticado pero no contiene el tipo de usuario se muestra la barra de candidato por defecto
                if((auth.getUserType() ?: UserType.CANDIDATE) == (UserType.CANDIDATE)) CandidateBottomBar(navController)
                else CandidateBottomBar(navController)
            }
        }
    ) {
        Column(
            modifier = Modifier.padding(it),
            verticalArrangement = Arrangement.spacedBy(4.dp)
        ){
            JobLoader(
                index = index,
                jobUUID = jobUUID
            )
        }
    }
}

@Preview(showBackground = true)
@Composable
fun JobCardScreenPreview() {
    FastjobTheme {
        JobCardScreen(1,null, NavController(LocalContext.current))
    }
}

@Preview(showBackground = true, uiMode = Configuration.UI_MODE_NIGHT_YES)
@Composable
fun JobCardScreenPreviewDark() {
    FastjobTheme {
        JobCardScreen(2,null, NavController(LocalContext.current))
    }
}