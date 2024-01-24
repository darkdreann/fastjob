package com.fastjob.ui.viewmodels.search

import androidx.lifecycle.ViewModel
import kotlinx.coroutines.flow.StateFlow

/**
 * Clase abstracta que representa el ViewModel de una pantalla de búsqueda.
 */
abstract class SearchViewModel: ViewModel() {
    // keyword state
    abstract val keyword: StateFlow<String>
    abstract fun setKeyword(keyword: String)

    // search state
    abstract val searchState: StateFlow<SearchState>
    abstract fun setSearchState(state: SearchState)

    // enum class que representa los estados de la búsqueda
    enum class SearchState {
        START, SEARCH, LOADING, CANCELLED, ERROR, DONE, NOT_FOUND, END_OF_LIST
    }
}