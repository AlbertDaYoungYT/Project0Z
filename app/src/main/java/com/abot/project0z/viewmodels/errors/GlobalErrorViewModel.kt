package com.abot.project0z.viewmodels.errors

import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.abot.project0z.utils.ErrorDetails
import com.abot.project0z.utils.ErrorDialog
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

data class GlobalErrorState(
    val isVisible: Boolean = false,
    val errorDetails: ErrorDetails? = null
)

// Singleton ViewModel (for simplicity, but less testable)
object GlobalErrorViewModel : ViewModel() {
    private val _errorState = MutableStateFlow(GlobalErrorState())
    val errorState: StateFlow<GlobalErrorState> = _errorState

    fun showError(errorDetails: ErrorDetails) {
        viewModelScope.launch {
            _errorState.value = GlobalErrorState(isVisible = true, errorDetails = errorDetails)
        }
    }

    fun hideError() {
        viewModelScope.launch {
            _errorState.value = GlobalErrorState(isVisible = false)
        }
    }
}


@Composable
fun GlobalErrorView() {
    val errorState by GlobalErrorViewModel.errorState.collectAsState()

    if (errorState.isVisible && errorState.errorDetails != null) {
        errorState.errorDetails!!.ShowErrorDialog(
            onDismissRequest = { GlobalErrorViewModel.hideError() }
        )
    }
}
@Composable
fun ErrorDetails.ShowErrorDialog(onDismissRequest: () -> Unit) {
    val showDialog = remember { mutableStateOf(true) } // Dialog is already visible
    ErrorDialog(
        showDialog = showDialog,
        title = "Error (Code $code) $name",
        message = message,
        onDismissRequest = onDismissRequest
    )
}