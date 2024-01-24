package com.fastjob.ui.components.basic

import android.content.res.Configuration
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
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.TextRange
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.fastjob.ui.theme.FastjobTheme

/**
 * Componente TextFieldAutocomplete para mostrar un campo de texto con un dropdown autocomplete
 * debajo del mismo.
 * @param enabled: Booleano para habilitar o deshabilitar el campo de texto.
 * @param label: String para mostrar un label en el campo de texto.
 * @param textState: Pair<String, (String) -> Unit> para manejar el estado del texto del campo de
 * @param autoCompleteFunction: (suspend (keyword: String) -> List<String>?) función de autocompletado para buscar las opciones.
 * @param imeAction: ImeAction acción del teclado.
 * @param keyBoardAction: KeyboardActions acciones del teclado.
 */
@Composable
fun TextFieldAutocomplete(
    enabled: Boolean = true,
    label: String? = null,
    textState: Pair<String, (String) -> Unit>,
    autoCompleteFunction: (suspend (keyword: String) -> List<String>?),
    imeAction: ImeAction = ImeAction.Done,
    keyBoardAction: KeyboardActions = KeyboardActions()
)
{
    // estado del texto
    val (text, setText) = textState

    // estado del campo de texto
    val textFieldValue = remember {
        mutableStateOf(
            TextFieldValue(
                text = text,
                selection = TextRange(text.length)
            )
        )
    }

    // Column para que el dropdown autocomplete se muestre debajo del textfield
    Column {
        // campo de texto
        TextField(
            value = textFieldValue.value,
            onValueChange = {
                textFieldValue.value = it
                setText(it.text)
            },
            singleLine = true,
            modifier = Modifier
                .height(52.dp)
                .clip(RoundedCornerShape(20.dp))
                .fillMaxWidth()
                .padding(horizontal = 10.dp),
            enabled = enabled,
            label = {
                label?.let {
                    Text(text = it)
                }
            },
            textStyle = TextStyle(fontSize = 13.sp),
            keyboardOptions = KeyboardOptions(
                imeAction = imeAction
            ),
            keyboardActions = keyBoardAction
        )

        // dropdown autocomplete para mostrar las opciones
        DropdownAutocomplete(
            keywordState = Pair(text) { word ->
                textFieldValue.value = textFieldValue.value.copy(
                    text = word,
                    selection = TextRange(word.length)
                )
                setText(word)
            },
            autocompleteFunction = autoCompleteFunction,
            modifier = Modifier
                .padding(start = 10.dp)
        )
    }

}

@Preview
@Composable
fun TextFieldAutocompletePreview() {
    FastjobTheme {
        TextFieldAutocomplete(
            label = "Test",
            textState = Pair("") {},
            autoCompleteFunction = { null }
        )
    }
}

@Preview(uiMode = Configuration.UI_MODE_NIGHT_YES)
@Composable
fun TextFieldAutocompletePreviewDark() {
    FastjobTheme {
        TextFieldAutocomplete(
            label = "Test",
            textState = Pair("") {},
            autoCompleteFunction = { null }
        )
    }
}