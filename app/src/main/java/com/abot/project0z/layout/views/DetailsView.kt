package com.abot.project0z.layout.views

import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.tooling.preview.Preview
import androidx.navigation.NavHostController
import com.abot.project0z.layout.Destination

@Preview
@Composable
fun DetailsView(navController: NavHostController? = null, itemId: String? = "none") {
    Text("Details View: $itemId")
}