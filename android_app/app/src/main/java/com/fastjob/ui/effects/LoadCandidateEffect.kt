package com.fastjob.ui.effects

import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import com.fastjob.auth.AuthAPI
import com.fastjob.models.CandidateIN
import com.fastjob.network.Client
import com.fastjob.services.JobCandidateService
import com.fastjob.ui.enums.LoadState
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.util.UUID

/**
 * Efecto para cargar un candidato
 * @param jobId UUID del trabajo
 * @param candidateId UUID del candidato
 * @param setCandidate función para establecer el candidato
 * @param setLoadState función para establecer el estado de carga
 */
@Composable
fun LoadCandidateEffect(
    jobId: UUID,
    candidateId: UUID,
    setCandidate: (CandidateIN) -> Unit,
    setLoadState: (LoadState) -> Unit
) {
    // obtenemos el servicio de jobCandidate y la instancia de autenticación
    val jobCandidateService = Client.getInstance().getService(JobCandidateService::class.java)
    val auth = AuthAPI.getInstance()

    if(!auth.isAuthenticated()) return

    // efecto para obtener el candidato
    LaunchedEffect(Unit){
        withContext(Dispatchers.IO) {
            // obtenemos la respuesta del servidor
            val response = jobCandidateService.getJobCandidate(
                auth = auth.getToken()!!,
                jobId = jobId,
                candidateId = candidateId
            )
            when {
                // si la respuesta es exitosa, establecemos el candidato y el estado de carga como cargado
                response.isSuccessful -> {
                    response.body()?.let {
                        setCandidate(it)
                        setLoadState(LoadState.LOADED)
                    } ?: setLoadState(LoadState.ERROR)
                }
                // si la respuesta es 404, establecemos el estado de carga como no encontrado
                response.code() == 404 -> setLoadState(LoadState.NOT_FOUND)
                // cualquier otro código de respuesta, establecemos el estado de carga como error
                else -> setLoadState(LoadState.ERROR)
            }
        }
    }
}
