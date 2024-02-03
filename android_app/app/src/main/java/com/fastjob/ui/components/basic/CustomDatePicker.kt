package com.fastjob.ui.components.basic

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.ExperimentalAnimationApi
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.DatePicker
import androidx.compose.material3.DatePickerDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme.colorScheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Text
import androidx.compose.material3.rememberDatePickerState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.DialogProperties
import com.fastjob.ui.functions.localFormat
import com.fastjob.ui.functions.toLocalDate
import com.fastjob.ui.theme.FastjobTheme
import java.time.LocalDate
import java.util.Calendar
import java.util.Date

/**
 * Muestra un dialogo con un date picker para seleccionar una fecha
 * @param label etiqueta del campo de texto
 * @param setDate funcion para establecer la fecha seleccionada
 * @param validator validador de la fecha seleccionada
 * @param errorMsg mensaje de error si la fecha seleccionada no es valida
 */
@OptIn(ExperimentalMaterial3Api::class, ExperimentalAnimationApi::class)
@Composable
fun CustomDatePicker(
    label: String,
    initialDate: LocalDate? = null,
    setDate: (LocalDate) -> Unit,
    validator: ((LocalDate) -> Boolean)? = null,
    errorMsg: String? = null
){
    // contexto local
    val context = LocalContext.current

    // fecha inicial
    val calendar = Calendar.getInstance().apply {
        val today = initialDate ?: LocalDate.now()
        this.set(today.year, today.monthValue-1, today.dayOfMonth)
    }

    // estado del date picker con la fecha inicial
    val datePickerState = rememberDatePickerState(initialSelectedDateMillis = calendar.timeInMillis)

    // fecha seleccionada
    val selectedDate = datePickerState.selectedDateMillis?.let { millis ->
        Date(millis).toLocalDate()
    }

    // estado de visibilidad del date picker
    var dateVisible by remember { mutableStateOf(false) }

    // animacion de entrada y salida del date picker
    AnimatedVisibility(
        visible = dateVisible,
        enter = fadeIn(),
        exit = fadeOut()
    ){
        // dialogo del date picker
        AlertDialog(
            onDismissRequest = { dateVisible = false },
            properties = DialogProperties(
                usePlatformDefaultWidth = false,
            ),
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 5.dp)
                .animateEnterExit(
                    enter = fadeIn(),
                    exit = fadeOut()
                )
        ) {
            // date picker
            DatePicker(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(colorScheme.background),
                state = datePickerState,
                showModeToggle = false,
                colors = DatePickerDefaults.colors(
                    selectedDayContentColor = colorScheme.tertiary,
                )
            )
        }
    }

    Column {
        // campo de texto
        OutlinedTextField(
            singleLine = true,
            readOnly = true,
            enabled = false,
            modifier = Modifier
                .fillMaxWidth()
                .clickable {
                    dateVisible = true
                },
            value = selectedDate?.localFormat(context) ?: "",
            onValueChange = {},
            label = { Text(label) },
            colors = OutlinedTextFieldDefaults.colors(
                disabledTextColor = colorScheme.onSurface,
                disabledContainerColor = Color.Transparent,
                disabledBorderColor = colorScheme.outline,
                disabledLeadingIconColor = colorScheme.onSurfaceVariant,
                disabledTrailingIconColor = colorScheme.onSurface,
                disabledLabelColor = colorScheme.onSurfaceVariant,
                disabledPlaceholderColor = colorScheme.onSurfaceVariant,
                disabledSupportingTextColor = colorScheme.onSurfaceVariant,
                disabledPrefixColor = colorScheme.onSurfaceVariant,
                disabledSuffixColor = colorScheme.onSurfaceVariant
            ),
            isError = selectedDate?.let { validator?.invoke(it) } ?: false,
        )
        // mensaje de error si existe
        errorMsg?.let {
            selectedDate?.let { localDate ->
                validator?.let { validator ->
                    if (validator(localDate)) {
                        Text(
                            text = errorMsg,
                            color = colorScheme.error,
                            modifier = Modifier
                                .fillMaxWidth()
                        )
                    }
                }
            }
        }
    }



    // effecto para ocultar el date picker cuando se selecciona una fecha
    LaunchedEffect(selectedDate){
        dateVisible = false
        selectedDate?.let {
            setDate(it)
        }
    }
}


@Preview(showBackground = true)
@Composable
fun DataPickerPreview(){
    FastjobTheme {
        CustomDatePicker(
            "Fecha",
            setDate = {},
            validator = { it.isAfter(LocalDate.now()) },
            errorMsg = "La fecha no puede ser mayor a la actual"
        )
    }
}