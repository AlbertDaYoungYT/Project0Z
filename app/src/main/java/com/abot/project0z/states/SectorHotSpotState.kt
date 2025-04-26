package com.abot.project0z.states

sealed class SectorHotSpotState {
    object HomeSector : SectorHotSpotState()
    object Liberated : SectorHotSpotState()
    object Captured : SectorHotSpotState()
    object CongestedControl : SectorHotSpotState()
    // Add more states as needed.
}