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
    object CompanyJobsListScreen: AppScreens("company_jobs_list")
    object CompanyCreateJobScreen: AppScreens("company_create_job")
    object CompanyUpdateJobScreen: AppScreens("company_update_job")
    object CompanyUpdateJobEducationScreen: AppScreens("company_update_job_education")
    object CompanyUpdateJobLanguageListScreen: AppScreens("company_update_job_language_list")
    object CompanyUpdateJobLanguageScreen: AppScreens("company_update_job_language")
    object CompanyJobCandidateListScreen: AppScreens("company_job_candidate_list")
    object CandidateCardScreen: AppScreens("candidate_card")
    object CandidateCardEducationScreen: AppScreens("candidate_card_education")
    object CandidateCardExperiencesScreen: AppScreens("candidate_card_experiences")
    object CandidateCardLanguageScreen: AppScreens("candidate_card_language")
    object CompanyProfileScreen: AppScreens("company_profile")
    object UpdateCompanyDataScreen: AppScreens("update_company_data")
}