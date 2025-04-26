package com.abot.project0z.viewmodels.errors

import com.abot.project0z.utils.ErrorDetails

object ErrorView {
    fun showError(code: Int, name: String, message: String) {
        val errorDetails = ErrorDetails(code, name, message)
        GlobalErrorViewModel.showError(errorDetails)
    }
    fun showError(errorDetails: ErrorDetails) {
        GlobalErrorViewModel.showError(errorDetails)
    }
}
