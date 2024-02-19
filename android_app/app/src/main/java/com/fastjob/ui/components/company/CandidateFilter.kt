package com.fastjob.ui.components.company

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.ExperimentalAnimationApi
import androidx.compose.animation.expandVertically
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.shrinkVertically
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.IconButtonColors
import androidx.compose.material3.IconButtonDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.MaterialTheme.colorScheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.ExperimentalComposeUiApi
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.DialogProperties
import androidx.core.text.isDigitsOnly
import com.fastjob.R
import com.fastjob.models.Availability
import com.fastjob.ui.components.basic.Selectable
import com.fastjob.ui.components.basic.TextFieldAutocomplete
import com.fastjob.ui.components.basic.TextFieldList
import com.fastjob.ui.components.basic.TextFieldPicker
import com.fastjob.ui.functions.keywords.management.EducationLevelPicker
import com.fastjob.ui.functions.keywords.management.LanguageLevelPicker
import com.fastjob.ui.functions.keywords.management.SubcategoryPicker
import com.fastjob.ui.functions.keywords.management.getEducationNameKeyword
import com.fastjob.ui.functions.keywords.management.getLanguages
import com.fastjob.ui.functions.keywords.management.getProvinceKeyword
import com.fastjob.ui.functions.keywords.management.getSectorCategoryKeyword
import com.fastjob.ui.viewmodels.search.CandidateSearchViewModel
import com.fastjob.ui.viewmodels.search.SearchViewModel

/**
 * Menu de filtros de busqueda de candidatos
 * @param viewModel viewmodel de la pantalla de busqueda de candidatos
 */
@OptIn(ExperimentalMaterial3Api::class, ExperimentalComposeUiApi::class,
    ExperimentalAnimationApi::class
)
@Composable
fun CandidateFilter(
    viewModel: CandidateSearchViewModel
) {
    // estado de visibilidad del menu
    var visibility by remember { mutableStateOf(false) }

    // estado de los filtros
    val filtersState by viewModel.filters.collectAsState()

    // picker de subcategorias para el autocomplete de subcategorias
    val subCategoryPicker = remember { SubcategoryPicker() }
    // picker de niveles educativos para el autocomplete de niveles formacion
    val educationLevelPicker = remember { EducationLevelPicker() }
    // picker de niveles de idiomas para el autocomplete de niveles idiomas
    val languageLevelPicker = remember { LanguageLevelPicker() }

    // estado de los textos de los campos de subcategoria y nivel formacion
    val (textEducationLevel, setTextEducationLevel) = rememberSaveable { mutableStateOf("") }
    val (subcategory, setSubcategory) = rememberSaveable { mutableStateOf("") }


    // controlador del teclado y accion para el boton de buscar
    val keyBoardController = LocalSoftwareKeyboardController.current
    val keyBoardAction = KeyboardActions(
        onSearch = {
            keyBoardController?.hide()
            visibility = false
            viewModel.setSearchState(SearchViewModel.SearchState.SEARCH)
        }
    )

    AnimatedVisibility(
        visible = visibility,
        enter = fadeIn(),
        exit = fadeOut()
    ){
        // filter dialog
        AlertDialog(
            modifier = Modifier
                .animateEnterExit(
                    enter = fadeIn(),
                    exit = fadeOut()
                )
                .background(colorScheme.background)
                .padding(horizontal = 10.dp, vertical = 20.dp),
            onDismissRequest = {
                visibility = false
            },
        ) {


            Box(
                contentAlignment = Alignment.Center
            ){// columna con los filtros
                Column(
                    modifier = Modifier
                        .verticalScroll(rememberScrollState())
                        .imePadding(),
                    verticalArrangement = Arrangement.spacedBy(7.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {

                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(10.dp),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Text(
                            text = stringResource(id = R.string.job_search_button_text),
                            fontSize = 20.sp
                        )
                        // botón de búsqueda
                        TextButton(
                            onClick = {
                                visibility = false
                                viewModel.setSearchState(SearchViewModel.SearchState.SEARCH)
                              },
                            modifier = Modifier
                                .size(60.dp, 28.dp),
                            contentPadding = PaddingValues(5.dp),
                        ) {
                            Text(
                                text = stringResource(id = R.string.search_button),
                                color = colorScheme.primary,
                                fontSize = 15.sp
                            )
                        }
                    }

                    // animacion para el campo de categoria
                    AnimatedVisibility(
                        visible = subcategory.isEmpty(),
                        enter = expandVertically(),
                        exit = shrinkVertically()
                    ) {
                        // campo de categoria
                        TextFieldAutocomplete(
                            modifier = Modifier
                                .clip(RoundedCornerShape(20.dp)),
                            label = stringResource(id = R.string.job_filter_sector_category),
                            textState = Pair(filtersState.sectorCategory) {
                                viewModel.setCandidateFilters(filtersState.copy(sectorCategory = it))
                                subCategoryPicker.setCategory(it)
                            },
                            autoCompleteFunction = ::getSectorCategoryKeyword,
                            enabled = subcategory.isEmpty(),
                            imeAction = ImeAction.Search,
                            keyBoardAction = keyBoardAction
                        )
                    }
                    // animacion para el campo de subcategoria
                    AnimatedVisibility(
                        visible = filtersState.sectorCategory.isNotEmpty(),
                        enter = expandVertically(),
                        exit = shrinkVertically()
                    ) {
                        // campo de subcategoria
                        TextFieldPicker(
                            modifier = Modifier
                                .clip(RoundedCornerShape(20.dp)),
                            label = stringResource(id = R.string.job_filter_sector_subcategory),
                            setValue = {
                                viewModel.setCandidateFilters(
                                    filtersState.copy(
                                        sectorId = subCategoryPicker.getSectorId(
                                            it
                                        )
                                    )
                                )
                            },
                            autoCompleteFunction = subCategoryPicker::getSubcategories,
                            enabled = filtersState.sectorCategory.isNotEmpty(),
                            textState = Pair(subcategory, setSubcategory),
                            imeAction = ImeAction.Search,
                            keyBoardAction = keyBoardAction
                        )
                    }
                    // campo de provincia
                    TextFieldAutocomplete(
                        modifier = Modifier
                            .clip(RoundedCornerShape(20.dp)),
                        label = stringResource(id = R.string.candidate_filter_address),
                        textState = Pair(filtersState.address) {
                            viewModel.setCandidateFilters(filtersState.copy(address = it))
                        },
                        autoCompleteFunction = ::getProvinceKeyword,
                        imeAction = ImeAction.Search,
                        keyBoardAction = keyBoardAction
                    )
                    // animacion para el campo de formacion
                    AnimatedVisibility(
                        visible = filtersState.educationLevelValue.isEmpty(),
                        enter = expandVertically(),
                        exit = shrinkVertically()
                    ) {
                        // campo de formacion
                        TextFieldAutocomplete(
                            modifier = Modifier
                                .clip(RoundedCornerShape(20.dp)),
                            label = stringResource(id = R.string.job_filter_education_name),
                            textState = Pair(filtersState.educationName) {
                                viewModel.setCandidateFilters(filtersState.copy(educationName = it))
                            },
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
                    ) {
                        // campo de nivel formacion
                        TextFieldPicker(
                            modifier = Modifier
                                .clip(RoundedCornerShape(20.dp)),
                            label = stringResource(id = R.string.job_filter_education_level_name),
                            setValue = {
                                viewModel.setCandidateFilters(
                                    filtersState.copy(
                                        educationLevelValue = educationLevelPicker.getLevelValue(it)
                                    )
                                )
                            },
                            autoCompleteFunction = educationLevelPicker::getEducationLevels,
                            enabled = filtersState.educationName.isEmpty(),
                            textState = Pair(textEducationLevel, setTextEducationLevel),
                            imeAction = ImeAction.Search,
                            keyBoardAction = keyBoardAction
                        )
                    }
                    // campo de idiomas
                    TextFieldAutocomplete(
                        modifier = Modifier
                            .clip(RoundedCornerShape(20.dp)),
                        label = stringResource(id = R.string.job_filter_language),
                        textState = Pair(filtersState.languages) {
                            viewModel.setCandidateFilters(filtersState.copy(languages = it))
                        },
                        autoCompleteFunction = ::getLanguages,
                        imeAction = ImeAction.Search,
                        keyBoardAction = keyBoardAction
                    )
                    // animacion para el campo de nivel formacion
                    AnimatedVisibility(
                        visible = filtersState.languages.isNotEmpty(),
                        enter = expandVertically(),
                        exit = shrinkVertically()
                    ) {
                        // campo de nivel formacion
                        TextFieldPicker(
                            modifier = Modifier
                                .clip(RoundedCornerShape(20.dp)),
                            label = stringResource(id = R.string.job_filter_education_level_name),
                            setValue = {
                                viewModel.setCandidateFilters(
                                    filtersState.copy(
                                        languageLevel = languageLevelPicker.getLevelId(it)
                                    )
                                )
                            },
                            autoCompleteFunction = languageLevelPicker::getLanguageLevels,
                            enabled = filtersState.educationName.isEmpty(),
                            textState = Pair(textEducationLevel, setTextEducationLevel),
                            imeAction = ImeAction.Search,
                            keyBoardAction = keyBoardAction
                        )
                    }
                    // textfield de la experiencia
                    TextField(
                        singleLine = true,
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 10.dp)
                            .clip(RoundedCornerShape(20.dp)),
                        label = { Text(stringResource(id = R.string.candidate_filter_exp)) },
                        value = filtersState.experienceMonths,
                        onValueChange = {
                            // si es un numero y tiene menos de 5 digitos se cambia
                            if (it.length <= 5 && it.isDigitsOnly()) {
                                viewModel.setCandidateFilters(filtersState.copy(experienceMonths = it))
                            }
                        },
                        keyboardOptions = KeyboardOptions(
                            keyboardType = KeyboardType.Number,
                            imeAction = ImeAction.Search
                        ),
                        keyboardActions = keyBoardAction,
                    )
                    TextFieldList(
                        label = stringResource(id = R.string.candidates_skills),
                        textState = Pair(filtersState.skills.toList()) {
                            viewModel.setCandidateFilters(filtersState.copy(skills = it.toSet()))
                        },
                        imeAction = ImeAction.Search,
                        keyBoardAction = keyBoardAction
                    )
                    // disponibilidad
                    Selectable(
                        label = stringResource(id = R.string.candidate_availability),
                        itemPossibilities = Availability.values().toList(),
                        selected = filtersState.availability,
                        getStringResource = { it?.displayName },
                        setSelected = {
                            viewModel.setCandidateFilters(
                                filtersState.copy(
                                    availability = it?.value ?: ""
                                )
                            )
                        },
                        stringToClass = { Availability.getByValueNullable(it) }
                    )

                }
            }
        }
    }

    IconButton(
        onClick = { visibility = true },
        colors = IconButtonDefaults.iconButtonColors(
            containerColor = colorScheme.secondary,
            contentColor = colorScheme.tertiary
        )
    ) {
        Icon(
            painter = painterResource(id = R.drawable.advanced),
            contentDescription = stringResource(id = R.string.job_search_button_icon_desc),
        )
    }
}

