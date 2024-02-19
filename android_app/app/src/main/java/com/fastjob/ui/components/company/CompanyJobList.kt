package com.fastjob.ui.components.company

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideIn
import androidx.compose.animation.slideOut
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.fastjob.R
import com.fastjob.ui.components.basic.ErrorItem
import com.fastjob.ui.components.basic.LoadingItem
import com.fastjob.ui.components.job.JobItem
import com.fastjob.ui.effects.JobCompanyListEffect
import com.fastjob.ui.enums.LoadState
import com.fastjob.ui.viewmodels.company.CompanyJobListViewModel

/**
 * Componente de la lista de ofertas de trabajo creadas por la empresa
 * @param itemsRefreshOffset Cantidad de items restantes para refrescar la lista
 * @param viewModel ViewModel de la pantalla de lista de ofertas de trabajo creadas por la empresa
 * @param navController Controlador de navegación
 */
@Composable
fun CompanyJobList(
    itemsRefreshOffset: Int = 1,
    viewModel: CompanyJobListViewModel,
    navController: NavController
) {
    // estado de la carga de la lista
    val loadState by viewModel.loadState.collectAsState()

    // estado del scroll
    val scrollState by viewModel.jobListScroll.collectAsState()

    // lista de trabajos
    val jobList by viewModel.jobList.collectAsState()

    // estado de si se llego al final del scroll
    val isItemReachEndScroll by remember {
        derivedStateOf {
            scrollState.layoutInfo.visibleItemsInfo.lastOrNull()?.index == scrollState.layoutInfo.totalItemsCount - if(scrollState.layoutInfo.totalItemsCount<itemsRefreshOffset) 1 else itemsRefreshOffset
        }
    }

    // efecto que se encarga de actualizar la lista de trabajos
    JobCompanyListEffect(
        loadState = loadState,
        companyJobViewModel = viewModel,
        isItemReachEndScroll = isItemReachEndScroll
    )

    // animacion de la lista de trabajos
    AnimatedVisibility(
        visible = loadState != LoadState.START,
        enter = when(loadState){
            LoadState.LOADED -> slideIn(
                initialOffset = { IntOffset(0, it.height) },
                animationSpec = tween(600)
            )
            else -> fadeIn()
        },
        exit = when(loadState){
            LoadState.LOADED -> slideOut(
                targetOffset = { IntOffset(0, it.height) },
                animationSpec = tween(600)
            )
            else -> fadeOut()
        },
    ) {
        // lista de trabajos
        LazyColumn(
            state = scrollState,
            verticalArrangement = jobList.isEmpty().let {
                if (it) Arrangement.Center
                else Arrangement.spacedBy(4.dp)
            },
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier
                .fillMaxWidth()
                .fillMaxHeight(),
        ) {
            // items de la lista de trabajos
            itemsIndexed(jobList) { index, item ->
                CompanyJobItem(
                    index = index,
                    job = item,
                    navController = navController,
                    deleteJob = {
                        viewModel.deleteJob(it)
                    }
                )
            }

            // item de carga y error
            when (loadState) {
                // item de carga
                LoadState.LOADING -> {
                    item {
                        LoadingItem("")
                    }
                }
                // item de error de candidato no ha aplicado a ningun trabajo
                LoadState.NOT_FOUND -> {
                    item {
                        ErrorItem(
                            text = stringResource(id = R.string.company_job_not_found)
                        )
                    }
                }
                // item de error de carga inesperado
                LoadState.ERROR -> {
                    item {
                        ErrorItem(
                            text = stringResource(id = R.string.list_error)
                        )
                    }
                }
                // else para acabar el when
                else -> {}
            }
        }
    }
}