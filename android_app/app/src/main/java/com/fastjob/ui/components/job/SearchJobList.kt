package com.fastjob.ui.components.job

import android.content.res.Configuration
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
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import androidx.navigation.compose.rememberNavController
import com.fastjob.R
import com.fastjob.ui.components.basic.ErrorItem
import com.fastjob.ui.components.basic.LoadingItem
import com.fastjob.ui.effects.JobSearchListEffect
import com.fastjob.ui.theme.FastjobTheme
import com.fastjob.ui.viewmodels.search.JobSearchViewModel
import com.fastjob.ui.viewmodels.search.SearchViewModel.SearchState

/**
 * Componente de la lista de trabajos
 * @param itemsRefreshOffset Cantidad de items restantes para refrescar la lista
 * @param jobSearchViewModel ViewModel de la pantalla de búsqueda
 * @param navController Controlador de navegación
 */
@Composable
fun SearchJobList(
    itemsRefreshOffset: Int = 1,
    jobSearchViewModel: JobSearchViewModel,
    navController: NavController
) {
    // estado de la busqueda
    val searchState by jobSearchViewModel.searchState.collectAsState()

    // estado del scroll
    val scrollState by jobSearchViewModel.jobListScroll.collectAsState()

    // lista de trabajos
    val jobList by jobSearchViewModel.jobList.collectAsState()

    // estado de si se llego al final del scroll
    val isItemReachEndScroll by remember {
        derivedStateOf {
            scrollState.layoutInfo.visibleItemsInfo.lastOrNull()?.index == scrollState.layoutInfo.totalItemsCount - if(scrollState.layoutInfo.totalItemsCount<itemsRefreshOffset) 1 else itemsRefreshOffset
        }
    }

    // efecto que se encarga de actualizar la lista de trabajos
    JobSearchListEffect(
        searchState = searchState,
        jobSearchViewModel = jobSearchViewModel,
        isItemReachEndScroll = isItemReachEndScroll,
        scrollState = scrollState
    )

    // animacion de la lista de trabajos
    AnimatedVisibility(
        visible = searchState != SearchState.SEARCH,
        enter = when(searchState){
            SearchState.DONE -> slideIn(
                initialOffset = { IntOffset(0, it.height) },
                animationSpec = tween(600)
            )
            else -> fadeIn()
        },
        exit = when(searchState){
            SearchState.DONE -> slideOut(
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
                JobItem(
                    index = index,
                    job = item,
                    navController = navController
                )
            }

            // item de carga y error
            when (searchState) {
                // item de carga
                SearchState.LOADING -> {
                    item {
                        LoadingItem("")
                    }
                }
                // item de error de no se encontraron trabajos
                SearchState.NOT_FOUND -> {
                    item {
                        ErrorItem(
                            text = stringResource(id = R.string.job_not_found)
                        )
                    }
                }
                // item de error de busqueda inesperado
                SearchState.ERROR -> {
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

@Preview(showBackground = true)
@Composable
fun JobListPreview() {
    FastjobTheme {
        SearchJobList(
            jobSearchViewModel = JobSearchViewModel(),
            navController = rememberNavController()
        )
    }
}

@Preview(showBackground = true, uiMode = Configuration.UI_MODE_NIGHT_YES)
@Composable
fun JobListPreviewDark() {
    FastjobTheme {
        SearchJobList(
            jobSearchViewModel = JobSearchViewModel(),
            navController = rememberNavController()
        )
    }
}