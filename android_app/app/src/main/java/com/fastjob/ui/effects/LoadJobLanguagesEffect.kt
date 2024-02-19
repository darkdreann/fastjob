package com.fastjob.ui.effects

import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import com.fastjob.ui.enums.LoadState
import com.fastjob.ui.viewmodels.company.JobLanguageListViewModel

/**
 * Efecto para cargar los idiomas
 * @param viewModel ViewModel de la lista de idiomas
 * @param isItemReachEndScroll Booleano que indica si se llego al final del scroll
 * @param loadState Estado de la carga
 */
@Composable
fun LoadJobLanguagesEffect(
    viewModel: JobLanguageListViewModel,
    isItemReachEndScroll: Boolean,
    loadState: LoadState
){
    // efecto que se encarga de actualizar la lista de idiomas
    LaunchedEffect(isItemReachEndScroll){
        if(loadState == LoadState.LOADED)
            viewModel.loadMoreLanguages()
    }
    // efecto que se encarga de cargar los idiomas al iniciar la pantalla
    LaunchedEffect(Unit){
        viewModel.getLanguages()
    }
}