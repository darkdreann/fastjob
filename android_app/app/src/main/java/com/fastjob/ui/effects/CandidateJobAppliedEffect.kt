package com.fastjob.ui.effects

import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import com.fastjob.auth.AuthAPI
import com.fastjob.network.Client
import com.fastjob.services.JobCandidateService
import com.fastjob.ui.enums.LoadState
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.util.UUID

/**
 * Efecto de carga de la candidatura del usuario con una oferta\
 * @param jobId UUID de la oferta
 * @param setApplied función para establecer el estado de candidatura
 * @param setLoadState función para establecer el estado de carga
 */
@Composable
fun CandidateJobAppliedEffect(
    jobId: UUID,
    setApplied: (Boolean) -> Unit,
    setLoadState: (LoadState) -> Unit
) {
    // instancia de autenticación
    val auth = AuthAPI.getInstance()
    // servicio de candidateJob
    val candidateJobService = Client.getInstance().getService(JobCandidateService::class.java)

    // si el usuario no está autenticado se establece el estado de carga a error
    if(!auth.isAuthenticated()) {
        setLoadState(LoadState.ERROR)
    }else{
        // se lanza el efecto de carga de la candidatura del usuario con la oferta
        LaunchedEffect(Unit){
            withContext(Dispatchers.IO){
                // se obtiene la respuesta de la petición
                val response = candidateJobService.isAppliedJob(
                    auth = auth.getToken()!!,
                    jobId = jobId,
                    candidateId = auth.getUserId()!!
                )

                // si la respuesta es exitosa se establece el estado de candidatura con la oferta, si no se establece el estado de carga a error
                if(response.isSuccessful){
                    response.body()?.let {
                        setApplied(it)
                        setLoadState(LoadState.LOADED)

                        // si no hay body se establece el estado de carga a error
                    } ?: setLoadState(LoadState.ERROR)

                }else{
                    // si la respuesta no es exitosa se establece el estado de carga a error
                    setLoadState(LoadState.ERROR)
                }
            }
        }
    }
}