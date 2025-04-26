package com.abot.project0z.states

sealed class HomeClientState {
    object Active : HomeClientState()
    object Inactive : HomeClientState()
    object WaitingToken : HomeClientState()
    object WaitingKey : HomeClientState()
    object WaitingSession : HomeClientState()
    data class FailedConnecting(val message: String) : HomeClientState()
    data class FailedAuthenticating(val message: String) : HomeClientState()
    object DebugMode : HomeClientState()
    // Add more states as needed.
}