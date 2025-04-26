package com.abot.project0z.layout

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Settings
import androidx.compose.ui.graphics.vector.ImageVector

sealed class BottomNavDestination(val route: String, val icon: ImageVector, val title: String) {
    object Home : BottomNavDestination("home",
        Icons.Filled.Home, "Home")
    object Profile : BottomNavDestination("profile",
        Icons.Filled.Person, "Profile")
    object Settings : BottomNavDestination("settings",
        Icons.Filled.Settings, "Settings")
}