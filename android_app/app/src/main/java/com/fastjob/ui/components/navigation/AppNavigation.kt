package com.fastjob.ui.components.navigation

import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.runtime.Composable
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.fastjob.auth.AuthAPI
import com.fastjob.models.Availability
import com.fastjob.models.UserType
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.screens.AcercaDeScreen
import com.fastjob.ui.screens.CandidateCardEducationScreen
import com.fastjob.ui.screens.CandidateCardExperiencesScreen
import com.fastjob.ui.screens.CandidateCardLanguageScreen
import com.fastjob.ui.screens.CandidateCardScreen
import com.fastjob.ui.screens.CandidateCreateEducationScreen
import com.fastjob.ui.screens.CandidateCreateExperienceScreen
import com.fastjob.ui.screens.CandidateCreateLanguageScreen
import com.fastjob.ui.screens.CandidateEducationScreen
import com.fastjob.ui.screens.CandidateExperiencesScreen
import com.fastjob.ui.screens.CandidateJobAppliedScreen
import com.fastjob.ui.screens.CandidateLanguageScreen
import com.fastjob.ui.screens.CandidateProfileScreen
import com.fastjob.ui.screens.CandidateSkillsAvailabilitiesUpdateScreen
import com.fastjob.ui.screens.CompanyCreateJobLanguageScreen
import com.fastjob.ui.screens.CompanyCreateJobScreen
import com.fastjob.ui.screens.CompanyJobLanguageListScreen
import com.fastjob.ui.screens.CompanyJobsListScreen
import com.fastjob.ui.screens.CompanyProfileScreen
import com.fastjob.ui.screens.CompanyUpdateJobEducationScreen
import com.fastjob.ui.screens.CompanyUpdateJobLanguageScreen
import com.fastjob.ui.screens.CompanyUpdateJobScreen
import com.fastjob.ui.screens.JobCardScreen
import com.fastjob.ui.screens.JobFinderScreen
import com.fastjob.ui.screens.SearchCandidateListScreen
import com.fastjob.ui.screens.UpdateCompanyDataScreen
import com.fastjob.ui.screens.UpdateUserAddressScreen
import com.fastjob.ui.screens.UpdateUserDataScreen
import com.fastjob.ui.screens.UpdateUserPasswordScreen
import com.fastjob.ui.screens.UserCandidateRegisterScreen
import com.fastjob.ui.screens.UserCompanyRegisterScreen
import com.fastjob.ui.screens.UserLoginScreen
import com.fastjob.ui.viewmodels.user.UpdateUserAddressViewModel.Address
import com.fastjob.ui.viewmodels.user.UpdateUserViewModel.UserData
import java.util.UUID

/**
 * Navegacion de la aplicacion
 */
@Composable
fun AppNavigation() {
    // Tiempo de animaciones
    val animationTime = 400
    // Controlador de navegacion
    val navController = rememberNavController()

    // instancia de autenticacion
    val auth = AuthAPI.getInstance()
    val startDestination = if(auth.isAuthenticated() && auth.getUserType() == UserType.COMPANY) AppScreens.CompanyJobsListScreen.route else AppScreens.JobFinderScreen.route

    // Navegacion
    NavHost(navController = navController, startDestination = startDestination){
        // Pantalla de busqueda de ofertas de trabajo
        composable(
            route = AppScreens.JobFinderScreen.route,
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) }
        ){
            JobFinderScreen(navController)
        }
        // Pantalla de oferta de trabajo
        composable(
            route = AppScreens.JobCardScreen.route + "/{jobId}/{listIndex}",
            arguments = listOf(
                navArgument("jobId") { type = NavType.StringType },
                navArgument("listIndex") { type = NavType.IntType }),
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) }
        ){
            JobCardScreen(
                it.arguments?.getInt("listIndex") ?: 0,
                it.arguments?.getString("jobId")?.let { jobId -> UUID.fromString(jobId) },
                navController
            )
        }
        // Pantalla de registro de candidato
        composable(
            route = AppScreens.UserCandidateRegisterScreen.route,
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) }
        ){
            UserCandidateRegisterScreen(navController)
        }
        // Pantalla de login de usuario
        composable(
            route = AppScreens.UserLoginScreen.route,
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) }
        ){
            UserLoginScreen(navController)
        }
        // Pantalla de ofertas de trabajo aplicadas por el candidato
        composable(
            route = AppScreens.CandidateJobAppliedScreen.route,
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) }
        ){
            CandidateJobAppliedScreen(navController)
        }
        // Pantalla de perfil de candidato
        composable(
            route = AppScreens.CandidateProfileScreen.route,
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) }
        ){
            CandidateProfileScreen(navController)
        }
        // Pantalla de actualizacion de datos de usuario
        composable(
            route = AppScreens.UpdateUserDataScreen.route + "/{userData}",
            arguments = listOf(
                navArgument("userData") { type = NavType.StringType }),
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) }
        ){
            it.arguments?.getString("userData")?.let { userData ->
                UpdateUserDataScreen(
                    UserData.fromString(userData),
                    navController
                )
            }
        }
        // Pantalla de actualizacion de contrasena de usuario
        composable(
            route = AppScreens.UpdateUserPasswordScreen.route,
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) }
        ) {
            UpdateUserPasswordScreen(navController)
        }
        // Pantalla de actualizacion de direccion de usuario
        composable(
            route = AppScreens.UpdateUserAddressScreen.route + "/{userAddress}",
            arguments = listOf(
                navArgument("userAddress") { type = NavType.StringType }),
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) }
        ) {
            it.arguments?.getString("userAddress")?.let { userAddress ->
                UpdateUserAddressScreen(
                    navController,
                    Address.fromString(userAddress)
                )
            }
        }
        // Pantalla de actualizacion de habilidades y jornadas de candidato
        composable(
            route = AppScreens.UpdateCandidateSkillsAvailabilitiesScreen.route + "/{skills}/{availabilities}",
            arguments = listOf(
                navArgument("skills") { type = NavType.StringType },
                navArgument("availabilities") { type = NavType.StringType }),
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) }
        ) {
            it.arguments?.getString("skills")?.let { skills ->
                it.arguments?.getString("availabilities")?.let { availabilities ->
                    CandidateSkillsAvailabilitiesUpdateScreen(
                        navController,
                        skills.trim().split(","),
                        availabilities.trim().split(",").map { availability -> Availability.getByValue(availability) }
                    )
                }
            }
        }
        // Pantalla de experiencias de candidato
        composable(
            route = AppScreens.CandidateExperiencesScreen.route,
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) },
        ) {
            CandidateExperiencesScreen(navController)
        }
        // pantalla de creacion de experiencia de candidato
        composable(
            route = AppScreens.CandidateEditExperienceScreen.route,
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) },
        ) {
            CandidateCreateExperienceScreen(
                navController
            )
        }
        // pantalla de actualizacion de experiencia de candidato
        composable(
            route = AppScreens.CandidateEditExperienceScreen.route + "/{experience_id}",
            arguments = listOf(
                navArgument("experience_id") { type = NavType.StringType }),
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) },
        ) {
            it.arguments?.getString("experience_id")?.let { experienceId ->
                CandidateCreateExperienceScreen(
                    navController,
                    UUID.fromString(experienceId)
                )
            }
        }
        // pantalla de formaciones de candidato
        composable(
            route = AppScreens.CandidateEducationsScreen.route,
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) },
        ) {
            CandidateEducationScreen(navController)
        }
        // pantalla de creacion de formacion de candidato
        composable(
            route = AppScreens.CandidateEditEducationScreen.route,
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) },
        ) {
            CandidateCreateEducationScreen(
                navController
            )
        }
        // pantalla de actualizacion de formacion de candidato
        composable(
            route = AppScreens.CandidateEditEducationScreen.route + "/{education_id}",
            arguments = listOf(
                navArgument("education_id") { type = NavType.StringType }),
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) },
        ) {
            it.arguments?.getString("education_id")?.let { educationId ->
                CandidateCreateEducationScreen(
                    navController,
                    UUID.fromString(educationId)
                )
            }
        }
        // pantalla de idiomas de candidato
        composable(
            route = AppScreens.CandidateLanguagesScreen.route,
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) },
        ) {
            CandidateLanguageScreen(navController)
        }
        // pantalla de creacion de idioma de candidato
        composable(
            route = AppScreens.CandidateEditLanguageScreen.route,
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) },
        ) {
            CandidateCreateLanguageScreen(
                navController
            )
        }
        // pantalla de actualizacion de idioma de candidato
        composable(
            route = AppScreens.CandidateEditLanguageScreen.route + "/{language_id}",
            arguments = listOf(
                navArgument("language_id") { type = NavType.StringType }),
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) },
        ) {
            it.arguments?.getString("language_id")?.let { languageId ->
                CandidateCreateLanguageScreen(
                    navController,
                    UUID.fromString(languageId)
                )
            }
        }
        // Pantalla de registro de empresa
        composable(
            route = AppScreens.UserCompanyRegisterScreen.route,
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) }
        ){
            UserCompanyRegisterScreen(navController)
        }
        // Pantalla de lista de ofertas de trabajo de la empresa
        composable(
            route = AppScreens.CompanyJobsListScreen.route,
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) }
        ){
            CompanyJobsListScreen(navController)
        }
        // Pantalla de creacion de oferta de trabajo
        composable(
            route = AppScreens.CompanyCreateJobScreen.route,
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) }
        ){
            CompanyCreateJobScreen(navController)
        }
        // Pantalla de actualizacion de oferta de trabajo
        composable(
            route = AppScreens.CompanyUpdateJobScreen.route + "/{jobId}",
            arguments = listOf(
                navArgument("jobId") { type = NavType.StringType }),
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) }
        ){
            it.arguments?.getString("jobId")?.let { jobId ->
                CompanyUpdateJobScreen(
                    navController,
                    UUID.fromString(jobId)
                )
            }
        }
        // Pantalla de actualizacion de formacion de oferta de trabajo
        composable(
            route = AppScreens.CompanyUpdateJobEducationScreen.route + "/{jobId}",
            arguments = listOf(
                navArgument("jobId") { type = NavType.StringType }),
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) }
        ){
            it.arguments?.getString("jobId")?.let { jobId ->
                CompanyUpdateJobEducationScreen(
                    navController,
                    UUID.fromString(jobId)
                )
            }
        }
        // Pantalla lista de idiomas de oferta de trabajo
        composable(
            route = AppScreens.CompanyUpdateJobLanguageListScreen.route + "/{jobId}",
            arguments = listOf(
                navArgument("jobId") { type = NavType.StringType }),
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) }
        ){
            it.arguments?.getString("jobId")?.let { jobId ->
                CompanyJobLanguageListScreen(
                    navController,
                    UUID.fromString(jobId)
                )
            }
        }
        // Pantalla de anadir idioma a oferta de trabajo
        composable(
            route = AppScreens.CompanyUpdateJobLanguageScreen.route + "/{jobId}",
            arguments = listOf(
                navArgument("jobId") { type = NavType.StringType }),
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) }
        ){
            it.arguments?.getString("jobId")?.let { jobId ->
                CompanyCreateJobLanguageScreen(
                    navController,
                    UUID.fromString(jobId)
                )
            }
        }
        // Pantalla de actualizacion de idioma de oferta de trabajo
        composable(
            route = AppScreens.CompanyUpdateJobLanguageScreen.route + "/{jobId}/{languageId}",
            arguments = listOf(
                navArgument("jobId") { type = NavType.StringType },
                navArgument("languageId") { type = NavType.StringType }),
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) }
        ){
            it.arguments?.getString("jobId")?.let { jobId ->
                it.arguments?.getString("languageId")?.let { languageId ->
                    CompanyUpdateJobLanguageScreen(
                        navController,
                        UUID.fromString(jobId),
                        UUID.fromString(languageId)
                    )
                }
            }
        }
        // Pantalla de lista de candidatos de oferta de trabajo
        composable(
            route = AppScreens.CompanyJobCandidateListScreen.route + "/{jobId}",
            arguments = listOf(
                navArgument("jobId") { type = NavType.StringType }),
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) }
        ){
            it.arguments?.getString("jobId")?.let { jobId ->
                SearchCandidateListScreen(
                    navController,
                    UUID.fromString(jobId)
                )
            }
        }
        // Pantalla candidato en oferta de trabajo
        composable(
            route = AppScreens.CandidateCardScreen.route + "/{index}/{jobId}/{candidateId}",
            arguments = listOf(
                navArgument("index") { type = NavType.IntType },
                navArgument("jobId") { type = NavType.StringType },
                navArgument("candidateId") { type = NavType.StringType }),
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) }
        ){
            it.arguments?.getInt("index")?.let { index ->
                it.arguments?.getString("jobId")?.let { jobId ->
                    it.arguments?.getString("candidateId")?.let { candidateId ->
                        CandidateCardScreen(
                            index,
                            UUID.fromString(jobId),
                            UUID.fromString(candidateId),
                            navController
                        )
                    }
                }
            }
        }
        // Pantalla experiencia de candidato en oferta de trabajo
        composable(
            route = AppScreens.CandidateCardExperiencesScreen.route + "/{jobId}/{candidateId}",
            arguments = listOf(
                navArgument("jobId") { type = NavType.StringType },
                navArgument("candidateId") { type = NavType.StringType }),
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) }
        ){
            it.arguments?.getString("jobId")?.let { jobId ->
                it.arguments?.getString("candidateId")?.let { candidateId ->
                    CandidateCardExperiencesScreen(
                        navController,
                        UUID.fromString(jobId),
                        UUID.fromString(candidateId)
                    )
                }
            }
        }
        // Pantalla idiomas de candidato en oferta de trabajo
        composable(
            route = AppScreens.CandidateCardLanguageScreen.route + "/{jobId}/{candidateId}",
            arguments = listOf(
                navArgument("jobId") { type = NavType.StringType },
                navArgument("candidateId") { type = NavType.StringType }),
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) }
        ){
            it.arguments?.getString("jobId")?.let { jobId ->
                it.arguments?.getString("candidateId")?.let { candidateId ->
                    CandidateCardLanguageScreen(
                        navController,
                        UUID.fromString(jobId),
                        UUID.fromString(candidateId)
                    )
                }
            }
        }
        // Pantalla forma de candidato en oferta de trabajo
        composable(
            route = AppScreens.CandidateCardEducationScreen.route + "/{jobId}/{candidateId}",
            arguments = listOf(
                navArgument("jobId") { type = NavType.StringType },
                navArgument("candidateId") { type = NavType.StringType }),
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) }
        ){
            it.arguments?.getString("jobId")?.let { jobId ->
                it.arguments?.getString("candidateId")?.let { candidateId ->
                    CandidateCardEducationScreen(
                        navController,
                        UUID.fromString(jobId),
                        UUID.fromString(candidateId)
                    )
                }
            }
        }
        // Pantalla de perfil de empresa
        composable(
            route = AppScreens.CompanyProfileScreen.route,
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) }
        ){
            CompanyProfileScreen(navController)
        }
        // Pantalla de actualizar datos de empresa
        composable(
            route = AppScreens.UpdateCompanyDataScreen.route + "/{currentTin}/{currentCompanyName}",
            arguments = listOf(
                navArgument("currentTin") { type = NavType.StringType },
                navArgument("currentCompanyName") { type = NavType.StringType }),
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) }
        ){
            it.arguments?.getString("currentTin")?.let { currentTin ->
                it.arguments?.getString("currentCompanyName")?.let { currentCompanyName ->
                    UpdateCompanyDataScreen(
                        navController,
                        currentTin,
                        currentCompanyName
                    )
                }
            }
        }
        // Pantalla acerca de
        composable(
            route = AppScreens.AcercaDeScreen.route,
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) }
        ){
            AcercaDeScreen(navController)
        }
    }
}