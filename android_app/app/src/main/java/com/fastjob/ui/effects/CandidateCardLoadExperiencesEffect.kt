package com.fastjob.ui.effects

import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import com.fastjob.ui.enums.LoadState
import com.fastjob.ui.viewmodels.company.CandidateCardExperienceListViewModel

/**
 * Efecto para cargar las experiencias
 * @param viewModel ViewModel de la lista de experiencias
 * @param isItemReachEndScroll Booleano que indica si se llego al final del scroll
 * @param loadState Estado de la carga
 */
@Composable
fun CandidateCardLoadExperiencesEffect(
    viewModel: CandidateCardExperienceListViewModel,
    isItemReachEndScroll: Boolean,
    loadState: LoadState
){
    // efecto que se encarga de actualizar la lista de experiencias
    LaunchedEffect(isItemReachEndScroll){
        if(loadState == LoadState.LOADED)
            viewModel.loadMoreExperiences()
    }
    // efecto que se encarga de cargar las experiencias por primera vez
    LaunchedEffect(Unit){
        viewModel.getExperiences()
    }
}