package com.abot.project0z.states

sealed class SectorState {
    object HomeSector : SectorState()
    object Liberated : SectorState()
    object Captured : SectorState()
    // Add more states as needed.
}