package com.fastjob.ui.screens

import android.content.res.Configuration
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import androidx.navigation.compose.rememberNavController
import com.fastjob.ui.components.basic.TopBar
import com.fastjob.ui.components.form.CreateCandidateForm
import com.fastjob.ui.theme.FastjobTheme
import com.fastjob.ui.viewmodels.form.user.CreateCandidateViewModel

@Composable
fun UserCandidateRegisterScreen(
    navController: NavController
){
    // viewmodel de la pantalla de creación de usuario
    val viewModel = viewModel<CreateCandidateViewModel>()

    Scaffold(
        topBar = {
            TopBar(navController)
        },
    ){
        Box(
            modifier = Modifier
                .padding(it)
                .padding(vertical = 5.dp, horizontal = 10.dp)
        ){
            CreateCandidateForm(
                viewModel = viewModel,
                navController = navController
            )
        }
    }




}




@Preview(showBackground = true)
@Composable
fun UserCandidateRegisterScreenPreview() {
    FastjobTheme {
        UserCandidateRegisterScreen(rememberNavController())
    }
}

@Preview(showBackground = true, uiMode = Configuration.UI_MODE_NIGHT_YES)
@Composable
fun UserCandidateRegisterScreenPreviewDark() {
    FastjobTheme {
        UserCandidateRegisterScreen(rememberNavController())
    }
}
