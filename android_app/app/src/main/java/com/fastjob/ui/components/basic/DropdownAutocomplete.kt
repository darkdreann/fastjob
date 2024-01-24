package com.fastjob.ui.components.basic

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.ExperimentalAnimationApi
import androidx.compose.animation.core.tween
import androidx.compose.animation.expandVertically
import androidx.compose.animation.shrinkVertically
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.PopupProperties
import com.fastjob.ui.effects.AutocompleteEffect
import com.fastjob.ui.functions.keywords.management.appendToKeyword

/**
 * Menu desplegable para autocompletar textfields con palabras sugeridas.
 * @param modifier: Modifier modificador del dropdown menu
 * @param keywordState: Pair<String, (String) -> Unit> estado de la palabra clave del textfield
 * @param appendWord: Boolean si es true, la palabra sugerida se añade al final de la palabra clave si es false, se reemplaza la palabra por la sugerida
 * @param autocompleteFunction: (suspend (keyword: String) -> List<String>?) funcion que devuelve la lista de palabras para autocompletar
 */
@OptIn(ExperimentalAnimationApi::class)
@Composable
fun DropdownAutocomplete(
    modifier: Modifier = Modifier,
    keywordState: Pair<String, (String) -> Unit>,
    appendWord: Boolean = false,
    autocompleteFunction: (suspend (keyword: String) -> List<String>?)
    ) {
    // estados
    val (wordsList, setWordList) = remember { mutableStateOf(listOf<String>()) }
    val (expanded, setExpanded) = remember { mutableStateOf(false) }
    val (autocompletedWord, setAutocompletedWord) = remember { mutableStateOf(true) }

    // estados de la palabra clave pasados por parametro
    val (keyword, setKeyword) = keywordState


    // effect para obtener la lista de palabras
    AutocompleteEffect(
        keyword = keyword,
        autocompleteFunction = autocompleteFunction,
        changeValueFunction = { word ->
            setWordList(word)
            if(!expanded)
                setExpanded(true)
        },
        autocompleteWordState = Pair(autocompletedWord, setAutocompletedWord)
    )

    // animacion del menu desplegable
    AnimatedVisibility(
        visible = expanded,
        modifier = Modifier.then(modifier),
        ) {
        // dropdown menu
        DropdownMenu(
            expanded = expanded,
            onDismissRequest = {
                setExpanded(false)
            },
            properties = PopupProperties(
                focusable = false
            ),
            modifier = Modifier
                .animateEnterExit(
                    enter = expandVertically(tween(200)),
                    exit = shrinkVertically(tween(200))
                )
                .heightIn(0.dp, 140.dp)
        ) {
            // crear un dropdown menu item por cada palabra sugerida
            wordsList.forEach { word ->
                DropdownMenuItem(
                    modifier = Modifier
                        .height(30.dp)
                        .then(modifier),
                    text = {
                        Text(text = word)
                    },
                    onClick = {
                        setAutocompletedWord(true)
                        setKeyword(
                            if (appendWord) appendToKeyword(keyword, word) else word
                        )
                        setExpanded(false)
                    }
                )
            }
        }
    }
}

