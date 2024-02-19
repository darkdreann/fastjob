package com.fastjob.ui.effects

import androidx.compose.foundation.lazy.LazyListState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import com.fastjob.ui.viewmodels.search.CandidateSearchViewModel
import com.fastjob.ui.viewmodels.search.SearchViewModel.SearchState

/**
 * Efecto que se encarga de buscar ofertas de trabajo por primera vez y cuando se llega al final del scroll
 * @param searchStatePair estado de la busqueda
 * @param candidateSearchViewModel viewmodel de la busqueda
 * @param isItemReachEndScroll estado de si se llego al final del scroll
 * @param scrollState estado del scroll
 */
@Composable
fun CandidateSearchListEffect(
    searchStatePair: Pair<SearchState, (SearchState) -> Unit>,
    candidateSearchViewModel: CandidateSearchViewModel,
    isItemReachEndScroll: Boolean,
    scrollState: LazyListState
){
    val (searchState, setSearchState) = searchStatePair

    // efecto que se encarga de actualizar la lista de candidatos
    LaunchedEffect(isItemReachEndScroll){
        if(searchState == SearchState.DONE)
            candidateSearchViewModel.loadMoreCandidates()
    }
    // efecto que se encarga de buscar candidatos por primera vez
    LaunchedEffect(searchState){
        if(searchState == SearchState.SEARCH){
            scrollState.scrollToItem(0)
            candidateSearchViewModel.getCandidates()
        }
    }

    LaunchedEffect(Unit) {
        setSearchState(SearchState.SEARCH)
    }
}