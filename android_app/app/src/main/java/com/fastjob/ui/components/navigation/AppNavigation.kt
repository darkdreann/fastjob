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
import com.fastjob.models.Availability
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.screens.CandidateCreateEducationScreen
import com.fastjob.ui.screens.CandidateCreateExperienceScreen
import com.fastjob.ui.screens.CandidateCreateLanguageScreen
import com.fastjob.ui.screens.CandidateEducationScreen
import com.fastjob.ui.screens.CandidateExperiencesScreen
import com.fastjob.ui.screens.CandidateJobAppliedScreen
import com.fastjob.ui.screens.CandidateLanguageScreen
import com.fastjob.ui.screens.CandidateProfileScreen
import com.fastjob.ui.screens.CandidateSkillsAvailabilitiesUpdateScreen
import com.fastjob.ui.screens.JobCardScreen
import com.fastjob.ui.screens.JobFinderScreen
import com.fastjob.ui.screens.UpdateUserAddressScreen
import com.fastjob.ui.screens.UpdateUserDataScreen
import com.fastjob.ui.screens.UpdateUserPasswordScreen
import com.fastjob.ui.screens.UserCandidateRegisterScreen
import com.fastjob.ui.screens.UserLoginScreen
import com.fastjob.ui.viewmodels.form.user.UpdateUserAddressViewModel.Address
import com.fastjob.ui.viewmodels.form.user.UpdateUserViewModel.UserData
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

    // Navegacion
    NavHost(navController = navController, startDestination = AppScreens.JobFinderScreen.route){
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
    }
}