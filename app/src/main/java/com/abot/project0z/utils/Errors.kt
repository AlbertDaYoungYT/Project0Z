package com.abot.project0z.utils

import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.MutableState
import androidx.compose.ui.window.DialogProperties
import com.abot.project0z.viewmodels.errors.ErrorView
import com.google.gson.Gson


@Composable
fun ErrorDialog(
    showDialog: MutableState<Boolean>,
    title: String,
    message: String,
    onDismissRequest: () -> Unit = { showDialog.value = false },
    onConfirmation: () -> Unit = { showDialog.value = false } // Optional action
) {
    if (showDialog.value) {
        AlertDialog(
            onDismissRequest = onDismissRequest,
            title = { Text(title) },
            text = { Text(message) },
            confirmButton = {
                Button(onClick = onConfirmation) {
                    Text("OK") // Or "Retry", etc.
                }
            },
            // dismissButton = {  // Optional dismiss button
            //     Button(onClick = onDismissRequest) {
            //         Text("Cancel")
            //     }
            // },
            properties = DialogProperties(
                dismissOnBackPress = true,
                dismissOnClickOutside = true,
            )
        )
    }
}


data class Error(
    val code: Int,
    val name: String,
    var message: String
) {  // Assuming you have a Serializable interface as in Python
    fun toLogger(e: Exception? = null): String {
        if (e != null) {
            message = e.message ?: message
        }
        this.show()
        return "Error (Code $code) $name '$message'"
    }

    fun toJson(): String {
        return Gson().toJson(this)
    }

    fun show() {
        ErrorView.showError(this)
    }
}

enum class Codes(val details: Error) {
    SUCCESS(Error(code = 0, name = "SUCCESS", message = "Operation successful")),

    // Authentication Errors (1xx)
    INVALID_CREDENTIALS(
        Error(
            code = 100,
            name = "INVALID_CREDENTIALS",
            message = "Incorrect username or password."
        )
    ),
    ACCOUNT_LOCKED(
        Error(
            code = 101,
            name = "ACCOUNT_LOCKED",
            message = "This account has been temporarily locked."
        )
    ),
    ACCOUNT_BANNED(
        Error(
            code = 102,
            name = "ACCOUNT_BANNED",
            message = "This account has been banned."
        )
    ),
    UNAUTHORIZED_ACCESS(
        Error(
            code = 103,
            name = "UNAUTHORIZED_ACCESS",
            message = "You do not have permission to access this resource."
        )
    ),
    TOKEN_EXPIRED(
        Error(
            code = 104,
            name = "TOKEN_EXPIRED",
            message = "The authentication token has expired."
        )
    ),
    INVALID_TOKEN(
        Error(
            code = 105,
            name = "INVALID_TOKEN",
            message = "The provided authentication token is invalid."
        )
    ),
    SESSION_EXPIRED(
        Error(
            code = 106,
            name = "SESSION_EXPIRED",
            message = "Your session has expired. Please log in again."
        )
    ),
    TOO_MANY_ATTEMPTS(
        Error(
            code = 107,
            name = "TOO_MANY_ATTEMPTS",
            message = "Too many login attempts. Please wait and try again later."
        )
    ),
    MFA_REQUIRED(
        Error(
            code = 108,
            name = "MFA_REQUIRED",
            message = "Multi-factor authentication is required."
        )
    ),
    MFA_FAILED(
        Error(
            code = 109,
            name = "MFA_FAILED",
            message = "Multi-factor authentication failed."
        )
    ),

    // User/Account Related Errors (2xx)
    USER_NOT_FOUND(
        Error(
            code = 200,
            name = "USER_NOT_FOUND",
            message = "User with the given identifier not found."
        )
    ),
    USERNAME_TAKEN(
        Error(
            code = 201,
            name = "USERNAME_TAKEN",
            message = "The specified username is already in use."
        )
    ),
    EMAIL_TAKEN(
        Error(
            code = 202,
            name = "EMAIL_TAKEN",
            message = "The specified email address is already registered."
        )
    ),
    INVALID_EMAIL_FORMAT(
        Error(
            code = 203,
            name = "INVALID_EMAIL_FORMAT",
            message = "The provided email address is not in a valid format."
        )
    ),
    PASSWORD_MISMATCH(
        Error(
            code = 204,
            name = "PASSWORD_MISMATCH",
            message = "The provided passwords do not match."
        )
    ),
    ACCOUNT_NOT_VERIFIED(
        Error(
            code = 205,
            name = "ACCOUNT_NOT_VERIFIED",
            message = "This account has not been verified."
        )
    ),
    WEAK_PASSWORD(
        Error(
            code = 206,
            name = "WEAK_PASSWORD",
            message = "The provided password is too weak."
        )
    ),
    PROFILE_INCOMPLETE(
        Error(
            code = 207,
            name = "PROFILE_INCOMPLETE",
            message = "User profile is incomplete."
        )
    ),
    AGE_RESTRICTION(
        Error(
            code = 208,
            name = "AGE_RESTRICTION",
            message = "User does not meet the minimum age requirement."
        )
    ),

    ACCOUNT_CHECK_FAILED(
        Error(
            code = 210,
            name = "ACCOUNT_CHECK_FAILED",
            message = "Account failed to pass checks."
        )
    ),

    // Game Logic Errors (3xx)
    INVALID_GAME_STATE(
        Error(
            code = 300,
            name = "INVALID_GAME_STATE",
            message = "The game is in an invalid state for this action."
        )
    ),
    INVALID_MOVE(
        Error(
            code = 301,
            name = "INVALID_MOVE",
            message = "The attempted move is not valid."
        )
    ),
    INSUFFICIENT_RESOURCES(
        Error(
            code = 302,
            name = "INSUFFICIENT_RESOURCES",
            message = "Not enough resources to perform this action."
        )
    ),
    ITEM_NOT_FOUND(
        Error(
            code = 303,
            name = "ITEM_NOT_FOUND",
            message = "The requested item could not be found."
        )
    ),
    ACTION_NOT_ALLOWED(
        Error(
            code = 304,
            name = "ACTION_NOT_ALLOWED",
            message = "You are not allowed to perform this action at this time."
        )
    ),
    LEVEL_REQUIREMENT_NOT_MET(
        Error(
            code = 305,
            name = "LEVEL_REQUIREMENT_NOT_MET",
            message = "You have not reached the required level."
        )
    ),
    MATCH_NOT_FOUND(
        Error(
            code = 306,
            name = "MATCH_NOT_FOUND",
            message = "The specified match could not be found."
        )
    ),
    ALREADY_IN_PARTY(
        Error(
            code = 307,
            name = "ALREADY_IN_PARTY",
            message = "You are already in a party."
        )
    ),

    // Database Errors (4xx)
    DATABASE_CONNECTION_ERROR(
        Error(
            code = 400,
            name = "DATABASE_CONNECTION_ERROR",
            message = "Failed to connect to the database."
        )
    ),
    DATABASE_QUERY_ERROR(
        Error(
            code = 401,
            name = "DATABASE_QUERY_ERROR",
            message = "An error occurred while executing the database query."
        )
    ),
    DATABASE_RECORD_EXISTS(
        Error(
            code = 402,
            name = "DATABASE_RECORD_EXISTS",
            message = "The record already exists in the database."
        )
    ),
    DATABASE_RECORD_NOT_FOUND(
        Error(
            code = 403,
            name = "DATABASE_RECORD_NOT_FOUND",
            message = "The requested record was not found in the database."
        )
    ),
    DATABASE_TIMEOUT(
        Error(
            code = 404,
            name = "DATABASE_TIMEOUT",
            message = "The database request timed out."
        )
    ),
    TRANSACTION_FAILED(
        Error(
            code = 405,
            name = "TRANSACTION_FAILED",
            message = "The database transaction failed."
        )
    ),
    DUPLICATE_ENTRY(
        Error(
            code = 406,
            name = "DUPLICATE_ENTRY",
            message = "A duplicate entry was found."
        )
    ),
    SCHEMA_MISMATCH(
        Error(
            code = 407,
            name = "SCHEMA_MISMATCH",
            message = "Database schema does not match expected structure."
        )
    ),

    // Input/Validation Errors (5xx)
    MISSING_REQUIRED_FIELD(
        Error(
            code = 500,
            name = "MISSING_REQUIRED_FIELD",
            message = "A required field is missing in the input."
        )
    ),
    INVALID_FIELD_VALUE(
        Error(
            code = 501,
            name = "INVALID_FIELD_VALUE",
            message = "The value provided for a field is invalid."
        )
    ),
    REQUEST_BODY_MALFORMED(
        Error(
            code = 502,
            name = "REQUEST_BODY_MALFORMED",
            message = "The request body is not in the expected format."
        )
    ),
    INVALID_ENUM_VALUE(
        Error(
            code = 503,
            name = "INVALID_ENUM_VALUE",
            message = "An invalid value was provided for an enumerated field."
        )
    ),
    VALUE_OUT_OF_RANGE(
        Error(
            code = 504,
            name = "VALUE_OUT_OF_RANGE",
            message = "A numeric value is outside the allowable range."
        )
    ),
    INVALID_DATE_FORMAT(
        Error(
            code = 505,
            name = "INVALID_DATE_FORMAT",
            message = "The date format is invalid. Expected ISO 8601."
        )
    ),
    UNSUPPORTED_MEDIA_TYPE(
        Error(
            code = 506,
            name = "UNSUPPORTED_MEDIA_TYPE",
            message = "The content type of the request is not supported."
        )
    ),

    // Internal Server Errors (9xx) - Typically unexpected issues
    INTERNAL_SERVER_ERROR(
        Error(
            code = 900,
            name = "INTERNAL_SERVER_ERROR",
            message = "An unexpected internal server error occurred."
        )
    ),
    UNHANDLED_EXCEPTION(
        Error(
            code = 901,
            name = "UNHANDLED_EXCEPTION",
            message = "An unhandled exception was raised."
        )
    ),
    CONFIGURATION_ERROR(
        Error(
            code = 902,
            name = "CONFIGURATION_ERROR",
            message = "There is an issue with the server configuration."
        )
    ),
    SERVICE_UNAVAILABLE(
        Error(
            code = 903,
            name = "SERVICE_UNAVAILABLE",
            message = "The service is currently unavailable."
        )
    ),
    DEPENDENCY_FAILURE(
        Error(
            code = 904,
            name = "DEPENDENCY_FAILURE",
            message = "A required external service failed to respond."
        )
    ),
    MEMORY_OVERLOAD(
        Error(
            code = 905,
            name = "MEMORY_OVERLOAD",
            message = "The server ran out of memory processing the request."
        )
    ),
    RATE_LIMIT_EXCEEDED(
        Error(
            code = 906,
            name = "RATE_LIMIT_EXCEEDED",
            message = "Rate limit exceeded. Slow down your requests."
        )
    ),

    // Client side errors 10xx
    ACCOUNT_PARSING_FAILED(
        Error(
            code = 1001,
            name = "ACCOUNT_PARSING_FAILED",
            message = "Failed to parse token from server"
        )
    ),
    SETTINGS_NOT_INITIALIZED(
        Error(
            code = 1002,
            name = "SETTINGS_NOT_INITIALIZED",
            message = "Settings have not been initialized"
        )
    ),

}