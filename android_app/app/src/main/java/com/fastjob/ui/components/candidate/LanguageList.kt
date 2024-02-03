package com.fastjob.ui.components.candidate

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.fastjob.R
import com.fastjob.ui.components.basic.ErrorItem
import com.fastjob.ui.components.basic.LoadingItem
import com.fastjob.ui.effects.LoadLanguagesEffect
import com.fastjob.ui.enums.LoadState
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.viewmodels.form.candidate.LanguageListViewModel

/**
 * Lista de experiencias del candidato
 * @param itemsRefreshOffset offset de items para refrescar la lista
 * @param viewModel ViewModel de la lista de idiomas
 * @param navController NavController para la navegacion
 */
@Composable
fun LanguageList(
    itemsRefreshOffset: Int = 1,
    viewModel: LanguageListViewModel,
    navController: NavController
) {

    // estado de la carga
    val loadState by viewModel.loadState.collectAsState()

    // lista de idiomas
    val languageList by viewModel.languageList.collectAsState()

    // estado del scroll
    val scrollState by viewModel.listScroll.collectAsState()

    // estado de si se llego al final del scroll
    val isItemReachEndScroll by remember {
        derivedStateOf {
            scrollState.layoutInfo.visibleItemsInfo.lastOrNull()?.index == scrollState.layoutInfo.totalItemsCount - if(scrollState.layoutInfo.totalItemsCount<itemsRefreshOffset) 1 else itemsRefreshOffset
        }
    }

    LoadLanguagesEffect(
        viewModel = viewModel,
        isItemReachEndScroll = isItemReachEndScroll,
        loadState = loadState
    )

    LazyColumn(
        state = scrollState,
        verticalArrangement = languageList.isEmpty().let {
            if (it) Arrangement.Center
            else Arrangement.spacedBy(4.dp)
        },
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = Modifier
            .fillMaxWidth()
            .fillMaxHeight(),
    ) {
        // items de la lista
        itemsIndexed(languageList) { _, item ->
            LanguageCard(
                candidateLanguage = item,
                edit = {
                    navController.navigate(AppScreens.CandidateEditLanguageScreen.route + "/${it}")
                },
                delete = {
                    viewModel.deleteLanguage(it)
                }
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