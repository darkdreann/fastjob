package com.fastjob.ui.components.job

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.expandVertically
import androidx.compose.animation.shrinkVertically
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.ime
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme.colorScheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.ExperimentalComposeUiApi
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.unit.dp
import com.fastjob.R
import com.fastjob.ui.components.basic.TextFieldAutocomplete
import com.fastjob.ui.components.basic.TextFieldList
import com.fastjob.ui.components.basic.TextFieldPicker
import com.fastjob.ui.functions.keywords.management.EducationLevelPicker
import com.fastjob.ui.functions.keywords.management.SubcategoryPicker
import com.fastjob.ui.functions.keywords.management.getEducationNameKeyword
import com.fastjob.ui.functions.keywords.management.getLanguages
import com.fastjob.ui.functions.keywords.management.getProvinceKeyword
import com.fastjob.ui.functions.keywords.management.getSectorCategoryKeyword
import com.fastjob.ui.viewmodels.search.JobSearchViewModel
import com.fastjob.ui.viewmodels.search.SearchViewModel

/**
 * Menu de filtros de busqueda de empleos
 * @param visibilityState estado de visibilidad del menu
 * @param viewModel viewmodel de la pantalla de busqueda de empleos
 */
@OptIn(ExperimentalMaterial3Api::class, ExperimentalComposeUiApi::class)
@Composable
fun JobFilterMenu(
    visibilityState: Pair<Boolean, (Boolean) -> Unit>,
    viewModel: JobSearchViewModel
) {
    // estado de visibilidad del menu
    val (visibility, setVisibility) = visibilityState

    // estado del modal bottom sheet
    val sheetState = rememberModalBottomSheetState()

    // estado de los filtros
    val filtersState by viewModel.filters.collectAsState()

    // picker de subcategorias para el autocomplete de subcategorias
    val subCategoryPicker = remember { SubcategoryPicker() }
    // picker de niveles educativos para el autocomplete de niveles formacion
    val educationLevelPicker = remember { EducationLevelPicker() }

    // estado de los textos de los campos de subcategoria y nivel formacion
    val (textSubCategory, setTextSubCategory) = rememberSaveable { mutableStateOf("") }
    val (textEducationLevel, setTextEducationLevel) = rememberSaveable { mutableStateOf("") }

    // controlador del teclado y accion para el boton de buscar
    val keyBoardController = LocalSoftwareKeyboardController.current
    val keyBoardAction = KeyboardActions(
        onSearch = {
            keyBoardController?.hide()
            setVisibility(false)
            viewModel.setSearchState(SearchViewModel.SearchState.SEARCH)
        }
    )

    // si el menu es visible se muestra el modal bottom sheet
    if(visibility) {
        // modal bottom sheet
        ModalBottomSheet(
            sheetState = sheetState,
            onDismissRequest = {
                setVisibility(false)
            },
            windowInsets = WindowInsets.ime,
            containerColor = colorScheme.tertiary,
        ) {
            // columna con los filtros
            Column(
                modifier = Modifier
                    .verticalScroll(rememberScrollState())
                    .padding(bottom = 60.dp)
                    .imePadding(),
                verticalArrangement = Arrangement.spacedBy(5.dp),
            ) {
                // animacion para el campo de categoria
                AnimatedVisibility(
                    visible = filtersState.sectorId.isEmpty(),
                    enter = expandVertically(),
                    exit = shrinkVertically()
                ){
                    // campo de categoria
                    TextFieldAutocomplete(
                        label = stringResource(id = R.string.job_filter_sector_category),
                        textState = Pair(filtersState.sectorCategory) {
                            viewModel.setCategoryName(it)
                            subCategoryPicker.setCategory(it)
                        },
                        autoCompleteFunction = ::getSectorCategoryKeyword,
                        enabled = filtersState.sectorId.isEmpty(),
                        imeAction = ImeAction.Search,
                        keyBoardAction = keyBoardAction
                    )
                }
                // animacion para el campo de subcategoria
                AnimatedVisibility(
                    visible = filtersState.sectorCategory.isNotEmpty(),
                    enter = expandVertically(),
                    exit = shrinkVertically()
                ){
                    // campo de subcategoria
                    TextFieldPicker(
                        label = stringResource(id = R.string.job_filter_sector_subcategory),
                        setValue = { viewModel.setSectorId(subCategoryPicker.getSectorId(it)) },
                        autoCompleteFunction = subCategoryPicker::getSubcategories,
                        enabled = filtersState.sectorCategory.isNotEmpty(),
                        textState = Pair(textSubCategory, setTextSubCategory),
                        imeAction = ImeAction.Search,
                        keyBoardAction = keyBoardAction
                    )
                }
                // campo de provincia
                TextFieldAutocomplete(
                    label = stringResource(id = R.string.job_filter_provincia),
                    textState = Pair(filtersState.province, viewModel::setProvince),
                    autoCompleteFunction = ::getProvinceKeyword
                )
                // animacion para el campo de formacion
                AnimatedVisibility(
                    visible = filtersState.educationLevelValue.isEmpty(),
                    enter = expandVertically(),
                    exit = shrinkVertically()
                ) {
                    // campo de formacion
                    TextFieldAutocomplete(
                        label = stringResource(id = R.string.job_filter_education_name),
                        textState = Pair(filtersState.educationName, viewModel::setEducationName),
                        autoCompleteFunction = ::getEducationNameKeyword,
                        enabled = filtersState.educationLevelValue.isEmpty(),
                        imeAction = ImeAction.Search,
                        keyBoardAction = keyBoardAction
                    )
                }
                // animacion para el campo de nivel formacion
                AnimatedVisibility(
                    visible = filtersState.educationName.isEmpty(),
                    enter = expandVertically(),
                    exit = shrinkVertically()
                ){
                    // campo de nivel formacion
                    TextFieldPicker(
                        label = stringResource(id = R.string.job_filter_education_level_name),
                        setValue = { viewModel.setEducationLevelValue(educationLevelPicker.getLevelValue(it)) },
                        autoCompleteFunction = educationLevelPicker::getEducationLevels,
                        enabled = filtersState.educationName.isEmpty(),
                        textState = Pair(textEducationLevel, setTextEducationLevel),
                        imeAction = ImeAction.Search,
                        keyBoardAction = keyBoardAction
                    )
                }
                // campo de idiomas
                TextFieldList(
                    label = stringResource(id = R.string.job_filter_language),
                    textState = Pair(filtersState.languages, viewModel::setLanguages),
                    autoCompleteFunction = ::getLanguages,
                    imeAction = ImeAction.Search,
                    keyBoardAction = keyBoardAction
                )
            }

        }
    }
}

