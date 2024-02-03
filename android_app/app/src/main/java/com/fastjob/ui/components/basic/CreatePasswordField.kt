package com.fastjob.ui.components.basic

import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme.colorScheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import com.fastjob.R
import com.fastjob.ui.functions.isPasswordSecure

/**
 * Componente que representa un campo para crear una contraseña
 * @param maxLength longitud máxima de la contraseña
 * @param errorState estado del error
 * @param setPassword función para establecer la contraseña
 */
@Composable
fun CreatePasswordField(
    maxLength: Int,
    errorState: Pair<Boolean, (Boolean) -> Unit> = Pair(false) {},
    setPassword: (String) -> Unit
){
    // estado del error
    val (isError, setError) = errorState

    // estado de la visibilidad de la contraseña
    var passwordVisibility by remember { mutableStateOf(false) }

    // estado passwords
    var passwordText by remember { mutableStateOf("") }
    var passwordConfirmText by remember { mutableStateOf("") }


    LaunchedEffect(passwordText, passwordConfirmText){
        if(passwordText.isPasswordSecure() && passwordText == passwordConfirmText){
            setPassword(passwordText)
        }
    }

    // campo de contraseña
    TextField(
        label = { Text(stringResource(id = R.string.user_password)) },
        singleLine = true,
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(15.dp)),
        value = passwordText,
        onValueChange = {
            if(it.length <= maxLength)
                passwordText = it
            setError(!it.isPasswordSecure())
        },
        visualTransformation = if (passwordVisibility) VisualTransformation.None else PasswordVisualTransformation(),
        trailingIcon = {
            // botón para mostrar/ocultar la contraseña
            TextButton(onClick = { passwordVisibility = !passwordVisibility }) {
                Text(
                    if (passwordVisibility) stringResource(id = R.string.password_hide)
                    else stringResource(id = R.string.password_show)
                )
            }
        },
        isError = isError
    )

    // campo de contraseña
    TextField(
        label = { Text(stringResource(id = R.string.password_confirmar)) },
        singleLine = true,
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(15.dp)),
        value = passwordConfirmText,
        onValueChange = {
            if(it.length <= maxLength)
                passwordConfirmText = it
            setError(!it.isPasswordSecure())
        },
        visualTransformation = if (passwordVisibility) VisualTransformation.None else PasswordVisualTransformation(),
        trailingIcon = {
            // botón para mostrar/ocultar la contraseña
            TextButton(onClick = { passwordVisibility = !passwordVisibility }) {
                Text(
                    if (passwordVisibility) stringResource(id = R.string.password_hide)
                    else stringResource(id = R.string.password_show)
                )
            }
        },
        isError = isError,
    )
    if(isError){
        Text(
            text = if(!passwordText.isPasswordSecure()) stringResource(id = R.string.register_user_password_error)
                    else stringResource(id = R.string.register_user_password_confirm_error),
            color = colorScheme.error,
        )
    }
}