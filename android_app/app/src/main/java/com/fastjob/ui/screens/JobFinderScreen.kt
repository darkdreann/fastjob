package com.fastjob.ui.screens


import android.content.res.Configuration
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.IconButtonDefaults
import androidx.compose.material3.MaterialTheme.colorScheme
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import androidx.navigation.compose.rememberNavController
import com.fastjob.R
import com.fastjob.auth.AuthAPI
import com.fastjob.models.UserType
import com.fastjob.ui.components.basic.CandidateBottomBar
import com.fastjob.ui.components.job.SearchJobList
import com.fastjob.ui.components.job.JobSearch
import com.fastjob.ui.components.basic.TopBar
import com.fastjob.ui.theme.FastjobTheme
import com.fastjob.ui.viewmodels.search.JobSearchViewModel
import kotlinx.coroutines.launch

/**
 * Pantalla inicial de la aplicación y que contiene las busquedas y la lista de ofertas de trabajo
 * @param navController controlador de navegación
 */
@Composable
fun JobFinderScreen(
    navController: NavController
){
    // Se obtiene la instancia de autenticación
    val auth = AuthAPI.getInstance()

    // Se obtiene el viewmodel de la pantalla
    val viewModel = viewModel<JobSearchViewModel>()

    // Se obtiene el scope de la corrutina
    val coroutineScope = rememberCoroutineScope()

    Scaffold(
        modifier = Modifier.fillMaxSize(),
        topBar = {
            TopBar(navController)
        },
        bottomBar = {
            if(auth.isAuthenticated() && auth.getUserType() == (UserType.CANDIDATE))
                CandidateBottomBar(navController)
        },
        floatingActionButton = {
            IconButton(
                onClick = {
                    coroutineScope.launch {
                        viewModel.jobListScroll.value.animateScrollToItem(0)
                    }
                },
                colors = IconButtonDefaults.iconButtonColors(
                    containerColor = colorScheme.secondary,
                    contentColor = colorScheme.tertiary
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
            verticalArrangement = Arrangement.spacedBy(4.dp)
        ){
            JobSearch(viewModel)
            SearchJobList(
                itemsRefreshOffset = 3,
                jobSearchViewModel = viewModel,
                navController = navController
            )
        }
    }
}
@Preview(showBackground = true)
@Composable
fun JobFinderScreenPreview() {
    FastjobTheme {
        JobFinderScreen(rememberNavController())
    }
}

@Preview(showBackground = true, uiMode = Configuration.UI_MODE_NIGHT_YES)
@Composable
fun JobFinderScreenPreviewDark() {
    FastjobTheme {
        JobFinderScreen(rememberNavController())
    }
}
