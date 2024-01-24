package com.fastjob.ui.navigation

/**
 * Clase que contiene las rutas de las pantallas de la aplicación
 */
sealed class AppScreens(val route: String) {
    object JobFinderScreen: AppScreens("job_finder")
    object JobCardScreen: AppScreens("job_card")
    object UserLoginScreen: AppScreens("login")
    object UserCandidateRegisterScreen: AppScreens("register_candidate")
    object UserCompanyRegisterScreen: AppScreens("register_company")
}