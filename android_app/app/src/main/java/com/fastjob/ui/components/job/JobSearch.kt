package com.fastjob.ui.components.job

import android.content.res.Configuration
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.MaterialTheme.colorScheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.fastjob.R
import com.fastjob.ui.components.basic.SearchTextField
import com.fastjob.ui.theme.FastjobTheme
import com.fastjob.ui.functions.keywords.management.getJobKeywords
import com.fastjob.ui.viewmodels.search.JobSearchViewModel
import com.fastjob.ui.viewmodels.search.SearchViewModel.SearchState

/**
 * Componente de la pantalla de búsqueda de empleos
 * @param viewModel ViewModel de la pantalla de búsqueda
 */
@Composable
fun JobSearch(
    viewModel: JobSearchViewModel
) {
    // estado de la búsqueda
    val searchState by viewModel.searchState.collectAsState()

    // estado de los filtros
    val filters by viewModel.filters.collectAsState()

    // estado de la búsqueda por palabra clave
    val keywordSearch by viewModel.keyword.collectAsState()

    // efecto para cargar todas las ofertas en la primera carga de la pantalla
    LaunchedEffect(Unit){
        if(searchState == SearchState.START)
            viewModel.setSearchState(SearchState.SEARCH)
    }

    // columna de la pantalla de búsqueda
    Column(
        modifier = Modifier
            .background(color = colorScheme.primary)
            .padding(
                horizontal = 6.dp,
                vertical = 4.dp
            )
            .fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(4.dp)
    ){
        // campo de búsqueda
        SearchTextField(
            viewModel = viewModel,
            placeholder = stringResource(R.string.job_search_placeholder),
            textFieldIcon = painterResource(R.drawable.find),
            textFieldIconDescription = stringResource(R.string.job_search_text_icon_desc),
            autoCompleteFunction = ::getJobKeywords
        )
        // fila de botones de filtros y búsqueda
        Row(
            horizontalArrangement = Arrangement.SpaceBetween,
            modifier = Modifier.fillMaxWidth()
        ){
            // botón de filtros
            JobFilterButton(viewModel)
            // animación del botón de búsqueda
            AnimatedVisibility(
                visible = keywordSearch.isNotEmpty() || !filters.isEmpty(),
                enter = fadeIn(tween(200)),
                exit = fadeOut(tween(200))
            ){
                // botón de búsqueda
                Button(
                    onClick = { viewModel.setSearchState(SearchState.SEARCH) },
                    modifier = Modifier
                        .size(60.dp, 28.dp),
                    colors = ButtonDefaults.buttonColors(
                        containerColor = Color.Transparent,
                    ),
                    contentPadding = PaddingValues(5.dp),
                ) {
                    Text(
                        text = stringResource(id = R.string.search_button),
                        color = colorScheme.tertiary,
                        fontSize = 12.sp
                    )
                }
            }
        }
    }
}

@Preview(showBackground = true)
@Composable
fun JobSearchPreview() {
    FastjobTheme {
        JobSearch(JobSearchViewModel())
    }
}

@Preview(showBackground = true, uiMode = Configuration.UI_MODE_NIGHT_YES)
@Composable
fun JobSearchPreviewDark() {
    FastjobTheme {
        JobSearch(JobSearchViewModel())
    }
}

