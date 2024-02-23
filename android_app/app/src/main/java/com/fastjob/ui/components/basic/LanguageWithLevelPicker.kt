package com.fastjob.ui.components.basic

import android.widget.Toast
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.ExperimentalAnimationApi
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme.colorScheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.DialogProperties
import com.fastjob.R
import com.fastjob.ui.functions.keywords.management.LanguageLevelPicker
import com.fastjob.ui.functions.keywords.management.LanguagePicker
import com.fastjob.ui.functions.toUUID
import com.fastjob.ui.viewmodels.company.CreateCompanyJobViewModel
import com.fastjob.ui.viewmodels.interfaces.JobLanguage

/**
 * Muestra un dialogo con un picker para seleccionar un idioma y un nivel
 * @param viewModel view model de la vista
 */
@OptIn(ExperimentalMaterial3Api::class, ExperimentalAnimationApi::class)
@Composable
fun LanguageWithLevelPicker(
    viewModel: CreateCompanyJobViewModel
) {
    // context
    val context = LocalContext.current
    val addErrorMsg = stringResource(id = R.string.job_language_add_error)


    // lista de idiomas
    val languages by viewModel.jobLanguages.collectAsState()

    // estado del dialogo
    var dialogVisibility by remember { mutableStateOf(false) }

    // estado idioma actual
    var currentJobLanguage by remember { mutableStateOf(JobLanguage()) }

    // pickers
    val languagePicker = remember { LanguagePicker() }
    val languageLevelPicker = remember { LanguageLevelPicker() }

    // estado de errores
    var languageError by remember { mutableStateOf(false) }
    var languageLevelError by remember { mutableStateOf(false) }

    // animacion de entrada y salida
    AnimatedVisibility(
        visible = dialogVisibility,
        enter = fadeIn(),
        exit = fadeOut()
    ){
        // dialogo del date picker
        AlertDialog(
            onDismissRequest = { dialogVisibility = false },
            properties = DialogProperties(
                usePlatformDefaultWidth = false,
            ),
            modifier = Modifier
                .fillMaxWidth()
                .background(colorScheme.background)
                .padding(horizontal = 5.dp)
                .animateEnterExit(
                    enter = fadeIn(),
                    exit = fadeOut()
                )
                .padding(horizontal = 10.dp)
        ) {

           Column(
                modifier = Modifier
                     .fillMaxWidth()
                     .padding(10.dp),
                verticalArrangement = Arrangement.spacedBy(10.dp)
           ) {

               Text(
                   text = stringResource(id = R.string.job_add_language),
                   fontSize = 20.sp,
               )

               TextFieldPicker(
                   padding = 0.dp,
                   label = stringResource(id = R.string.job_language_name),
                   setValue = { currentJobLanguage = currentJobLanguage.copy(languageId = languagePicker.getLanguageId(it).toUUID())},
                   textState = Pair(currentJobLanguage.languageName){
                       currentJobLanguage = currentJobLanguage.copy(languageName = it)
                   },
                   autoCompleteFunction = languagePicker::getLanguages,
                   isError = languageError,
               )

               TextFieldPicker(
                   padding = 0.dp,
                   label = stringResource(id = R.string.job_language_level),
                   setValue = { currentJobLanguage = currentJobLanguage.copy(languageLevelId = languageLevelPicker.getLevelId(it).toUUID())},
                   textState = Pair(currentJobLanguage.languageLevelName){
                       currentJobLanguage = currentJobLanguage.copy(languageLevelName = it)
                   },
                   autoCompleteFunction = languageLevelPicker::getLanguageLevels,
                   isError = languageError,
               )

               Row(
                   modifier = Modifier
                       .fillMaxWidth(),
                   horizontalArrangement = Arrangement.SpaceBetween
               ) {
                   TextButton(
                       onClick = {
                            dialogVisibility = false
                            currentJobLanguage = JobLanguage()
                       }
                   ) {
                       Text(text = stringResource(id = R.string.cancel_button))
                   }

                   TextButton(
                       onClick = {
                           if(currentJobLanguage.languageId != null && currentJobLanguage.languageLevelId != null) {
                               viewModel.setJobLanguages(
                                   languages + currentJobLanguage
                               )
                               dialogVisibility = false
                               currentJobLanguage = JobLanguage()
                           }else{
                               languageError = currentJobLanguage.languageId == null
                               languageLevelError = currentJobLanguage.languageLevelId == null
                               Toast.makeText(context, addErrorMsg, Toast.LENGTH_SHORT).show()
                           }
                       }
                   ) {
                       Text(text = stringResource(id = R.string.job_add_language))
                   }
               }
           }

        }
    }

    Column(
        modifier = Modifier
            .fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(6.dp)
    ){
        Button(
            modifier = Modifier
                .fillMaxWidth(),
            colors = ButtonDefaults.buttonColors(
                containerColor = colorScheme.primary,
                contentColor = colorScheme.tertiary
            ),
            onClick = {
                dialogVisibility = true
            }
        ) {
            Text(text = stringResource(id = R.string.job_add_language))
        }


        LazyColumn(
            modifier = Modifier
                .fillMaxWidth()
                .heightIn(min = 0.dp, max = 200.dp)
        ){
            itemsIndexed(languages) { index, item ->
                TextField(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(20.dp)),
                    readOnly = true,
                    value = "${item.languageName} - ${item.languageLevelName}",
                    onValueChange = {},
                    trailingIcon = {
                        IconButton(
                            onClick = {
                                viewModel.setJobLanguages(
                                    languages.filterIndexed { i, _ -> i != index }
                                )
                            }
                        ) {
                            Icon(
                                painter = painterResource(id = R.drawable.delete),
                                contentDescription = stringResource(id = R.string.job_delete_language_icon_desc)
                            )
                        }
                    }
                )
            }
        }
    }



}