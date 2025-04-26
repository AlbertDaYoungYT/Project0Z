package com.abot.project0z.layout

import android.icu.text.DecimalFormat
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.LocationOn
import androidx.compose.material.icons.filled.Star
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.ListItem
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.abot.project0z.dataclasses.Mission
import kotlinx.coroutines.launch



@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SectorScreen() {
    // Sample list of missions (replace with your actual data source)
    val missions = remember {
        listOf(
            Mission(
                "Liberate Sector Alpha",
                "Clear out the enemy forces.",
                "Medium",
                "100 XP",
                "Sector Alpha"
            ),
            Mission(
                "Retrieve Data",
                "Recover the lost data packets.",
                "Hard",
                "200 XP",
                "Research Facility"
            ),
            Mission(
                "Defend Outpost",
                "Protect the outpost from attack.",
                "Easy",
                "50 XP",
                "Outpost Delta"
            ),
            Mission(
                "Explore Ruins",
                "Discover the secrets of the ruins.",
                "Medium",
                "150 XP",
                "Ancient Ruins"
            ),
            Mission(
                "Secure the Perimeter",
                "Establish a secure perimeter around the area.",
                "Medium",
                "120 XP",
                "Perimeter Zone"
            ),
            Mission(
                "Eliminate the Threat",
                "Neutralize the high-priority target.",
                "Hard",
                "250 XP",
                "Enemy Stronghold"
            ),
        )
    }

    // State for the Snackbar
    val snackbarHostState = remember { SnackbarHostState() }
    // Coroutine scope for launching coroutines
    val scope = rememberCoroutineScope()

    // User progress state
    val userProgress by remember { mutableFloatStateOf(0.00123f) } // Example initial progress

    Scaffold(
        topBar = {
            TopAppBar(title = { Text("Strategic Operations") })
        },
        snackbarHost = { SnackbarHost(snackbarHostState) }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(16.dp)
        ) {
            // User Progress Section
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("Sector Progress", style = MaterialTheme.typography.headlineSmall)
                Spacer(modifier = Modifier.weight(1f)) // Push the text to the right
                val formattedProgress = remember(userProgress) {
                    DecimalFormat("#.####").format(userProgress)
                }
                Text(
                    text = "$formattedProgress%",
                    style = MaterialTheme.typography.bodyMedium,
                    fontWeight = FontWeight.Bold
                )
            }
            LinearProgressIndicator(
                progress = { userProgress },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 8.dp),
            )
            Spacer(modifier = Modifier.height(16.dp))


            // Available Missions Section
            Text("Available Missions", style = MaterialTheme.typography.headlineSmall)
            LazyColumn(
                modifier = Modifier.fillMaxSize(),
                contentPadding = PaddingValues(vertical = 8.dp)
            ) {
                items(missions) { mission ->
                    MissionCard(mission = mission, onStartMission = {
                        scope.launch {
                            snackbarHostState.showSnackbar("Mission ${mission.name} started!")
                        }
                    })
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MissionCard(mission: Mission, onStartMission: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp)
    ) {
        ListItem(
            headlineContent = { Text(mission.name, fontWeight = FontWeight.Bold) },
            supportingContent = {
                Column {
                    Text(mission.description)
                    Spacer(modifier = Modifier.height(4.dp))
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(
                            Icons.Filled.LocationOn,
                            contentDescription = "Location",
                            modifier = Modifier.size(16.dp),
                            tint = Color.Gray
                        )
                        Spacer(modifier = Modifier.size(4.dp))
                        Text(mission.location, style = MaterialTheme.typography.bodySmall)
                    }
                    Spacer(modifier = Modifier.height(4.dp))
                    Text("Difficulty: ${mission.difficulty}", style = MaterialTheme.typography.bodySmall)
                    Text("Rewards: ${mission.rewards}", style = MaterialTheme.typography.bodySmall)
                }
            },
            leadingContent = {
                Icon(Icons.Filled.Star, contentDescription = "Mission", tint = Color.Yellow)
            },
            trailingContent = {
                Button(onClick = onStartMission) {
                    Text("Start")
                }
            }
        )
    }
}