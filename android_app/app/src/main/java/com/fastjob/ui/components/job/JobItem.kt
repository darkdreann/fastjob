package com.fastjob.ui.components.job

import android.content.res.Configuration
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
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import androidx.navigation.compose.rememberNavController
import com.fastjob.R
import com.fastjob.models.MinimalJobIN
import com.fastjob.ui.functions.capitalize
import com.fastjob.ui.functions.capitalizeParagraph
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.theme.FastjobTheme
import java.util.Locale
import java.util.UUID

/**
 * Componente que muestra una oferta de trabajo para hacer una lista de ofertas de trabajo.\
 * @param index Indice de la oferta de trabajo
 * @param job Oferta de trabajo a mostrar
 * @param navController Controlador de navegacion
 */
@Composable
fun JobItem(
    index: Int = 0,
    job: MinimalJobIN,
    navController: NavController
) {
    // numero de lineas que se mostraran en la descripcion
    val descriptionMaxLines = 4
    // imagenes de las ofertas de trabajo
    val firstImage = painterResource(id = R.drawable.job_first)
    val secondImage = painterResource(id = R.drawable.job_second)

    // funcion que se ejecuta cuando se hace click en la oferta de trabajo
    val clickable = {
        navController.navigate(AppScreens.JobCardScreen.route + "/${job.id}/$index")
    }

    // columna que contiene la oferta de trabajo
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 10.dp)
            .clickable(onClick = clickable),
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
    }
}






@Preview(showBackground = true)
@Composable
fun JobItemPreview() {
    FastjobTheme {
        JobItem(
            job = MinimalJobIN(UUID.randomUUID(), "title", "description", "province"),
            navController = rememberNavController()
        )
    }
}

@Preview(showBackground = true, uiMode = Configuration.UI_MODE_NIGHT_YES)
@Composable
fun JobItemPreviewDark() {
    FastjobTheme {
        JobItem(
            index = 1,
            job = MinimalJobIN(UUID.randomUUID(), "title", "description", "province"),
            navController = rememberNavController()
        )
    }
}