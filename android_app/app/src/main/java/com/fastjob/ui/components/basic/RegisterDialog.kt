package com.fastjob.ui.components.basic

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.navigation.NavController
import com.fastjob.R
import com.fastjob.ui.navigation.AppScreens

/**
 * Dialogo de registro de usuario permitiendo elegir entre candidato o empresa
 * @param navController controlador de navegación
 * @param visibilityState estado de visibilidad del dialogo
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RegisterDialog(
    navController: NavController,
    visibilityState: Pair<Boolean, (Boolean) -> Unit>
){
    // estado de visibilidad del dialogo
    val (visibility, setVisibility) = visibilityState

    // animación de entrada y salida
    AnimatedVisibility(
        visible = visibility,
        enter = fadeIn(),
        exit = fadeOut()
    ) {
        // dialogo de registro
        AlertDialog(
            onDismissRequest = {
                setVisibility(false)
            },
            title = {
                Text(stringResource(id = R.string.register_dialog_title))
            },
            text = {
                Text(stringResource(id = R.string.register_dialog_text))
            },
            confirmButton = {
                // botones de registro
                Row(
                    modifier = Modifier.fillMaxWidth()
                ){
                    // botón de registro de candidato
                    TextButton(
                        modifier = Modifier.weight(1f),
                        onClick = {
                            setVisibility(false)
                            navController.navigate(AppScreens.UserCandidateRegisterScreen.route)
                        }
                    ) {
                        Text(stringResource(id = R.string.register_dialog_button_candidate))
                    }
                    // botón de registro de empresa
                    TextButton(
                        modifier = Modifier.weight(1f),
                        onClick = {
                            setVisibility(false)
                            navController.navigate(AppScreens.UserCompanyRegisterScreen.route)
                        }
                    ) {
                        Text(stringResource(id = R.string.register_dialog_button_company))
                    }
                }
            },
            icon = {
                Icon(
                    painter = painterResource(id = R.drawable.register),
                    contentDescription = stringResource(id = R.string.register_dialog_icon_desc)
                )
            }
        )
    }
}