package com.abot.project0z.config

import android.graphics.Region
import androidx.compose.foundation.isSystemInDarkTheme
import com.abot.project0z.MainActivity
import com.google.android.gms.common.util.JsonUtils
import kotlinx.serialization.json.JsonObject
import java.lang.reflect.Field
import java.util.Arrays
import java.util.Locale
import java.util.logging.Level


class ConfigContainer {
    var databaseInfo: Database = Database()
    var language: Language = Language()
    var account: Account = Account()
    var client: Client = Client()

    /* Option containers. */
    class Database {
        var http: DataStore = DataStore()
        var game: DataStore = DataStore()

        class DataStore {
            // TODO Create Android inbuilt DataStore
        }
    }

    class Client {
        val args: ARGS = ARGS()
        var http: HTTP = HTTP()
        var game: Game = Game()

        var darkTheme: Boolean? = null
        var dynamicColor: Boolean? = true
    }

    class Language {
        var language: Locale = Locale.getDefault()
        var fallback: Locale = Locale.US
    }

    class Account {
        var accountId: String = ""
        var accountEmail: String = ""
        var accountUsername: String = ""
        var accountPassword: String = ""
        val id: Any
            get() {
                // TODO Auto-generated method stub
                throw UnsupportedOperationException("Unimplemented method 'getId'")
            }
    }

    /* Arguments related to client */
    class ARGS {
        var launchInDebugMode: Boolean = true
    }

    /* Server options. */
    class HTTP {
        /* This is the address used in URLs. */
        var accessAddress: String = "192.168.1.2"

        /* This is the port used in URLs. */
        var accessPort: Int = 8080

        var encryption: Encryption = Encryption()
        var policies: Policies = Policies()
    }

    class Game {
        /* This is the address used in the default region. */
        var accessAddress: String = "192.168.1.2"

        /* This is the port used in the default region. */
        var accessPort: Int = 23899

        /* Entities within a certain range will be loaded for the player */
        var loadEntitiesForPlayerRange: Int = 300

        /* Kcp internal work interval (milliseconds) */
        var kcpInterval: Int = 20

        /* Show packet payload in console or no (in any case the payload is shown in encrypted view) */
        var isShowPacketPayload: Boolean = true

        /* Server access tokens */
        var session_key: String = ""
        var account_token: String = ""

        var gameOptions: GameOptions = GameOptions()
    }

    class Encryption {
        var useEncryption: Boolean = true

        /* Should 'https' be appended to URLs? */
        var useInRouting: Boolean = true
        // Create Encryption variable from server
    }

    class Policies {
        var cors: CORS = CORS()

        class CORS {
            var enabled: Boolean = true
            var allowedOrigins: Array<String> = arrayOf("*")
        }
    }

    class GameOptions {
        var inventoryLimits: InventoryLimits = InventoryLimits()
        var sceneEntityLimit: Int = 1000 // Unenforced. TODO: Implement.

        class InventoryLimits {
            var weapons: Int = 2000
            var relics: Int = 2000
            var materials: Int = 2000
            var all: Int = 30000
        }
    }
}

