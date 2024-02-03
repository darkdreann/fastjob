package com.fastjob.ui.components.basic

import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
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

/**
 * Componente que representa un campo de contraseña
 * @param maxLength longitud máxima de la contraseña
 * @param errorState estado del error
 * @param passwordState estado de la contraseña
 */
@Composable
fun PasswordField(
    maxLength: Int,
    errorState: Pair<Boolean, (Boolean) -> Unit> = Pair(false) {},
    passwordState: Pair<String, (String) -> Unit>
){
    // estado de la contraseña
    val (password, setPassword) = passwordState

    // estado del error
    val (isError, setError) = errorState

    // estado de la visibilidad de la contraseña
    var passwordVisibility by remember { mutableStateOf(false) }

    // campo de contraseña
    TextField(
        label = { Text(stringResource(id = R.string.user_password)) },
        singleLine = true,
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(15.dp)),
        value = password,
        onValueChange = {
            if(it.length <= maxLength)
                setPassword(it)
            setError(false)
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
}