package com.fastjob.ui.effects

import androidx.compose.foundation.lazy.LazyListState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import com.fastjob.ui.viewmodels.search.JobSearchViewModel
import com.fastjob.ui.viewmodels.search.SearchViewModel.SearchState

/**
 * Efecto que se encarga de buscar ofertas de trabajo por primera vez y cuando se llega al final del scroll
 * @param searchState estado de la busqueda
 * @param jobSearchViewModel viewmodel de la busqueda
 * @param isItemReachEndScroll estado de si se llego al final del scroll
 * @param scrollState estado del scroll
 */
@Composable
fun JobSearchListEffect(
    searchState: SearchState,
    jobSearchViewModel: JobSearchViewModel,
    isItemReachEndScroll: Boolean,
    scrollState: LazyListState
){
    // efecto que se encarga de actualizar la lista de trabajos
    LaunchedEffect(isItemReachEndScroll){
        if(searchState == SearchState.DONE)
            jobSearchViewModel.loadMoreJobs()
    }
    // efecto que se encarga de buscar ofertas de trabajo por primera vez
    LaunchedEffect(searchState){
        if(searchState == SearchState.SEARCH){
            scrollState.scrollToItem(0)
            jobSearchViewModel.getJobs()
        }
    }
}