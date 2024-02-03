package com.fastjob.ui.components.form

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import com.fastjob.R
import com.fastjob.ui.components.basic.BasicDialog
import com.fastjob.ui.components.basic.ErrorItem
import com.fastjob.ui.components.basic.LoadingItem
import com.fastjob.ui.components.basic.TextFieldPicker
import com.fastjob.ui.enums.LoadState
import com.fastjob.ui.functions.keywords.management.LanguageLevelPicker
import com.fastjob.ui.functions.keywords.management.LanguagePicker
import com.fastjob.ui.functions.toUUID
import com.fastjob.ui.viewmodels.form.candidate.CandidateLanguageViewModel

/**
 * Formulario de idioma del candidato
 * @param viewModel ViewModel del formulario de idioma
 */
@Composable
fun CandidateLanguageForm(
    viewModel: CandidateLanguageViewModel
) {

    // estado del idioma
    val language by viewModel.language.collectAsState()

    // estado de error del idioma
    val languageError by viewModel.languageError.collectAsState()

    // estado de carga
    val loadState by viewModel.loadState.collectAsState()

    // estado del dialogo de error
    val errorVisibility by viewModel.errorVisibility.collectAsState()

    // picker de language y level
    val languagePicker = remember { LanguagePicker() }
    val languageLevelPicker = remember { LanguageLevelPicker() }

    // estado del nombre y nombre del nivel del idioma
    val (languageName, setLanguageName) = remember { mutableStateOf("") }
    val (languageLevelName, setLanguageLevelName) = remember { mutableStateOf("") }


    // carga del idioma
    LaunchedEffect(Unit){
        viewModel.loadLanguage(setLanguageName)
    }

    // item de carga y error
    when (loadState) {
        // item de carga
        LoadState.LOADING -> {
            Box(
                modifier = Modifier
                    .fillMaxSize(),
                contentAlignment = Alignment.Center
            ){
                LoadingItem("")
            }
        }
        // item de error de carga
        LoadState.ERROR -> {
            Box(
                modifier = Modifier
                    .fillMaxSize(),
                contentAlignment = Alignment.Center
            ){
                ErrorItem(
                    text = stringResource(id = R.string.list_error)
                )
            }
        }
        LoadState.LOADED -> {
            BasicDialog(
                title = stringResource(id = R.string.candidate_language_error_title),
                content = stringResource(id = R.string.candidate_language_error_msg),
                icon = painterResource(id = R.drawable.error),
                visibilityState = Pair(errorVisibility, viewModel::setErrorVisibility))

            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(16.dp)
                    .imePadding()
                    .verticalScroll(rememberScrollState()),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.spacedBy(10.dp)
            ) {

                // imagen de usuario
                Image(
                    modifier = Modifier
                        .fillMaxWidth(),
                    painter = painterResource(id = R.drawable.user_img),
                    contentDescription = stringResource(id = R.string.user_image_desc),
                )

                // campo de idioma
                TextFieldPicker(
                    padding = 0.dp,
                    label = stringResource(id = R.string.candidate_language),
                    setValue = { viewModel.setLanguage(language.copy(languageId = languagePicker.getLanguageId(it).toUUID()))},
                    textState = Pair(languageName){
                        viewModel.setLanguage(language.copy(languageName = it))
                        setLanguageName(it)
                    },
                    autoCompleteFunction = languagePicker::getLanguages,
                    readOnly = !viewModel.isNewLanguage(),
                    isError = languageError.languageId,
                )

                // campo de nivel idioma
                TextFieldPicker(
                    padding = 0.dp,
                    label = stringResource(id = R.string.candidate_language_level),
                    setValue = { viewModel.setLanguage(language.copy(levelId = languageLevelPicker.getLevelId(it).toUUID()))},
                    textState = Pair(languageLevelName){
                        viewModel.setLanguage(language.copy(levelName = it))
                        setLanguageLevelName(it)
                    },
                    autoCompleteFunction = languageLevelPicker::getLanguageLevels,
                    isError = languageError.levelId,
                )

                // botón de guardar
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 10.dp),
                    contentAlignment = Alignment.BottomEnd
                ){
                    TextButton(
                        onClick = {
                            viewModel.saveLanguage()
                        }
                    ) {
                        Text(text = stringResource(id = R.string.save_button))
                    }
                }
            }

        }
        // else para acabar el when
        else -> {}
    }



}