package com.abot.project0z.layout.views

import androidx.compose.foundation.layout.Column
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.tooling.preview.Preview
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavHostController
import com.abot.project0z.MainActivity
import com.abot.project0z.layout.Destination
import com.abot.project0z.states.HomeClientState
import com.abot.project0z.states.HomeUiState
import com.abot.project0z.viewmodels.ui.HomeViewModel
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.util.UUID

@Preview
@Composable
fun HomeView(
    navController: NavHostController? = null,
    viewModel: HomeViewModel = viewModel()
) {
    val uiState by viewModel.uiState.collectAsState()
    val clientState by viewModel.clientState.collectAsState()

    val token = remember { mutableStateOf("") }


    Column {
        // Display client state
        when (clientState) {
            is HomeClientState.Active -> Text("Client: Active")
            is HomeClientState.Inactive -> Text("Client: Inactive")
            is HomeClientState.WaitingToken -> Text("Client: Waiting for Token")
            is HomeClientState.WaitingKey -> Text("Client: Waiting for Key")
            is HomeClientState.WaitingSession -> Text("Client: Waiting for Session")
            is HomeClientState.FailedConnecting -> Text("Client: Failed Connecting: ${(clientState as HomeClientState.FailedConnecting).message}")
            is HomeClientState.FailedAuthenticating -> Text("Client: Failed Authenticating: ${(clientState as HomeClientState.FailedAuthenticating).message}")
            is HomeClientState.DebugMode -> Text("Client: Debug Mode")
        }

        // Display UI state
        when (uiState) {
            is HomeUiState.LoggedIn -> {
                LaunchedEffect(Unit) {
                    DataStoreManager.readBoolean(MainActivity.dataStoreContainer.accountData.isLoggedIn).collect { res ->
                        if (res == true) {
                            DataStoreManager.readString(MainActivity.dataStoreContainer.accountData.token).collect { resToken ->
                                token.value = resToken.toString()
                            }
                        } else {
                            token.value = UUID.randomUUID().toString()
                            DataStoreManager.saveString(MainActivity.dataStoreContainer.accountData.token, token.value)
                        }
                    }
                }
                Text("Logged In as @")
                Button(onClick = { viewModel.logOut() }) {
                    Text("Log out")
                }
            }

            is HomeUiState.LoggedOut -> Text("Logged Out")
            is HomeUiState.AwaitingVerification -> Text("Awaiting Verification")
            is HomeUiState.Error -> Text("Error : ${(uiState as HomeUiState.Error).message}")

        }

        if (navController != null) {
            Button(onClick = { navController.navigate(Destination.Profile.route) }) {
                Text("Go to Profile")
            }
        }
    }
}
