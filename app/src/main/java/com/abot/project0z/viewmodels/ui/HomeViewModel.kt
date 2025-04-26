package com.abot.project0z.viewmodels.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.abot.project0z.states.HomeClientState
import com.abot.project0z.states.HomeUiState
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class HomeViewModel : ViewModel() {

    private val _uiState = MutableStateFlow<HomeUiState>(HomeUiState.LoggedOut)
    val uiState: StateFlow<HomeUiState> = _uiState.asStateFlow()

    private val _clientState = MutableStateFlow<HomeClientState>(HomeClientState.Inactive)
    val clientState: StateFlow<HomeClientState> = _clientState.asStateFlow()

    init {
        viewModelScope.launch {
            // Simulate client state changes
            delay(1000)
            _clientState.value = HomeClientState.WaitingToken
            delay(1500)
            _clientState.value = HomeClientState.Active

            // Simulate user state changes
            delay(2000)
            _uiState.value = HomeUiState.LoggedIn
        }
    }

    fun logOut() {
        _uiState.value = HomeUiState.LoggedOut
    }
}