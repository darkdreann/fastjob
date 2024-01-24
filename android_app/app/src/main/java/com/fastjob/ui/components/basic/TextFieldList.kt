package com.fastjob.ui.components.basic

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.TextRange
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.fastjob.R
import com.fastjob.ui.theme.success
import com.fastjob.ui.theme.error

/**
 * Componente que permite ingresar una lista de textos
 * @param enabled habilita o deshabilita el componente
 * @param label etiqueta del componente
 * @param textState estado del texto
 * @param autoCompleteFunction función de autocompletado para mostrar sugerencias
 * @param imeAction acción del teclado
 * @param keyBoardAction acciones del teclado
 */
@Composable
fun TextFieldList(
    enabled: Boolean = true,
    label: String? = null,
    textState: Pair<List<String>, (List<String>) -> Unit>,
    autoCompleteFunction: (suspend (keyword: String) -> List<String>?),
    imeAction: ImeAction = ImeAction.Done,
    keyBoardAction: KeyboardActions = KeyboardActions()
)
{
    // límite de elementos en la lista
    val limitElementsList = 5
    // estado de la lista de textos
    val (textList, setTextList) = textState
    // estado del texto
    val textFieldValue = remember { mutableStateOf(TextFieldValue()) }

    // columna que contiene los componentes
    Column(
        verticalArrangement = Arrangement.spacedBy(1.dp)
    ) {
        // textfield para ingresar el texto
        TextField(
            value = textFieldValue.value,
            onValueChange = {
                textFieldValue.value = it
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
            trailingIcon = {
                    // botón para agregar el texto a la lista
                    Button(
                        onClick = {
                            if(textFieldValue.value.text.isNotEmpty()){
                                setTextList(textList + textFieldValue.value.text)
                                textFieldValue.value = TextFieldValue()
                            }
                        },
                        colors = ButtonDefaults.buttonColors(
                            containerColor = Color.Transparent
                        ),
                        shape = CircleShape,
                        modifier = Modifier
                            .height(40.dp)
                            .width(40.dp),
                        contentPadding = PaddingValues(5.dp),
                        enabled = textList.size < limitElementsList,
                        border = BorderStroke(3.dp, success)
                    )
                    {
                        // icono de agregar
                        Icon(
                            painter = painterResource(id = R.drawable.add),
                            contentDescription = stringResource(id = R.string.add_icon),
                            tint = success,
                            modifier = Modifier.size(25.dp)
                        )
                    }
            },
            keyboardOptions = KeyboardOptions(
                imeAction = imeAction
            ),
            keyboardActions = keyBoardAction
        )

        // dropdown autocomplete
        DropdownAutocomplete(
            keywordState = Pair(textFieldValue.value.text) {
                textFieldValue.value = textFieldValue.value.copy(
                    text = it,
                    selection = TextRange(it.length)
                )
            },
            autocompleteFunction = autoCompleteFunction,
            modifier = Modifier
                .padding(start = 10.dp)
        )
        // animación para mostrar la lista de textos
        AnimatedVisibility(textList.isNotEmpty()) {
            // textfield para mostrar la lista de textos
            TextField(
                readOnly = true,
                value = textList.joinToString(", "),
                onValueChange = {
                    setTextList(it.split(", "))
                },
                singleLine = true,
                modifier = Modifier
                    .height(44.dp)
                    .clip(RoundedCornerShape(20.dp))
                    .fillMaxWidth()
                    .padding(horizontal = 10.dp),
                textStyle = TextStyle(fontSize = 9.sp),
                trailingIcon = {
                    // botón para limpiar la lista de textos
                    Button(
                        onClick = {
                            setTextList(emptyList())
                        },
                        colors = ButtonDefaults.buttonColors(
                            containerColor = Color.Transparent
                        ),
                        shape = CircleShape,
                        contentPadding = PaddingValues(5.dp),
                        modifier = Modifier
                            .height(40.dp)
                            .width(40.dp),
                        border = BorderStroke(3.dp, error)
                    )
                    {
                        // icono de limpiar
                        Icon(
                            painter = painterResource(id = R.drawable.clean),
                            contentDescription = stringResource(id = R.string.clear_icon),
                            tint = error,
                            modifier = Modifier.size(20.dp)
                        )
                    }
                }
            )
        }
    }
}