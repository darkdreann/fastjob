package com.fastjob.ui.effects

import android.util.Log
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import com.fastjob.ui.enums.LoadState
import com.fastjob.ui.viewmodels.company.CompanyJobListViewModel

/**
 * Efecto que se encarga de cargar ofertas de trabajo por primera vez y cuando se llega al final del scroll
 * @param loadState estado de la carga
 * @param companyJobViewModel viewmodel de la lista de trabajos del candidato
 * @param isItemReachEndScroll estado de si se llego al final del scroll
 */
@Composable
fun JobCompanyListEffect(
    loadState: LoadState,
    companyJobViewModel: CompanyJobListViewModel,
    isItemReachEndScroll: Boolean
){
    // efecto que se encarga de actualizar la lista de trabajos
    LaunchedEffect(isItemReachEndScroll){
        if(loadState == LoadState.LOADED)
            companyJobViewModel.loadMoreJobs()
    }

    // efecto que se encarga de cargar la lista de trabajos
    LaunchedEffect(Unit){
        if(loadState == LoadState.START){
            companyJobViewModel.getJobs()
        }
    }
}