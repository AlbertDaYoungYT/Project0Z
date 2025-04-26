package com.abot.project0z

import android.annotation.SuppressLint
import android.content.Context
import android.os.Bundle
import android.util.Log
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.ComponentActivity
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.navigation.NavHostController
import androidx.navigation.compose.rememberNavController
import com.abot.project0z.config.ConfigContainer
import com.abot.project0z.layout.AppNavGraph
import com.abot.project0z.layout.BottomNavBar
import com.abot.project0z.ui.theme.Project0ZTheme
import com.abot.project0z.utils.Codes
import com.abot.project0z.viewmodels.errors.GlobalErrorView
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import org.reflections.Reflections
import java.io.File
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.collect
import androidx.compose.runtime.rememberCoroutineScope
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.preferencesDataStore
import com.abot.project0z.config.DataStoreContainer
import org.slf4j.Logger
import org.slf4j.LoggerFactory


class MainActivity : ComponentActivity() {

    @SuppressLint("UnusedMaterial3ScaffoldPaddingParameter")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        enableEdgeToEdge()
        dataStoreContainer = DataStoreContainer(this)

        setContent {
            Project0ZTheme(
                darkTheme = config.client.darkTheme ?: isSystemInDarkTheme(),
                dynamicColor = config.client.dynamicColor == true
            ) {
                navController = rememberNavController()

                Scaffold(
                    modifier = Modifier.fillMaxSize(),
                    bottomBar = { BottomNavBar(navController = navController!!) }
                ) { innerPadding ->
                    GlobalErrorView()
                    AppNavGraph(navController = navController!!, innerPadding = innerPadding)
                }
            }
        }
    }

    @SuppressLint("StaticFieldLeak")
    companion object {
        public val logger: Logger = LoggerFactory.getLogger("ProjectZ0") as Logger
        public val config: ConfigContainer = ConfigContainer()
        public val reflector: Reflections = Reflections("com.abot")
        public var navController: NavHostController? = null

        public var dataStoreContainer: DataStoreContainer? = null

        fun getLogger(): Logger {
            return logger
        }
    }
}