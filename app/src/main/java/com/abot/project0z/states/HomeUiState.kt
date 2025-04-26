package com.abot.project0z.states

sealed class HomeUiState {
    object LoggedIn : HomeUiState()
    object LoggedOut : HomeUiState()
    object AwaitingVerification : HomeUiState()
    // Add more states as needed.
    data class Error(val message: String) : HomeUiState()
}