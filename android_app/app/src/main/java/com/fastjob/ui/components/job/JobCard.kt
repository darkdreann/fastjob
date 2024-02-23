package com.fastjob.ui.components.job

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Divider
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.fastjob.R
import com.fastjob.models.JobIN
import com.fastjob.ui.components.basic.Map
import com.fastjob.ui.functions.capitalize
import com.fastjob.ui.functions.capitalizeParagraph
import com.fastjob.ui.functions.generateExperienceText
import com.fastjob.ui.functions.localFormat
import java.util.Locale

/**
 * Componente de una oferta de trabajo
 * @param modifier modificador del componente
 * @param index índice de la oferta
 * @param job oferta
 */
@Composable
fun JobCard(
    modifier: Modifier = Modifier,
    index: Int = 0,
    job: JobIN
) {
    // imagenes para los jobs
    val firstImage = painterResource(id = R.drawable.job_first)
    val secondImage = painterResource(id = R.drawable.job_second)

    // contexto local
    val localContext = LocalContext.current

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
            contentDescription = stringResource(id = R.string.job_image_desc),
            modifier = Modifier
                .fillMaxWidth()
                .padding(top = 10.dp),
            alpha = if(job.active) 1f else 0.5f,
        )
        // titulo de job
        Text(
            text = job.title.uppercase(Locale.getDefault()),
            fontSize = 20.sp,
            modifier = Modifier
                .fillMaxWidth(),
            textAlign = TextAlign.Center,
            maxLines = 1
        )
        // descripcion de job
        Text(
            text = job.description.capitalizeParagraph(),
            textAlign = TextAlign.Justify,
        )
        // separador
        Divider(
            modifier = Modifier
                .fillMaxWidth()
                .padding(vertical = 15.dp),
            thickness = 1.dp,
        )
        // sector de job
        Text(
            text = "${stringResource(id = R.string.job_sector)} ${job.sector.category.uppercase(Locale.getDefault())} - ${job.sector.subcategory.uppercase(Locale.getDefault())}".trimMargin(),
            modifier = Modifier.fillMaxWidth(),
        )
        // experiencia de job
        Text(
            text = generateExperienceText(
                job.requiredExperience,
                listOf(
                    stringResource(id = R.string.job_experience),
                    stringResource(id = R.string.job_experience_year),
                    stringResource(id = R.string.job_experience_years),
                    stringResource(id = R.string.job_experience_month),
                    stringResource(id = R.string.job_experience_months)
                )
            )?: stringResource(id = R.string.job_experience_none),
            modifier = Modifier
                .fillMaxWidth(),
        )
        // jornada de trabajo
        Text(
            text = "${stringResource(id = R.string.job_availability)} ${stringResource(id = job.workSchedule.displayName)}",
        )
        // separador si hay skills idiomas o formacion
        job.skills.isNotEmpty().or(job.languages?.isNotEmpty()?:false).or(job.requiredEducation?.isNotEmpty()?:false).let {
            if(it) {
                Divider(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 15.dp),
                    thickness = 1.dp,
                )
            }
        }
        // formacion si no es null o vacio
        job.requiredEducation?.values?.firstOrNull()?.let {
            // label de formacion
            Text(
                text = stringResource(id = R.string.job_education)
            )
            // formacion
            Text(
                text = "${it.level.name.capitalize()} - ${it.qualification.capitalize()}",
                fontSize = 12.sp
            )
        }
        // skills si no esta vacio
        if(job.skills.isNotEmpty()) {
            // label de skills
            Text(
                text = stringResource(id = R.string.job_skills),
            )
            // skills
            Text(
                text = job.skills.joinToString(", ") { it.capitalize() },
                fontSize = 12.sp
            )
        }
        // idiomas si no es null o vacio
        job.languages?.let {
            if(it.isNotEmpty()) {
                // label de idiomas
                Text(
                    text = stringResource(id = R.string.job_languages),
                )
                // recorrer idiomas y mostrarlos
                for(language in it) {
                    Text(
                        text = "${language.language.name.capitalize()} - ${language.level.name.capitalize()}",
                        fontSize = 12.sp
                    )
                }
            }
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
            direction = "${job.address.postalCode} ${job.address.city} ${job.address.province}"
        )
        // fecha de publicacion
        Text(
            text = "${stringResource(id = R.string.job_publication_date)} ${job.publicationDate.localFormat(localContext)}",
            modifier = Modifier
                .fillMaxWidth()
                .padding(vertical = 15.dp),
            textAlign = TextAlign.End,
            fontSize = 8.sp
        )
    }
}