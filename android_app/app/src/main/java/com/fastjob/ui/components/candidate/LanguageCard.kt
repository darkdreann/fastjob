package com.fastjob.ui.components.candidate

import androidx.compose.foundation.Image
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.fastjob.R
import com.fastjob.models.LanguageWithLevelIN
import com.fastjob.ui.functions.capitalize
import java.util.UUID

/**
 * Muestra una tarjeta con la informacion de un idioma
 * @param candidateLanguage idioma a mostrar
 * @param edit funcion para editar el idioma
 * @param delete funcion para eliminar el idioma
 */
@Composable
fun LanguageCard(
    candidateLanguage: LanguageWithLevelIN,
    edit: ((UUID) -> Unit)? = null,
    delete: ((UUID) -> Unit)? = null
) {
    // visibilidad del dropdown
    var dropdownVisibility by remember { mutableStateOf(false) }

    Row(
        modifier = Modifier
            .clickable {
                if (edit != null || delete != null) {
                    dropdownVisibility = true
                }
            }
    ){
        Image(
            modifier = Modifier.weight(0.2f),
            painter = painterResource(id = R.drawable.language),
            contentDescription = stringResource(id = R.string.candidate_language_image_desc),
        )
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(8.dp)
                .weight(0.8f),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            // nombre del idioma
            Text(
                text = candidateLanguage.language.name.capitalize(),
                fontSize = 20.sp
            )
            // nivel del idioma
            Text(
                text = candidateLanguage.level.name.capitalize()
            )
            if (edit != null || delete != null) {
                DropdownMenu(
                    expanded = dropdownVisibility,
                    onDismissRequest = { dropdownVisibility = false }
                ) {
                    // opciones de editar
                    edit?.let {
                        DropdownMenuItem(
                            onClick = {
                                dropdownVisibility = false
                                edit(candidateLanguage.language.id)
                            },
                            text = {
                                Text(
                                    text = stringResource(id = R.string.candidate_language_edit),
                                )
                            }
                        )
                    }
                    // opciones de eliminar
                    delete?.let {
                        DropdownMenuItem(
                            onClick = {
                                dropdownVisibility = false
                                delete(candidateLanguage.language.id)
                            },
                            text = {
                                Text(
                                    text = stringResource(id = R.string.candidate_language_delete),
                                )
                            }
                        )
                    }
                }
            }
        }
    }


}