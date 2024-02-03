package com.fastjob.ui.components.candidate

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
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
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.fastjob.R
import com.fastjob.models.CandidateEducationIN
import com.fastjob.ui.functions.capitalize
import com.fastjob.ui.functions.localFormat
import java.util.UUID

/**
 * Muestra una tarjeta con la informacion de una formacion
 * @param candidateEducation formacion a mostrar
 * @param edit funcion para editar la formacion
 * @param delete funcion para eliminar la formacion
 */
@Composable
fun EducationCard(
    candidateEducation: CandidateEducationIN,
    edit: ((UUID) -> Unit)? = null,
    delete: ((UUID) -> Unit)? = null
) {
    // visibilidad del dropdown
    var dropdownVisibility by remember { mutableStateOf(false) }

    // contexto local
    val context = LocalContext.current

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(8.dp)
            .clickable {
                if (edit != null || delete != null) {
                    dropdownVisibility = true
                }
            },
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        // titulo formacion
        Text(
            text = candidateEducation.education.qualification.capitalize(),
            fontSize = 20.sp
        )
        // nivel de formacion
        Text(
            text = candidateEducation.education.level.name.capitalize(),
        )
        // sector de la formacion
        candidateEducation.education.sector?.let {
            Text(
                text = "${it.values.first().category.capitalize()} ${it.values.first().subcategory.capitalize()}",

            )
        }
        // nombre de la empresa
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .padding(8.dp),
            contentAlignment = Alignment.CenterEnd
        ){
            Text(
                text = candidateEducation.completionDate.localFormat(context),
            )
        }
        if(edit != null || delete != null){
            DropdownMenu(
                expanded = dropdownVisibility,
                onDismissRequest = { dropdownVisibility = false }
            ) {
                // opciones de editar
                edit?.let {
                    DropdownMenuItem(
                        onClick = {
                            dropdownVisibility = false
                            edit(candidateEducation.education.id)
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
                            delete(candidateEducation.education.id)
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