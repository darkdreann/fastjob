package com.fastjob.ui.components.candidate

import androidx.compose.foundation.Image
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
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
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.fastjob.R
import com.fastjob.models.ExperienceIN
import com.fastjob.ui.functions.capitalize
import com.fastjob.ui.functions.capitalizeParagraph
import com.fastjob.ui.functions.localFormat
import java.util.Locale
import java.util.UUID

/**
 * Muestra una tarjeta con la informacion de una experiencia laboral
 * @param experience experiencia laboral
 * @param edit funcion para editar la experiencia
 * @param delete funcion para eliminar la experiencia
 */
@Composable
fun ExperienceCard(
    experience: ExperienceIN,
    edit: ((UUID) -> Unit)? = null,
    delete: ((UUID) -> Unit)? = null
) {
    // visibilidad del dropdown
    var dropdownVisibility by remember { mutableStateOf(false) }

    // contexto local
    val context = LocalContext.current

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
            painter = painterResource(id = R.drawable.experience),
            contentDescription = stringResource(id = R.string.candidate_experience_image_desc)
        )
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(8.dp)
                .weight(0.8f),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            // titulo posicion laboral
            Text(
                text = experience.jobPosition.uppercase(Locale.getDefault()),
                fontSize = 20.sp
            )
            // descripcion
            Text(
                text = experience.jobPositionDescription.capitalizeParagraph(),
            )
            // sector
            Text(
                text = "${experience.sector.category.capitalize()} ${experience.sector.subcategory.capitalize()}",

                )
            // fechas de inicio y fin
            Text(
                text = "${experience.startDate.localFormat(context)} - ${
                    experience.endDate?.localFormat(
                        context
                    ) ?: stringResource(id = R.string.candidate_experience_end_date_default)
                }",
            )
            // nombre de la empresa
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(8.dp),
                contentAlignment = Alignment.CenterEnd
            ) {
                Text(
                    text = experience.companyName.capitalize(),
                )
            }
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
                                edit(experience.id)
                            },
                            text = {
                                Text(
                                    text = stringResource(id = R.string.candidate_experience_edit),
                                )
                            }
                        )
                    }
                    // opciones de eliminar
                    delete?.let {
                        DropdownMenuItem(
                            onClick = {
                                dropdownVisibility = false
                                delete(experience.id)
                            },
                            text = {
                                Text(
                                    text = stringResource(id = R.string.candidate_experience_delete),
                                )
                            }
                        )
                    }
                }
            }
        }
    }


}