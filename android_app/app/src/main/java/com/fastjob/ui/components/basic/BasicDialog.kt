package com.fastjob.ui.components.basic

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.painter.Painter
import androidx.compose.ui.res.stringResource
import com.fastjob.R
import com.fastjob.ui.theme.error

/**
 * Dialogo basico para mostrar un mensaj
 * @param title titulo del dialogo
 * @param content contenido del dialogo
 * @param icon icono del dialogo
 * @param visibilityState visibilidad del dialogo
 */
@Composable
fun BasicDialog(
    title: String,
    content: String,
    icon: Painter,
    visibilityState: Pair<Boolean, (Boolean) -> Unit>
) {

    // visibilidad del dialogo
    val (visibility, setVisibility) = visibilityState

    // animacion de entrada y salida
    AnimatedVisibility(
        visible = visibility,
        enter = fadeIn(),
        exit = fadeOut()
    ) {
        // dialogo
        AlertDialog(
            onDismissRequest = {
                setVisibility(false)
            },
            title = {
                Text(title)
            },
            text = {
                Text(content)
            },
            confirmButton = {
                TextButton(
                    onClick = {
                        setVisibility(false)
                    }
                ) {
                    Text(stringResource(id = R.string.aceptar_dialog))
                }
            },
            icon = {
                Icon(
                    painter = icon,
                    contentDescription = stringResource(id = R.string.dialog_icon_desc),
                    tint = error
                )
            }
        )
    }



}