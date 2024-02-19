package com.fastjob.ui.components.basic

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.material3.BottomAppBar
import androidx.compose.material3.Divider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme.colorScheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import com.fastjob.R
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.theme.FastjobTheme

/**
 * Barra de navegación inferior para el tipo de usuario company
 * @param navController controlador de navegación
 */
@Composable
fun CompanyBottomBar(
    navController: NavController
){
    BottomAppBar(
        modifier = Modifier
            .height(90.dp)
            .fillMaxWidth(),
        containerColor = colorScheme.primary,
        contentColor = colorScheme.tertiary
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween
        ){
            IconButton(
                modifier = Modifier
                    .fillMaxSize()
                    .weight(0.33f),
                onClick = { navController.navigate(AppScreens.CompanyJobsListScreen.route) }
            ) {
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Icon(
                        modifier = Modifier.size(20.dp),
                        painter = painterResource(id = R.drawable.list),
                        contentDescription = stringResource(id = R.string.bottom_bar_job_created)
                    )
                    Text(
                        text = stringResource(id = R.string.bottom_bar_job_created),
                        fontSize = 10.sp
                    )
                }
            }
            Divider(
                modifier = Modifier
                    .fillMaxHeight()
                    .width(1.dp),
                color = Color.Gray
            )
            IconButton(
                modifier = Modifier
                    .fillMaxSize()
                    .weight(0.33f),
                onClick = {
                    navController.navigate(AppScreens.CompanyCreateJobScreen.route)
                }
            ) {
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Icon(
                        modifier = Modifier.size(20.dp),
                        painter = painterResource(id = R.drawable.add_list),
                        contentDescription = stringResource(id = R.string.bottom_bar_job_create)
                    )
                    Text(
                        text = stringResource(id = R.string.bottom_bar_job_create),
                        fontSize = 10.sp
                    )
                }
            }
            Divider(
                modifier = Modifier
                    .fillMaxHeight()
                    .width(1.dp),
                color = Color.Gray
            )
            IconButton(
                modifier = Modifier
                    .fillMaxSize()
                    .weight(0.33f),
                onClick = {
                    navController.navigate(AppScreens.CompanyProfileScreen.route)
                }
            ) {
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Icon(
                        modifier = Modifier.size(20.dp),
                        painter = painterResource(id = R.drawable.profile),
                        contentDescription = stringResource(id = R.string.bottom_bar_profile)
                    )
                    Text(
                        text = stringResource(id = R.string.bottom_bar_profile),
                        fontSize = 10.sp
                    )
                }
            }
        }
    }
}


@Preview(showBackground = true)
@Composable
fun CompanyBottomBarPreview(){
    FastjobTheme {
        CompanyBottomBar(NavController(LocalContext.current))
    }
}