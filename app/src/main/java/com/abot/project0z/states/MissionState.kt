package com.abot.project0z.states

sealed class MissionState {
    object Extracted : MissionState()
    object Extracting : MissionState()
    object MovingToExtraction : MissionState()
    object Completed : MissionState()
    object InProgress : MissionState()
    object Starting : MissionState()
    object MovingToDropPoint : MissionState()
    object FindingMatch : MissionState()
    object JoiningMatch : MissionState()
    // Add more states as needed.
    data class Error(val message: String) : MissionState()

}