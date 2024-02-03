@file:Suppress("DEPRECATION")

package com.fastjob.ui.components.basic

import android.content.res.Configuration
import android.location.Address
import android.location.Geocoder
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.fastjob.R
import com.fastjob.ui.enums.LoadState
import com.fastjob.ui.theme.FastjobTheme
import com.google.android.gms.maps.model.CameraPosition
import com.google.android.gms.maps.model.LatLng
import com.google.maps.android.compose.GoogleMap
import com.google.maps.android.compose.Marker
import com.google.maps.android.compose.MarkerState
import com.google.maps.android.compose.rememberCameraPositionState
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.IOException

/**
 * Mapa de Google Maps
 * Busca la direccion con el [Geocoder] y muestra el [GoogleMap] con un [Marker] en la posición
 * @param direction Dirección a buscar
 */
@Composable
fun Map(
    direction: String
){
    // Geocoder para buscar la dirección
    val geocoder = Geocoder(LocalContext.current)
    // Estado de carga del mapa
    val (loadState, setMapLoadState) = remember { mutableStateOf(LoadState.LOADING) }
    // Posición de la cámara
    val cameraPositionState = rememberCameraPositionState { position = CameraPosition.fromLatLngZoom(LatLng(0.0, 0.0), 10f) }

    // effect para buscar la dirección
    LaunchedEffect(Unit){
        withContext(Dispatchers.IO) {
            try {
                // Busca la dirección con el geocoder
                val addresses: List<Address> = geocoder.getFromLocationName(direction, 1)?.toList() ?: emptyList()
                when {
                    // Si no encuentra la dirección cambia el estado a NOT_FOUND
                    addresses.isEmpty() -> setMapLoadState(LoadState.NOT_FOUND)
                    else -> {
                        // Si encuentra la dirección cambia el estado a LOADED y actualiza la posición de la cámara
                        cameraPositionState.position = CameraPosition
                            .fromLatLngZoom(LatLng(addresses[0].latitude, addresses[0].longitude), 10f)
                        setMapLoadState(LoadState.LOADED)
                    }
                }
            // Si hay un error cambia el estado a ERROR
            } catch (_: IOException) {
                setMapLoadState(LoadState.ERROR)
            }
        }
    }

    // Muestra el mapa según el estado de carga
    Box(
        contentAlignment = Alignment.Center,
        modifier = Modifier
            .fillMaxWidth()
            .height(230.dp),
    ) {
        when (loadState) {
            // Muestra el loading
            LoadState.LOADING -> {
                LoadingItem("")
            }
            // Muestra el error
            LoadState.ERROR -> {
                ErrorItem(stringResource(id = R.string.map_error))
            }
            // Muestra que no se ha encontrado la dirección
            LoadState.NOT_FOUND -> {
                ErrorItem(stringResource(id = R.string.map_location_not_found).replace("{DIR}", direction))
            }
            // Muestra el mapa
            LoadState.LOADED -> {
                GoogleMap(
                    modifier = Modifier.fillMaxWidth(),
                    cameraPositionState = cameraPositionState
                ) {
                    Marker(
                        state = MarkerState(position = cameraPositionState.position.target),
                        title = direction
                    )
                }
            }
            // else para acabar el when
            else -> {}
        }
    }
}


@Preview(showBackground = true)
@Composable
fun MapPreview() {
    FastjobTheme {
        Map("madrid")
    }
}

@Preview(showBackground = true, uiMode = Configuration.UI_MODE_NIGHT_YES)
@Composable
fun MapPreviewDark() {
    FastjobTheme {
        Map("madrid")
    }
}
