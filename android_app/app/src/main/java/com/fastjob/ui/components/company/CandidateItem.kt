package com.fastjob.ui.components.company

import androidx.compose.foundation.Image
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import com.fastjob.R
import com.fastjob.models.MinimalCandidateIN
import com.fastjob.ui.functions.capitalize
import com.fastjob.ui.functions.capitalizeWords
import com.fastjob.ui.navigation.AppScreens
import java.util.UUID

/**
 * Componente que muestra un candidato
 * @param index Indice de la oferta de trabajo
 * @param jobId Identificador de la oferta de trabajo
 * @param candidate Candidato
 * @param navController Controlador de navegacion
 */
@Composable
fun CandidateItem(
    index: Int = 0,
    jobId: UUID,
    candidate: MinimalCandidateIN,
    navController: NavController
) {
    // numero de lineas que se mostraran en la descripcion
    val descriptionMaxLines = 4
    // imagenes de los candidatos
    val firstImage = painterResource(id = R.drawable.job_first)
    val secondImage = painterResource(id = R.drawable.job_second)

    // lista de nombres de las disponibilidades
    val availabilitiesDisplayNames = candidate.availabilities?.map { stringResource(id = it.displayName) }

    // funcion que se ejecuta cuando se hace click
    val clickable = {
        navController.navigate(AppScreens.CandidateCardScreen.route + "/$index/${jobId}/${candidate.id}")
    }

    // columna que contiene el candidato
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 10.dp)
            .clickable(onClick = clickable),
        verticalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        // imagen del candidato
        Image(
            painter = (index % 2 == 0).let { if(it) firstImage else secondImage },
            contentDescription = stringResource(id = R.string.job_image_desc),
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 10.dp)
        )
        // nombre del candidato
        Text(
            text = "${candidate.name.capitalizeWords()} ${candidate.surname.capitalizeWords()}",
            fontSize = 18.sp,
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 10.dp)
        )
        // habilidades del candidato
        Text(
            text = "${stringResource(id = R.string.candidates_skills)}: ${candidate.skills?.joinToString(", ") { it.capitalize() } ?: stringResource(id = R.string.candidates_skills_empty)}",
            fontSize = 14.sp,
            maxLines = descriptionMaxLines,
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 10.dp),
            textAlign = TextAlign.Justify
        )
        // habilidades del candidato
        Text(
            text = "${stringResource(id = R.string.candidates_availabilities)}: ${availabilitiesDisplayNames?.joinToString(", ") ?: stringResource(id = R.string.candidates_availabilities_empty)}",
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
                text = candidate.province.capitalize(),
                fontSize = 9.sp
            )
        }
    }
}




