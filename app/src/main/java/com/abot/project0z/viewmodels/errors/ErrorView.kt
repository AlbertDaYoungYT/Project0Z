package com.abot.project0z.viewmodels.errors

import com.abot.project0z.utils.Error

object ErrorView {
    fun showError(code: Int, name: String, message: String) {
        val Error = Error(code, name, message)
        GlobalErrorViewModel.showError(Error)
    }
    fun showError(Error: Error) {
        GlobalErrorViewModel.showError(Error)
    }
}
