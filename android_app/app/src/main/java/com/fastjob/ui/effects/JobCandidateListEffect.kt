package com.fastjob.ui.effects

import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import com.fastjob.ui.enums.LoadState
import com.fastjob.ui.viewmodels.job.CandidateJobListViewModel

/**
 * Efecto que se encarga de cargar ofertas de trabajo por primera vez y cuando se llega al final del scroll
 * @param loadState estado de la carga
 * @param candidateJobViewModel viewmodel de la lista de trabajos del candidato
 * @param isItemReachEndScroll estado de si se llego al final del scroll
 */
@Composable
fun JobCandidateListEffect(
    loadState: LoadState,
    candidateJobViewModel: CandidateJobListViewModel,
    isItemReachEndScroll: Boolean
){
    // efecto que se encarga de actualizar la lista de trabajos
    LaunchedEffect(isItemReachEndScroll){
        if(loadState == LoadState.LOADED)
            candidateJobViewModel.loadMoreJobs()
    }

    // efecto que se encarga de cargar la lista de trabajos
    LaunchedEffect(Unit){
        if(loadState == LoadState.START){
            candidateJobViewModel.getJobs()
        }
    }
}