package com.fastjob.ui.components.company

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.fastjob.R
import com.fastjob.ui.components.basic.ErrorItem
import com.fastjob.ui.components.basic.LoadingItem
import com.fastjob.ui.effects.LoadCandidateEffect
import com.fastjob.ui.enums.LoadState
import com.fastjob.ui.viewmodels.company.CandidateCardViewModel
import java.util.UUID

/**
 * Composable que muestra la información de un candidato.
 * @param index Índice del candidato
 * @param jobId UUID de la oferta
 * @param candidateId UUID del candidato
 * @param viewModel ViewModel del candidato
 */
@Composable
fun CandidateLoader(
    index: Int,
    jobId: UUID,
    candidateId: UUID,
    viewModel: CandidateCardViewModel,
    navController: NavController
) {
    // estado de carga
    val loadState by viewModel.loadState.collectAsState()
    // candidato
    val candidate by viewModel.candidate.collectAsState()

    // efecto de carga del candidato
    LoadCandidateEffect(
        jobId = jobId,
        candidateId = candidateId,
        setCandidate = viewModel::setCandidate,
        setLoadState = viewModel::setLoadState
    )

    // oferta
    Box(
        contentAlignment = Alignment.Center,
        modifier = Modifier
            .fillMaxSize(),
    ) {
        when (loadState) {
            // si el estado de carga es LOADING se muestra el componente de carga
            LoadState.LOADING -> {
                LoadingItem(stringResource(id = R.string.candidate_loading))
            }
            // si el estado de carga es ERROR se muestra el componente de error
            LoadState.ERROR -> {
                ErrorItem(stringResource(id = R.string.candidate_loading_error))
            }
            // si el estado de carga es NOT_FOUND se muestra el componente de error de candidato no encontrada
            LoadState.NOT_FOUND -> {
                ErrorItem(stringResource(id = R.string.candidate_loading_not_found))
            }
            // si el estado de carga es LOADED se muestra el componente de candidato
            LoadState.LOADED -> {
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.spacedBy(15.dp),
                    modifier = Modifier
                        .fillMaxSize()
                        .verticalScroll(rememberScrollState())
                ) {
                    // componente de candidato
                    CandidateCard(
                        index = index,
                        candidate = candidate ?: return,
                        navController = navController,
                        jobId = jobId
                    )
                }
            }
            // else para acabar el when
            else -> {}
        }
    }
}