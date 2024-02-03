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
    object CandidateJobAppliedScreen: AppScreens("candidate_job_applied")
    object CandidateProfileScreen: AppScreens("candidate_profile")
    object UpdateUserDataScreen: AppScreens("update_user_data")
    object UpdateUserPasswordScreen: AppScreens("update_user_password")
    object UpdateUserAddressScreen: AppScreens("update_user_address")
    object UpdateCandidateSkillsAvailabilitiesScreen: AppScreens("update_candidate_skills_availabilities")
    object CandidateExperiencesScreen: AppScreens("candidate_experiences")
    object CandidateEditExperienceScreen: AppScreens("candidate_experience_edit")
    object CandidateEducationsScreen: AppScreens("candidate_educations")
    object CandidateEditEducationScreen: AppScreens("candidate_education_edit")
    object CandidateLanguagesScreen: AppScreens("candidate_languages")
    object CandidateEditLanguageScreen: AppScreens("candidate_language_edit")
}