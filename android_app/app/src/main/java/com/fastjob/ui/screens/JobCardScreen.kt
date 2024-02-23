package com.fastjob.ui.screens

import android.content.res.Configuration
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.tooling.preview.Preview
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.fastjob.ui.components.basic.CandidateBottomBar
import com.fastjob.ui.components.basic.TopBar
import com.fastjob.ui.components.job.JobLoader
import com.fastjob.ui.theme.FastjobTheme
import com.fastjob.ui.viewmodels.job.JobCardViewModel
import java.util.UUID

/**
 * Pantalla que muestra la información de una oferta de trabajo.
 * @param index Índice de la posición de la oferta de trabajo en la lista.
 * @param jobUUID UUID de la oferta de trabajo.
 * @param navController controlador de navegación.
 */
@Composable
fun JobCardScreen(
    index: Int,
    jobUUID: UUID?,
    navController: NavController
){
    // view model
    val viewModel = viewModel<JobCardViewModel>()

    Scaffold(
        topBar = {
            TopBar(navController)
        },
        bottomBar = {
            if(JobCardViewModel.auth.isAuthenticated())
                CandidateBottomBar(navController)
        }
    ) {
        Box(
            modifier = Modifier.padding(it)
        ){
            JobLoader(
                index = index,
                jobUUID = jobUUID,
                viewModel = viewModel
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