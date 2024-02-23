package com.fastjob.ui.components.form

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.MaterialTheme.colorScheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import com.fastjob.R
import com.fastjob.models.UserType
import com.fastjob.ui.components.basic.BasicDialog
import com.fastjob.ui.components.basic.PasswordField
import com.fastjob.ui.enums.LoginState
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.viewmodels.login.LoginViewModel

/**
 * Pantalla de login de usuario
 * @param viewModel ViewModel de la pantalla
 * @param navController controlador de navegación

 */
@Composable
fun LoginUser(
    viewModel: LoginViewModel,
    navController: NavController
) {
    // estado del login
    val loginState by viewModel.loginState.collectAsState()

    // estado del username
    val username by viewModel.username.collectAsState()
    // estado del password
    val password by viewModel.password.collectAsState()

    // estado de error del username
    val usernameError by viewModel.usernameError.collectAsState()
    // estado de error del password
    val passwordError by viewModel.passwordError.collectAsState()

    // estado visibilidad error
    val errorVisibility by viewModel.errorVisibility.collectAsState()

    // si el login es exitoso, navegar a la pantalla de búsqueda de empleo
    when(loginState) {
        LoginState.SUCCESS -> {
            when(LoginViewModel.auth.getUserType()){
                UserType.CANDIDATE -> navController.navigate(AppScreens.JobFinderScreen.route)
                UserType.COMPANY -> navController.navigate(AppScreens.CompanyJobsListScreen.route)
                else -> {
                    LoginViewModel.auth.logout()
                    BasicDialog(
                        title = stringResource(id = R.string.login_user_error_title),
                        content = stringResource(id = R.string.login_user_error_admin),
                        icon = painterResource(id = R.drawable.error),
                        visibilityState = Pair(errorVisibility, viewModel::setErrorVisibility)
                    )
                }
            }

        }
        // si el login falla, mostrar un dialogo de error
        LoginState.ERROR -> {
            BasicDialog(
                title = stringResource(id = R.string.login_user_error_title),
                content = stringResource(id = R.string.login_user_error_msg),
                icon = painterResource(id = R.drawable.error),
                visibilityState = Pair(errorVisibility, viewModel::setErrorVisibility)
            )
        }
        else -> {}
    }

    // contenido
    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(horizontal = 20.dp, vertical = 10.dp)
            .imePadding(),
        verticalArrangement = Arrangement.spacedBy(10.dp),
    ) {

        // imagen de usuario
        Image(
            modifier = Modifier
                .fillMaxWidth()
                .height(300.dp),
            painter = painterResource(id = R.drawable.user_img),
            contentDescription = stringResource(id = R.string.user_image_desc),
        )
        // titulo
        Text(
            modifier = Modifier.fillMaxWidth(),
            text = stringResource(id = R.string.login_user_title),
            fontSize = 30.sp,
            textAlign = TextAlign.Center,
        )
        // username
        TextField(
            singleLine = true,
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(15.dp)),
            label = { Text(stringResource(id = R.string.register_user_username)) },
            value = username,
            onValueChange = {
                if(it.length <= 16){
                    viewModel.setUsername(it)
                    viewModel.setUsernameError(false)
                }
            },
            isError = usernameError,
        )
        // password
        PasswordField(
            maxLength = 30,
            passwordState = Pair(password, viewModel::setPassword),
            errorState = Pair(passwordError, viewModel::setPasswordError)
        )
        // boton de login
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .padding(top = 20.dp),
            contentAlignment = Alignment.BottomEnd
        ){
            Button(
                onClick = {
                    viewModel.login()
                },
                colors = ButtonDefaults.buttonColors(
                    containerColor = colorScheme.tertiary,
                    contentColor = colorScheme.primary
                ),
                ) {
                Text(text = stringResource(id = R.string.login_user_button))
            }
        }
    }
}