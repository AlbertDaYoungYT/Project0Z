package com.abot.project0z.layout

import androidx.navigation.NamedNavArgument
import androidx.navigation.NavType
import androidx.navigation.navArgument

sealed class Destination(val route: String, val navArguments: List<NamedNavArgument> = emptyList()) {
    object Home : Destination("home")
    object Profile : Destination("profile")
    object Settings : Destination("settings")
    object Details : Destination(
        "details/{itemId}",
        listOf(navArgument("itemId") { type = NavType.StringType })
    ) {
        fun createRoute(itemId: String) = "details/$itemId"
    }
    // Add more destinations as your app grows
}