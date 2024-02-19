package com.fastjob.ui.components.company

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.material3.Divider
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.fastjob.R
import com.fastjob.ui.components.basic.ErrorItem
import com.fastjob.ui.components.basic.LoadingItem
import com.fastjob.ui.components.candidate.ExperienceCard
import com.fastjob.ui.effects.CandidateCardLoadExperiencesEffect
import com.fastjob.ui.enums.LoadState
import com.fastjob.ui.viewmodels.company.CandidateCardExperienceListViewModel

/**
 * Lista de experiencias del candidato
 * @param itemsRefreshOffset offset de items para refrescar la lista
 * @param viewModel ViewModel de la lista de experiencias
 */
@Composable
fun CandidateCardExperienceList(
    itemsRefreshOffset: Int = 1,
    viewModel: CandidateCardExperienceListViewModel
) {

    // estado de la carga
    val loadState by viewModel.loadState.collectAsState()

    // lista de experiencias
    val experienceList by viewModel.experienceList.collectAsState()

    // estado del scroll
    val scrollState by viewModel.listScroll.collectAsState()

    // estado de si se llego al final del scroll
    val isItemReachEndScroll by remember {
        derivedStateOf {
            scrollState.layoutInfo.visibleItemsInfo.lastOrNull()?.index == scrollState.layoutInfo.totalItemsCount - if(scrollState.layoutInfo.totalItemsCount<itemsRefreshOffset) 1 else itemsRefreshOffset
        }
    }

    CandidateCardLoadExperiencesEffect(
        viewModel = viewModel,
        isItemReachEndScroll = isItemReachEndScroll,
        loadState = loadState
    )

    Column{
        Text(
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 16.dp, top = 10.dp),
            text = stringResource(id = R.string.experience_list_title),
            fontSize = 25.sp,
            textAlign = TextAlign.Center
        )
        LazyColumn(
            state = scrollState,
            verticalArrangement = experienceList.isEmpty().let {
                if (it) Arrangement.Center
                else Arrangement.spacedBy(4.dp)
            },
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier
                .fillMaxWidth()
                .fillMaxHeight(),
        ) {
            // items de la lista
            itemsIndexed(experienceList) { _, item ->
                ExperienceCard(
                    experience = item,
                )
                Divider(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 15.dp),
                    thickness = 1.dp,
                )
            }

            // item de carga y error
            when (loadState) {
                // item de carga
                LoadState.LOADING -> {
                    item {
                        LoadingItem("")
                    }
                }
                // item de error de no se encontraron items
                LoadState.NOT_FOUND -> {
                    item {
                        ErrorItem(
                            text = stringResource(id = R.string.exp_not_found)
                        )
                    }
                }
                // item de error de carga
                LoadState.ERROR -> {
                    item {
                        ErrorItem(
                            text = stringResource(id = R.string.list_error)
                        )
                    }
                }
                // else para acabar el when
                else -> {}
            }
        }
    }
}