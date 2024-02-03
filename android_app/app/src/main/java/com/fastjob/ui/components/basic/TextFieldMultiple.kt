package com.fastjob.ui.components.basic

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.expandIn
import androidx.compose.animation.shrinkOut
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.MaterialTheme.colorScheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.runtime.toMutableStateList
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import com.fastjob.R
import kotlinx.coroutines.runBlocking

/**
 * Componente para crear un TextField con múltiples items
 * @param modifier modificador del componente
 * @param label texto del label
 * @param setError función para establecer el estado de error
 * @param checkError función para validar el error
 * @param errorMsg texto del error
 * @param buttonAddText texto del botón de agregar
 * @param itemList lista de items
 * @param setList función para establecer la lista de items
 * @param keyboardOptions opciones del teclado
 * @param itemsCheck función para validar los items
 * @param maxListItems cantidad máxima de items
 * @param maxHeight altura máxima del componente
 */
@Composable
fun TextFieldMultiple(
    modifier: Modifier = Modifier,
    label: String,
    setError: ((Boolean) -> Unit)? = null,
    checkError: ((String) -> Boolean)? = null,
    errorMsg: String = "",
    buttonAddText: String,
    itemList: List<String>,
    setList: (List<String>) -> Unit,
    keyboardOptions: KeyboardOptions = KeyboardOptions(),
    itemsCheck: ((String) -> Boolean)? = null,
    maxListItems: Int = 10,
    maxHeight: Int = 200
){

    // estado Lista
    val items = remember { if(itemList.isNotEmpty()) itemList.toMutableStateList() else listOf("").toMutableStateList() }

    // estado de lista errores
    val errors = remember { items.map { false }.toMutableStateList() }

    // estado del scroll
    val scrollState = rememberLazyListState()

    // animacion de scroll al agregar un item
    LaunchedEffect(items.size) {
        scrollState.animateScrollToItem(items.lastIndex)
    }

    // lazy column con los items
    LazyColumn(
        state = scrollState,
        modifier = Modifier
            .fillMaxWidth()
            .heightIn(max = maxHeight.dp)
            .then(modifier),
        verticalArrangement = Arrangement.spacedBy(4.dp)
    ){
        // items
        itemsIndexed(items) { index, item ->
            // text field para cada item
            TextField(
                singleLine = true,
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(15.dp)),
                label = { Text(label) },
                value = item,
                onValueChange = { newValue ->
                    // si hay una función para validar los items, se ejecuta
                    itemsCheck?.let {
                        if (it(newValue)) {
                            items[index] = newValue
                            setList(items)
                        }
                    }
                    ?: run {
                        items[index] = newValue
                        setList(items)
                    }
                    setError?.let {
                        checkError?.let { check ->
                            errors[index] = check(newValue)
                            it(errors[index])
                        }
                    }
                },
                trailingIcon = {
                    // si hay más de un item, se muestra el botón de eliminar
                    if (items.size > 1) {
                        // botón de eliminar
                        IconButton(
                            onClick = {
                                items.removeAt(index)
                                setList(items)
                            },
                            modifier = Modifier
                        ) {
                            // icono de  eliminar
                            Icon(
                                painter = painterResource(id = R.drawable.delete),
                                contentDescription = stringResource(id = R.string.delete_icon),
                                tint = Color.Black,
                            )
                        }
                    }
                },
                keyboardOptions = keyboardOptions,
                isError = errors[index],
            )
            if(errors[index]){
                Text(
                    text = errorMsg,
                    color = MaterialTheme.colorScheme.error,
                )
            }
        }
        item {
            // animación de visibilidad del botón de agregar
            AnimatedVisibility(
                visible = items.size <= maxListItems,
                enter = expandIn(),
                exit = shrinkOut()
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth(),
                    contentAlignment = Alignment.CenterEnd
                ) {
                    // botón de agregar
                    Button(
                        modifier = Modifier.fillMaxWidth(),
                        onClick = {
                            items.add("")
                            errors.add(false)
                        },
                        colors = ButtonDefaults.buttonColors(
                            containerColor = colorScheme.primary,
                            contentColor = colorScheme.tertiary
                        ),
                    ) {
                        Text(text = buttonAddText)
                        Icon(
                            painter = painterResource(id = R.drawable.add),
                            contentDescription = stringResource(id = R.string.add_icon)
                        )
                    }
                }
            }
        }
    }
}