package com.fastjob.ui.components.basic

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import com.fastjob.R
import com.fastjob.models.Availability
import com.fastjob.models.interfaces.Selectable

/**
 * Componente que muestra un campo seleccionable
 * @param modifier Modificador del componente
 * @param label Etiqueta del campo
 * @param itemPossibilities Posibilidades de seleccion
 * @param selected Seleccion actual
 * @param getStringResource Funcion que muestra el valor seleccionado
 * @param setSelected Funcion que cambia el valor seleccionado
 */
@Composable
fun <T: Selectable> Selectable(
    modifier: Modifier = Modifier,
    label: String,
    itemPossibilities: List<T>,
    selected: String,
    getStringResource: (T?) -> Int?,
    setSelected: (T?) -> Unit,
    stringToClass: (String) -> T?
){
    // estado del menu
    var menuVisibility by remember { mutableStateOf(false) }

    // columna con los items
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .then(modifier),
        verticalArrangement = Arrangement.spacedBy(4.dp)
    ){
        // items
        TextField(
            enabled = false,
            singleLine = true,
            modifier = Modifier
                .fillMaxWidth()

                .padding(horizontal = 10.dp)
                .clip(RoundedCornerShape(20.dp))
                .clickable {
                    menuVisibility = true
                },
            label = { Text(label) },
            value = stringResource(id = getStringResource(stringToClass(selected)) ?: R.string.selectable_default),
            onValueChange = {},
            trailingIcon = {
                // boton de eliminar
                if(selected != "") {
                    IconButton(
                        onClick = {
                            setSelected(null)
                        },
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
        // menu de opciones
        DropdownMenu(
            expanded = menuVisibility,
            onDismissRequest = { menuVisibility = false }
        ) {
            // columnas con las opciones
            Column {
                // recorre las posibilidades y crea un DropdownMenuItem por cada una
                itemPossibilities.forEach { possibility ->
                    if(possibility.value != selected) {
                        DropdownMenuItem(
                            text = { Text(text = stringResource(id = possibility.displayName)) },
                            onClick = {
                                setSelected(possibility)
                                menuVisibility = false
                            }
                        )
                    }
                }
            }
        }
    }
}