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
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.screens.JobCardScreen
import com.fastjob.ui.screens.JobFinderScreen
import com.fastjob.ui.screens.UserCandidateRegisterScreen
import com.fastjob.ui.screens.UserLoginScreen

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
                it.arguments?.getString("jobId")?.let { jobId -> java.util.UUID.fromString(jobId) },
                navController
            )
        }
        composable(
            route = AppScreens.UserCandidateRegisterScreen.route,
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) }
        ){
            UserCandidateRegisterScreen(navController)
        }
        composable(
            route = AppScreens.UserLoginScreen.route,
            enterTransition = { fadeIn(tween(animationTime)) },
            exitTransition = { fadeOut(tween(animationTime)) },
            popEnterTransition = { fadeIn(tween(animationTime)) },
            popExitTransition = { fadeOut(tween(animationTime)) }
        ){
            UserLoginScreen(navController)
        }
    }
}