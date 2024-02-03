package com.fastjob.ui.components.basic

import android.content.res.Configuration
import android.util.Log
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.TextRange
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.fastjob.ui.theme.FastjobTheme
import java.lang.Error

/**
 * Componente que contiene un TextField con un label y un DropdownAutocomplete
 * @param enabled si el TextField está habilitado
 * @param label texto del label
 * @param setValue función que se ejecuta cuando se selecciona un valor del DropdownAutocomplete
 * @param textState estado del TextField
 * @param autoCompleteFunction función que se ejecuta cuando se escribe en el TextField para obtener los valores del DropdownAutocomplete
 * @param imeAction acción del teclado
 * @param keyBoardAction acciones del teclado
 */
@Composable
fun TextFieldPicker(
    modifier: Modifier = Modifier,
    padding: Dp = 10.dp,
    enabled: Boolean = true,
    readOnly: Boolean = false,
    label: String? = null,
    setValue: (String) -> Unit,
    textState: Pair<String, (String) -> Unit>,
    autoCompleteFunction: (suspend (keyword: String) -> List<String>?),
    imeAction: ImeAction = ImeAction.Done,
    keyBoardAction: KeyboardActions = KeyboardActions(),
    isError: Boolean = false
)
{
    // estado del texto
    val (text, setText) = textState

    // estado del TextField
    val textFieldValue = remember {
        mutableStateOf(
            TextFieldValue(
                text = text,
                selection = TextRange(text.length)
            )
        )
    }

    // columna con el TextField y el DropdownAutocomplete
    Column {
        // TextField
        TextField(
            value = textFieldValue.value,
            onValueChange = {
                textFieldValue.value = it
                setText(it.text)
                setValue(it.text)
            },
            enabled = enabled,
            readOnly = readOnly,
            singleLine = true,
            modifier = Modifier
                .height(52.dp)
                .clip(RoundedCornerShape(20.dp))
                .fillMaxWidth()
                .padding(horizontal = padding)
                .then(modifier),
            label = {
                label?.let {
                    Text(text = it)
                }
            },
            textStyle = TextStyle(fontSize = 13.sp),
            keyboardOptions = KeyboardOptions(
                imeAction = imeAction
            ),
            keyboardActions = keyBoardAction,
            isError = isError
        )
        // dropdown autocomplete si se especifica la función de autocompletado
        DropdownAutocomplete(
            keywordState = Pair(text) { word ->
                textFieldValue.value = textFieldValue.value.copy(
                    text = word,
                    selection = TextRange(word.length)
                )
                setText(word)
                setValue(word)
            },
            autocompleteFunction = autoCompleteFunction,
            modifier = Modifier
                .padding(start = 10.dp)
        )
    }
}

@Preview
@Composable
fun TextFieldPickerPreview() {
    FastjobTheme {
        TextFieldPicker(
            label = "Test",
            setValue = {},
            autoCompleteFunction = { null },
            textState = Pair("") {}
        )
    }
}

@Preview(uiMode = Configuration.UI_MODE_NIGHT_YES)
@Composable
fun TextFieldPickerPreviewDark() {
    FastjobTheme {
        TextFieldPicker(
            label = "Test",
            setValue = {},
            autoCompleteFunction = { null },
            textState = Pair("") {}
        )
    }
}