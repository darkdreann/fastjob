package com.fastjob.ui.effects

import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import com.fastjob.auth.AuthAPI
import com.fastjob.models.JobIN
import com.fastjob.network.Client
import com.fastjob.services.JobService
import com.fastjob.ui.enums.LoadState
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.util.UUID

/**
 * Efecto para obtener un trabajo por su UUID
 * @param jobUUID UUID del trabajo
 * @param setJob Función para establecer el trabajo
 * @param setLoadState Función para establecer el estado de carga
 */
@Composable
fun LoadJobEffect(
    jobUUID: UUID,
    setJob: (JobIN) -> Unit,
    setLoadState: (LoadState) -> Unit
) {
    // obtenemos el servicio de trabajos y la instancia de autenticación
    val jobService = Client.getInstance().getService(JobService::class.java)
    val auth = AuthAPI.getInstance()

    // efecto para obtener el trabajo
    LaunchedEffect(Unit){
        withContext(Dispatchers.IO) {
            // obtenemos la respuesta del servidor
            val response = jobService.getJob(
                auth = auth.getToken(),
                id = jobUUID
            )
            when {
                // si la respuesta es exitosa, establecemos el trabajo y el estado de carga como cargado
                response.isSuccessful -> {
                    response.body()?.let {
                        setJob(it)
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
