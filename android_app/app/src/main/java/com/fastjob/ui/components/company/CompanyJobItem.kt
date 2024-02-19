package com.fastjob.ui.components.company

import androidx.compose.foundation.Image
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
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import com.fastjob.R
import com.fastjob.models.MinimalJobIN
import com.fastjob.ui.functions.capitalize
import com.fastjob.ui.functions.capitalizeParagraph
import com.fastjob.ui.navigation.AppScreens
import java.util.Locale
import java.util.UUID

/**
 * Componente que muestra una oferta de trabajo para hacer una lista de ofertas de trabajo.\
 * @param index Indice de la oferta de trabajo
 * @param job Oferta de trabajo a mostrar
 * @param navController Controlador de navegacion
 */
@Composable
fun CompanyJobItem(
    index: Int = 0,
    job: MinimalJobIN,
    navController: NavController,
    deleteJob: (UUID) -> Unit
) {
    // numero de lineas que se mostraran en la descripcion
    val descriptionMaxLines = 4
    // imagenes de las ofertas de trabajo
    val firstImage = painterResource(id = R.drawable.job_first)
    val secondImage = painterResource(id = R.drawable.job_second)

    // estado visibilidad del dropdown
    var dropdownVisibility by remember { mutableStateOf(false) }


    // columna que contiene la oferta de trabajo
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 10.dp)
            .clickable{
                dropdownVisibility = true
            },
        verticalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        // imagen de la oferta de trabajo
        Image(
            painter = (index % 2 == 0).let { if(it) firstImage else secondImage },
            contentDescription = stringResource(id = R.string.job_image_desc),
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 10.dp)
        )
        // titulo de la oferta de trabajo
        Text(
            text = job.title.uppercase(Locale.getDefault()),
            fontSize = 18.sp,
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 10.dp)
        )
        // descripcion de la oferta de trabajo
        Text(
            text = job.description.capitalizeParagraph(),
            fontSize = 14.sp,
            maxLines = descriptionMaxLines,
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 10.dp),
            textAlign = TextAlign.Justify
        )
        // provincia de la oferta de trabajo
        Box(
            contentAlignment = Alignment.BottomEnd,
            modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 10.dp)
        ){
            Text(
                text = job.province.capitalize(),
                fontSize = 9.sp
            )
        }

        DropdownMenu(
            expanded = dropdownVisibility,
            onDismissRequest = { dropdownVisibility = false }
        ) {
            // editar oferta de trabajo
            DropdownMenuItem(
                onClick = {
                    dropdownVisibility = false
                    navController.navigate(AppScreens.CompanyUpdateJobScreen.route + "/${job.id}")
                },
                text = {
                    Text(
                        text = stringResource(id = R.string.job_edit),
                    )
                }
            )
            // editar formacion
            DropdownMenuItem(
                onClick = {
                    dropdownVisibility = false
                    navController.navigate(AppScreens.CompanyUpdateJobEducationScreen.route + "/${job.id}")
                },
                text = {
                    Text(
                        text = stringResource(id = R.string.job_education_edit),
                    )
                }
            )
            // editar idiomas
            DropdownMenuItem(
                onClick = {
                    dropdownVisibility = false
                    navController.navigate(AppScreens.CompanyUpdateJobLanguageListScreen.route + "/${job.id}")
                },
                text = {
                    Text(
                        text = stringResource(id = R.string.job_language_edit),
                    )
                }
            )
            // ver candidatos aplicados
            DropdownMenuItem(
                onClick = {
                    dropdownVisibility = false
                    navController.navigate(AppScreens.CompanyJobCandidateListScreen.route + "/${job.id}")
                },
                text = {
                    Text(
                        text = stringResource(id = R.string.job_candidates_list),
                    )
                }
            )
            // eliminar oferta
            DropdownMenuItem(
                onClick = {
                    dropdownVisibility = false
                    deleteJob(job.id)
                },
                text = {
                    Text(
                        text = stringResource(id = R.string.job_delete),
                    )
                }
            )
        }
    }
}

