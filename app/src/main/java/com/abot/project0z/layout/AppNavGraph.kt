package com.abot.project0z.layout

import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.padding
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import com.abot.project0z.layout.views.HomeView
import com.abot.project0z.layout.views.ProfileView
import com.abot.project0z.layout.views.SettingsView
import com.abot.project0z.layout.views.DetailsView

@Composable
fun AppNavGraph(
    navController: NavHostController,
    innerPadding: PaddingValues
) {
    NavHost(
        navController = navController,
        startDestination = Destination.Home.route,
        modifier = Modifier.padding(innerPadding)
    ) {
        composable(Destination.Home.route) {
            HomeView(navController = navController)
        }
        composable(Destination.Profile.route) {
            ProfileView(navController = navController)
        }
        composable(Destination.Settings.route) {
            SettingsView(navController = navController)
        }
        composable(
            route = Destination.Details.route,
            arguments = Destination.Details.navArguments
        ) {
            val itemId = it.arguments?.getString("itemId")
                ?: throw IllegalStateException("No item ID")
            DetailsView(navController, itemId)
        }
        // Add more composable for additional destinations
    }
}