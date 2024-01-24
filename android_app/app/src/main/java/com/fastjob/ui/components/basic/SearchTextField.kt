package com.fastjob.ui.components.basic

import android.content.res.Configuration
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.ExperimentalComposeUiApi
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.painter.Painter
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.TextRange
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.fastjob.R
import com.fastjob.ui.theme.FastjobTheme
import com.fastjob.ui.viewmodels.search.JobSearchViewModel
import com.fastjob.ui.viewmodels.search.SearchViewModel

/**
 * Componente de campo de texto para busquedas puede tener autocompletado.
 * @param viewModel viewmodel que contiene el estado del campo de texto.
 * @param placeholder texto que se muestra cuando el campo está vacío tiene un valor por defecto.
 * @param textFieldIcon icono que se muestra en el campo de texto por defecto no tiene.
 * @param textFieldIconDescription descripción del icono que se muestra en el campo de texto tiene un valor por defecto.
 * @param autoCompleteFunction función que se ejecuta para obtener las sugerencias de autocompletado. Si no se especifica no tiene autocompletado.
 */
@OptIn(ExperimentalComposeUiApi::class)
@Composable
fun SearchTextField(
    viewModel: SearchViewModel,
    placeholder: String = stringResource(R.string.search_textfield_default_placeholder),
    textFieldIcon: Painter? = null,
    textFieldIconDescription: String = stringResource(R.string.search_textfield_default_icon_description),
    autoCompleteFunction: (suspend (keyword: String) -> List<String>?)? = null)
{
    // controlador del teclado
    val controller = LocalSoftwareKeyboardController.current

    // estado de la palabra a buscar
    val keyword by viewModel.keyword.collectAsState()

    // estado del campo de texto
    val textFieldValue = remember {
        mutableStateOf(
            TextFieldValue(
                text = keyword,
                selection = TextRange(keyword.length)
            )
        )
    }

    // column para los componentes
    Column {
        // campo de texto
        TextField(
            value = textFieldValue.value,
            onValueChange = {
                viewModel.setKeyword(it.text)
                textFieldValue.value = it
            },
            placeholder = {
                Text(placeholder)
            },
            leadingIcon = {
                // si se especifica el icono se muestra
                textFieldIcon?.let {
                    Icon(
                        painter = it,
                        contentDescription = textFieldIconDescription
                    )
                }
            },
            keyboardOptions = KeyboardOptions(
                imeAction = ImeAction.Search
            ),
            keyboardActions = KeyboardActions(
                onSearch = {
                    controller?.hide()
                    viewModel.setSearchState(SearchViewModel.SearchState.SEARCH)
                }
            ),
            singleLine = true,
            modifier = Modifier
                .height(55.dp)
                .clip(RoundedCornerShape(15.dp))
                .fillMaxWidth()
        )
        // dropdown autocomplete si se especifica la función de autocompletado
        autoCompleteFunction?.let {
            DropdownAutocomplete(
                appendWord = true,
                keywordState = Pair(keyword) { word ->
                    viewModel.setKeyword(word)
                    textFieldValue.value = textFieldValue.value.copy(
                        text = word,
                        selection = TextRange(word.length)
                    )
                },
                autocompleteFunction = autoCompleteFunction
            )
        }
    }


}


@Preview
@Composable
fun JobTextFieldPreview() {
    FastjobTheme {
        SearchTextField(JobSearchViewModel())
    }
}

@Preview(uiMode = Configuration.UI_MODE_NIGHT_YES)
@Composable
fun JobTextFieldPreviewDark() {
    FastjobTheme {
        SearchTextField(JobSearchViewModel())
    }
}