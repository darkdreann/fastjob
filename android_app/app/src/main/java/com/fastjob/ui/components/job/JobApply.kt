package com.fastjob.ui.components.job

import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme.colorScheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import com.fastjob.R
import com.fastjob.ui.components.basic.ErrorItem
import com.fastjob.ui.enums.LoadState
import com.fastjob.ui.viewmodels.job.JobCardViewModel

/**
 * Componente con el botón de candidatura a una oferta
 * @param index Índice de la oferta
 * @param jobUUID UUID de la oferta
 * @param viewModel ViewModel de la oferta
 */
@Composable
fun JobApply(
    viewModel: JobCardViewModel
) {
    // se ha cargado la oferta
    val isJobLoaded by viewModel.loadState.collectAsState()

    // se ha cargado el estado del usuario con la oferta
    val jobAppliedLoading by viewModel.isAppliedLoading.collectAsState()

    // se ha aplicado a la oferta
    val isApplied by viewModel.isApplied.collectAsState()

    when{
        // si se ha cargado la oferta y el estado de candidatura del usuario con la oferta se muestra el botón de candidatura
        isJobLoaded == LoadState.LOADED && jobAppliedLoading == LoadState.LOADED -> {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(end = 15.dp),
                contentAlignment = Alignment.CenterEnd
            )
            {
                TextButton(
                    modifier = Modifier
                        .padding(bottom = 16.dp)
                        .border(1.dp, colorScheme.primary),
                    onClick = {
                        viewModel.applyJob()
                    }
                ) {
                    Text(
                        if (isApplied) stringResource(id = R.string.job_candidate_remove) else stringResource(
                            id = R.string.job_candidate_apply
                        )
                    )
                }
            }
        }
        // si se ha cargado la oferta pero el estado de candidatura es error se muestra un mensaje de error
        isJobLoaded == LoadState.LOADED && jobAppliedLoading == LoadState.ERROR -> {
            ErrorItem(stringResource(id = R.string.job_candidate_applied_error))
        }
    }
}