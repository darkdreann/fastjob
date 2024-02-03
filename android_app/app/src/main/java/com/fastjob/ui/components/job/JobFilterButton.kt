package com.fastjob.ui.components.job

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.size
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme.colorScheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.fastjob.R
import com.fastjob.ui.viewmodels.search.JobSearchViewModel

/**
 * Boton de filtros de busqueda de empleo
 * @param viewModel: ViewModel de la pantalla de busqueda de empleo
 */
@Composable
fun JobFilterButton(
    viewModel: JobSearchViewModel
) {
    // estado de visibilidad del menu de filtros
    val (visibility, setVisibility) = rememberSaveable { mutableStateOf(false) }

    // boton de filtros
    Button(
        onClick = {
            setVisibility(true)
        },
        colors = ButtonDefaults.buttonColors(
            containerColor = colorScheme.tertiary
        ),
        modifier = Modifier
            .size(60.dp, 28.dp),
        contentPadding = PaddingValues(5.dp),
    )
    {
        // fila con icono y texto
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .height(30.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.Center
        ){
            // icono
            Icon(
                modifier = Modifier.size(15.dp),
                painter = painterResource(id = R.drawable.advanced),
                contentDescription = stringResource(id = R.string.job_search_button_icon_desc),
                tint = colorScheme.secondary,
            )
            // texto
            Text(
                text = stringResource(id = R.string.job_search_button_text),
                fontSize = 10.sp,
                color = colorScheme.secondary
            )
        }
    }
    JobFilterMenu(
        visibilityState = Pair(visibility, setVisibility),
        viewModel = viewModel
    )

}
