package com.abot.project0z.config

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.emptyPreferences
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.map
import java.io.IOException


private const val ACCOUNT_PREFERENCES = "account_preferences"
private val Context.dataStore: DataStore<Preferences> by preferencesDataStore(
    name = ACCOUNT_PREFERENCES
)
class DataStoreContainer(context: Context) {
    private val dataStore = context.dataStore

    suspend fun saveAccountData(accountData: AccountData) {
        dataStore.edit { preferences ->
            preferences[USERNAME_KEY] = accountData.username
            preferences[TOKEN_KEY] = accountData.token
            preferences[IS_LOGGED_IN_KEY] = accountData.isLoggedIn
        }
    }

    val accountDataFlow: Flow<AccountData> = dataStore.data
        .catch { exception ->
            if (exception is IOException) {
                emit(emptyPreferences())
            } else {
                throw exception
            }
        }
        .map { preferences ->
            AccountData(
                username = preferences[USERNAME_KEY] ?: "",
                token = preferences[TOKEN_KEY] ?: "",
                isLoggedIn = preferences[IS_LOGGED_IN_KEY] ?: false
            )
        }

    suspend fun clearAccountData() {
        dataStore.edit { preferences ->
            preferences.clear()
        }
    }

    companion object {
        val USERNAME_KEY = stringPreferencesKey("username")
        val TOKEN_KEY = stringPreferencesKey("token")
        val IS_LOGGED_IN_KEY = booleanPreferencesKey("is_logged_in")
    }

    data class AccountData(
        val username: String = "",
        val token: String = "",
        val isLoggedIn: Boolean = false
    )
}