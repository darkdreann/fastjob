package com.fastjob.ui.effects

import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import com.fastjob.ui.enums.LoadState
import com.fastjob.ui.viewmodels.candidate.ExperienceListViewModel

/**
 * Efecto para cargar las experiencias
 * @param viewModel ViewModel de la lista de experiencias
 * @param isItemReachEndScroll Booleano que indica si se llego al final del scroll
 * @param loadState Estado de la carga
 */
@Composable
fun LoadExperiencesEffect(
    viewModel: ExperienceListViewModel,
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