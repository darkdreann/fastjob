package com.fastjob.ui.effects

import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.async
import kotlinx.coroutines.withContext

/**
 * Efecto para el autocompletado de palabras
 * @param keyword palabra a buscar
 * @param autocompleteFunction función que devuelve una lista de palabras
 * @param changeValueFunction función que cambia el valor de la lista de palabras
 * @param autocompleteWordState estado si se uso el autocompletado. De esta forma se evita que se busque cuando se cambia el valor por usar el autocompletado
 */
@Composable
fun AutocompleteEffect(
    keyword: String,
    autocompleteFunction: (suspend (keyword: String) -> List<String>?),
    changeValueFunction: (List<String>) -> Unit,
    autocompleteWordState: Pair<Boolean, (Boolean) -> Unit>,
) {
    val (autocompleteWord, setAutocompleteWord) = autocompleteWordState

    // si la palabra cambió, se busca el autocompletado
    LaunchedEffect(keyword) {
        withContext(Dispatchers.IO) {
            when (autocompleteWord) {
                // si se usó el autocompletado, y se cambió la palabra, se cambia el estado a false
                true -> setAutocompleteWord(false)
                // si la palabra cambió, pero no se usó el autocompletado, se busca la lista de palabras
                false -> {
                    async {
                        autocompleteFunction(keyword.replace(".", ""))
                    }.await()
                        ?.let(changeValueFunction)
                }
            }
        }
    }
}