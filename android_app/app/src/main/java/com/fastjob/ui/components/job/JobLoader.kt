package com.fastjob.ui.components.job

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import com.fastjob.R
import com.fastjob.models.JobIN
import com.fastjob.ui.components.basic.ErrorItem
import com.fastjob.ui.components.basic.LoadingItem
import com.fastjob.ui.effects.LoadJobEffect
import com.fastjob.ui.enums.LoadState
import java.util.UUID

/**
 * Componente de carga de una oferta
 * @param index Índice de la oferta
 * @param jobUUID UUID de la oferta
 */
@Composable
fun JobLoader(
    index: Int,
    jobUUID: UUID?
) {
    // estado de carga de la oferta
    val (loadState, setLoadState) = remember { mutableStateOf(LoadState.LOADING) }
    // oferta
    val (job, setJob) = remember { mutableStateOf<JobIN?>(null) }

    // si el UUID de la oferta no es nulo se activa el efecto de carga, si es nulo se cambia el estado de carga a error
    jobUUID?.let {
        // efecto de carga de la oferta
        LoadJobEffect(
            jobUUID = it,
            setJob = setJob,
            setLoadState = setLoadState
        )
    } ?: setLoadState(LoadState.ERROR)

    // oferta
    Box(
        contentAlignment = Alignment.Center,
        modifier = Modifier
            .fillMaxSize(),
    ) {
        when (loadState) {
            // si el estado de carga es LOADING se muestra el componente de carga
            LoadState.LOADING -> {
                LoadingItem(stringResource(id = R.string.job_loading))
            }
            // si el estado de carga es ERROR se muestra el componente de error
            LoadState.ERROR -> {
                ErrorItem(stringResource(id = R.string.job_loading_error))
            }
            // si el estado de carga es NOT_FOUND se muestra el componente de error de oferta no encontrada
            LoadState.NOT_FOUND -> {
                ErrorItem(stringResource(id = R.string.job_loading_not_found))
            }
            // si el estado de carga es LOADED se muestra el componente de oferta
            LoadState.LOADED -> {
                JobCard(
                    index = index,
                    job = job ?: return@Box
                )
            }
        }
    }
}