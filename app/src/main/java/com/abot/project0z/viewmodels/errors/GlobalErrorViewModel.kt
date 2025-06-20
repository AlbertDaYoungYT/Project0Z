package com.abot.project0z.viewmodels.errors

import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.abot.project0z.utils.Error
import com.abot.project0z.utils.ErrorDialog
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

data class GlobalErrorState(
    val isVisible: Boolean = false,
    val Error: Error? = null
)

// Singleton ViewModel (for simplicity, but less testable)
object GlobalErrorViewModel : ViewModel() {
    private val _errorState = MutableStateFlow(GlobalErrorState())
    val errorState: StateFlow<GlobalErrorState> = _errorState

    fun showError(Error: Error) {
        viewModelScope.launch {
            _errorState.value = GlobalErrorState(isVisible = true, Error = Error)
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

    if (errorState.isVisible && errorState.Error != null) {
        errorState.Error!!.ShowErrorDialog(
            onDismissRequest = { GlobalErrorViewModel.hideError() }
        )
    }
}
@Composable
fun Error.ShowErrorDialog(onDismissRequest: () -> Unit) {
    val showDialog = remember { mutableStateOf(true) } // Dialog is already visible
    ErrorDialog(
        showDialog = showDialog,
        title = "Error (Code $code) $name",
        message = message,
        onDismissRequest = onDismissRequest
    )
}