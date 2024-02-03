package com.fastjob.ui.components.basic

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.expandIn
import androidx.compose.animation.shrinkOut
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme.colorScheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.runtime.toMutableStateList
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import com.fastjob.R
import com.fastjob.models.Availability

/**
 * Componente que permite seleccionar una lista de Availability
 * @param modifier modificador del componente
 * @param label etiqueta del TextField
 * @param buttonAddText texto del botón de agregar
 * @param itemPossibilities posibilidades de Availability
 * @param itemList lista de Availability
 * @param setList función que se ejecuta al cambiar la lista
 * @param maxListItems cantidad máxima de items
 * @param maxHeight altura máxima del componente
 */
@Composable
fun SelectableAvailability(
    modifier: Modifier = Modifier,
    label: String,
    buttonAddText: String,
    itemPossibilities: List<Availability>,
    itemList: List<Availability>,
    setList: (List<Availability>) -> Unit,
    maxListItems: Int = 10,
    maxHeight: Int = 200
){
    // estado Lista
    val items = remember { if(itemList.isNotEmpty()) itemList.map { it.value }.toMutableStateList() else listOf("").toMutableStateList() }

    // estado del menu
    var menuVisibility by remember { mutableStateOf(false) }

    // estado del scroll
    val scrollState = rememberLazyListState()

    // indice del item seleccionado
    var currentIndex by remember { mutableIntStateOf(0) }

    // animacion de scroll al agregar un item
    LaunchedEffect(items.size) {
        scrollState.animateScrollToItem(items.lastIndex)
    }

    // columna con los items
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
            // campo de texto con el item
            TextField(
                enabled = false,
                singleLine = true,
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(15.dp))
                    .clickable {
                        menuVisibility = true
                        currentIndex = index
                    },
                label = { Text(label) },
                value = stringResource(id = Availability.getDisplayNameByValue(item)),
                onValueChange = {},
                trailingIcon = {
                    // boton de eliminar si hay mas de un item
                    if (items.size > 1) {
                        // botón de eliminar
                        IconButton(
                            onClick = {
                                items.removeAt(index)
                                setList(items.map { Availability.getByValue(it) })
                            },
                            modifier = Modifier
                        ) {
                            // icono de eliminar
                            Icon(
                                painter = painterResource(id = R.drawable.delete),
                                contentDescription = stringResource(id = R.string.delete_icon),
                                tint = Color.Black,
                            )
                        }
                    }
                },
            )
        }
        item {
            // animacion de visibilidad del boton de agregar
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
                    // boton de agregar
                    Button(
                        modifier = Modifier.fillMaxWidth(),
                        onClick = {
                            items.add("")
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

    // menu de opciones
    DropdownMenu(
        expanded = menuVisibility,
        onDismissRequest = { menuVisibility = false }
    ) {
        // columnas con las opciones
        Column {
            // recorre las posibilidades y crea un DropdownMenuItem por cada una
            itemPossibilities.forEach { possibility ->
                if(possibility.value !in items) {
                    DropdownMenuItem(
                        text = { Text(text = stringResource(id = possibility.displayName)) },
                        onClick = {
                            //if(possibility !in items) {
                            items[currentIndex] = possibility.value
                            setList(items.map { Availability.getByValue(it) })
                            menuVisibility = false
                            //}
                        }
                    )
                }
            }
        }
    }
}