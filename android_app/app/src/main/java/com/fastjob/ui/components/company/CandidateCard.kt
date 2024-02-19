package com.fastjob.ui.components.company

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Divider
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import com.fastjob.R
import com.fastjob.models.CandidateIN
import com.fastjob.ui.components.basic.Map
import com.fastjob.ui.functions.capitalize
import com.fastjob.ui.functions.capitalizeParagraph
import com.fastjob.ui.functions.generateExperienceText
import com.fastjob.ui.functions.localFormat
import com.fastjob.ui.navigation.AppScreens
import java.util.Locale
import java.util.UUID

/**
 * Composable que muestra la informacion de un candidato
 * @param modifier modificador del composable]
 * @param index indice del candidato
 * @param candidate candidato a mostrar
 */
@Composable
fun CandidateCard(
    modifier: Modifier = Modifier,
    index: Int = 0,
    jobId: UUID,
    candidate: CandidateIN,
    navController: NavController
) {
    // imagenes para los jobs
    val firstImage = painterResource(id = R.drawable.job_first)
    val secondImage = painterResource(id = R.drawable.job_second)

    // lista de nombres de las disponibilidades
    val availabilitiesDisplayNames = candidate.availabilities?.map { stringResource(id = it.displayName) }


    // columna de contenido
    Column(
        verticalArrangement = Arrangement.spacedBy(10.dp),
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 8.dp)
            .then(modifier)
    ) {
        // imagen de job
        Image(
            painter = (index % 2 == 0).let { if(it) firstImage else secondImage },
            contentDescription = stringResource(id = R.string.candidate_image_description),
            modifier = Modifier
                .fillMaxWidth()
                .padding(top = 10.dp),
        )
        // nombre de candidato
        Text(
            text = "${candidate.user.name.capitalize()} ${candidate.user.surname.capitalize()}",
            fontSize = 20.sp,
            modifier = Modifier
                .fillMaxWidth(),
            textAlign = TextAlign.Center,
            maxLines = 1
        )
        // email de candidato
        Text(
            text = candidate.user.email,
            textAlign = TextAlign.Justify,
        )
        // telefonos de candidato
        Text(
            text = candidate.user.phoneNumbers.joinToString(", "),
            textAlign = TextAlign.Justify,
        )
        // separador
        Divider(
            modifier = Modifier
                .fillMaxWidth()
                .padding(vertical = 15.dp),
            thickness = 1.dp,
        )
        // habilidades
        Text(
            text = "${stringResource(id = R.string.candidates_skills)}: ${candidate.skills?.joinToString(", ") { it.capitalize() }?.ifEmpty{ null } ?: stringResource(id = R.string.candidates_skills_empty)}",
            modifier = Modifier.fillMaxWidth(),
        )
        // jornada de trabajo
        Text(
            text = "${stringResource(id = R.string.candidates_availabilities)}: ${availabilitiesDisplayNames?.joinToString(", ")?.ifEmpty{ null } ?: stringResource(id = R.string.candidates_availabilities_empty)}",
            modifier = Modifier.fillMaxWidth(),
        )
        // separador
        Divider(
            modifier = Modifier
                .fillMaxWidth()
                .padding(vertical = 15.dp),
            thickness = 1.dp,
        )
        TextButton(
            modifier = Modifier.fillMaxWidth(),
            onClick = { navController.navigate(AppScreens.CandidateCardEducationScreen.route + "/${jobId}/${candidate.user.id}")  }
        ) {
            Text(
                modifier = Modifier.fillMaxWidth(),
                textAlign = TextAlign.Center,
                text = stringResource(id = R.string.candidate_education_show_more)
            )
        }
        TextButton(
            modifier = Modifier.fillMaxWidth(),
            onClick = { navController.navigate(AppScreens.CandidateCardExperiencesScreen.route + "/${jobId}/${candidate.user.id}")  }
        ) {
            Text(
                modifier = Modifier.fillMaxWidth(),
                textAlign = TextAlign.Center,
                text = stringResource(id = R.string.candidate_experience_show_more)
            )
        }
        TextButton(
            modifier = Modifier.fillMaxWidth(),
            onClick = { navController.navigate(AppScreens.CandidateCardLanguageScreen.route + "/${jobId}/${candidate.user.id}")  }
        ) {
            Text(
                modifier = Modifier.fillMaxWidth(),
                textAlign = TextAlign.Center,
                text = stringResource(id = R.string.candidate_language_show_more)
            )
        }
        // separador
        Divider(
            modifier = Modifier
                .fillMaxWidth()
                .padding(vertical = 15.dp),
            thickness = 1.dp,
        )
        // mapa con la direccion
        Map(
            direction = "${candidate.user.address.postalCode} ${candidate.user.address.city} ${candidate.user.address.province}"
        )
    }
}