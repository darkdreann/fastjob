package com.fastjob.ui.components.basic

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.height
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme.colorScheme
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.fastjob.R
import com.fastjob.auth.AuthAPI
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.theme.FastjobTheme

/**
 * Barra superior de la aplicación.
 * @param navController controlador de navegación
 * @param isLoginScreen indica si la barra superior se encuentra en la pantalla de login
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TopBar(
    navController: NavController,
    isLoginScreen: Boolean = false
){
    val auth = AuthAPI.getInstance()

    val (registerMenuVisibility, setRegisterMenuVisibility) = remember { mutableStateOf(false) }
    var menuOpen by remember { mutableStateOf(false) }

    TopAppBar(
        colors = TopAppBarDefaults.topAppBarColors(
            containerColor = colorScheme.primary,
            actionIconContentColor = colorScheme.tertiary
        ),
        modifier = Modifier
            .height(60.dp),
        title = {},
        navigationIcon = {},
        actions = {
            Column(
                modifier = Modifier
                    .fillMaxHeight(),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                IconButton(
                    modifier = Modifier
                        .fillMaxHeight(),
                    onClick = {
                        menuOpen = true
                    },
                ) {
                    Icon(
                        painter = if(!auth.isAuthenticated()) painterResource(id = R.drawable.user_login) else painterResource(id = R.drawable.user_logout),
                        contentDescription = stringResource(id = R.string.top_bar_icon_desc)
                    )
                }
                DropdownMenu(
                    expanded = menuOpen,
                    onDismissRequest = {
                        menuOpen = false
                    }
                ) {
                    if(!auth.isAuthenticated()) {
                        DropdownMenuItem(
                            text = {
                                Text(
                                    text = stringResource(id = R.string.top_bar_login),
                                )
                            },
                            onClick = {
                                navController.navigate(AppScreens.UserLoginScreen.route)
                            }
                        )
                        DropdownMenuItem(
                            text = {
                                Text(
                                    text = stringResource(id = R.string.top_bar_register),
                                )
                            },
                            onClick = {
                                setRegisterMenuVisibility(true)
                            }
                        )
                        RegisterDialog(
                            navController = navController,
                            visibilityState = Pair(registerMenuVisibility, setRegisterMenuVisibility)
                        )
                        if(isLoginScreen){
                            DropdownMenuItem(
                                text = {
                                    Text(
                                        text = stringResource(id = R.string.top_bar_offers),
                                    )
                                },
                                onClick = {
                                    navController.navigate(AppScreens.JobFinderScreen.route)
                                }
                            )
                        }
                    }else{
                        DropdownMenuItem(
                            text = {
                                Text(
                                    text = stringResource(id = R.string.top_bar_logout),
                                )
                            },
                            onClick = {
                                navController.navigate(AppScreens.UserLoginScreen.route){
                                    navController.graph.startDestinationRoute?.let {
                                        popUpTo(it) {
                                            inclusive = true
                                        }
                                    }
                                }.also {
                                    auth.logout()
                                }
                            }
                        )
                    }
                    DropdownMenuItem(
                        text = {
                            Text(
                                text = stringResource(id = R.string.acerca_de),
                            )
                        },
                        onClick = {
                            navController.navigate(AppScreens.AcercaDeScreen.route)
                        }
                    )
                }
            }

        }
    )
}

@Preview(showBackground = true)
@Composable
fun TopBarPreview(){
    FastjobTheme {
        TopBar(NavController(LocalContext.current))
    }
}