package com.fastjob.ui.components.profile

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import com.fastjob.R
import com.fastjob.ui.components.basic.ErrorItem
import com.fastjob.ui.components.basic.LoadingItem
import com.fastjob.ui.enums.LoadState
import com.fastjob.ui.functions.capitalize
import com.fastjob.ui.functions.capitalizeWords
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.viewmodels.profile.CompanyProfileViewModel
import com.fastjob.ui.viewmodels.user.UpdateUserAddressViewModel
import com.fastjob.ui.viewmodels.user.UpdateUserViewModel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

/**
 * Pantalla de perfil de empresa
 * @param navController controlador de navegación
 * @param viewModel ViewModel de la pantalla
 */
@Composable
fun CompanyProfile(
    navController: NavController,
    viewModel: CompanyProfileViewModel
) {
    if(!CompanyProfileViewModel.auth.isAuthenticated()) navController.navigate(AppScreens.UserLoginScreen.route)

    // estado de carga de la empresa
    val companyLoadState by viewModel.companyLoadState.collectAsState()

    // información de la empresa
    val companyData by viewModel.company.collectAsState()


    LaunchedEffect(Unit){
        withContext(Dispatchers.IO){
            viewModel.loadCompany()
        }
    }

    when(companyLoadState){
        LoadState.LOADING -> {
            Box(
                modifier = Modifier
                    .fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                LoadingItem(stringResource(id = R.string.user_profile_loading))
            }
        }
        LoadState.ERROR -> {
            Box(
                modifier = Modifier
                    .fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                ErrorItem(stringResource(id = R.string.user_profile_error))
            }
        }
        LoadState.LOADED -> {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(
                        horizontal = 15.dp,
                        vertical = 10.dp
                    )
                    .verticalScroll(rememberScrollState()),
                verticalArrangement = Arrangement.spacedBy(7.dp)
            ) {

                companyData?.let {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .heightIn(0.dp, 160.dp)
                            .padding(
                                start = 6.dp,
                                bottom = 15.dp
                            ),
                        horizontalArrangement = Arrangement.Start
                    ) {

                        Image(
                            modifier = Modifier
                                .fillMaxSize()
                                .weight(0.3f),
                            painter = painterResource(id = R.drawable.user_img),
                            contentDescription = stringResource(id = R.string.user_image_desc),
                        )
                        Column(
                            modifier = Modifier
                                .fillMaxSize()
                                .weight(0.7f),
                            verticalArrangement = Arrangement.Center,
                            horizontalAlignment = Alignment.CenterHorizontally
                        ){
                            Row(
                                horizontalArrangement = Arrangement.spacedBy(3.dp)
                            ){
                                Text(
                                    text = it.user.name.capitalizeWords(),
                                    textAlign = TextAlign.Center,
                                    fontSize = 25.sp,
                                    fontStyle = FontStyle.Italic,
                                    lineHeight = 25.sp
                                )
                                Text(
                                    text = it.user.surname.capitalizeWords(),
                                    textAlign = TextAlign.Center,
                                    fontSize = 25.sp,
                                    fontStyle = FontStyle.Italic,
                                    lineHeight = 25.sp
                                )
                            }
                            Text(
                                text = it.companyName.capitalize(),
                                textAlign = TextAlign.Center,
                                fontSize = 25.sp,
                                fontStyle = FontStyle.Italic,
                                lineHeight = 25.sp
                            )
                        }

                    }
                    TextButton(
                        onClick = {
                            navController.navigate(AppScreens.UpdateUserDataScreen.route + "/${
                                UpdateUserViewModel.UserData(
                                    name = it.user.name,
                                    surname = it.user.surname,
                                    phoneNumbers = it.user.phoneNumbers,
                                )
                            }")
                        }
                    ) {
                        Text(
                            text = stringResource(id = R.string.user_profile_edit_user_info),
                            fontSize = 17.sp,
                        )
                    }
                    TextButton(
                        onClick = {
                            navController.navigate(AppScreens.UpdateUserPasswordScreen.route)
                        }
                    ) {
                        Text(
                            text = stringResource(id = R.string.user_profile_edit_user_password),
                            fontSize = 17.sp,
                        )
                    }
                    TextButton(
                        onClick = {
                            navController.navigate(AppScreens.UpdateUserAddressScreen.route + "/${
                                UpdateUserAddressViewModel.Address(
                                    street = it.user.address.street,
                                    city = it.user.address.city,
                                    province = it.user.address.province,
                                    postalCode = it.user.address.postalCode.toString(),
                                )
                            }")
                        }
                    ) {
                        Text(
                            text = stringResource(id = R.string.user_profile_edit_user_address),
                            fontSize = 17.sp,
                        )
                    }
                    TextButton(
                        onClick = {
                            navController.navigate(AppScreens.UpdateCompanyDataScreen.route + "/${it.tin}/${it.companyName}")
                        }
                    ) {
                        Text(
                            text = stringResource(id = R.string.company_profile_edit_data),
                            fontSize = 17.sp,
                        )
                    }
                } ?: Box(
                    modifier = Modifier
                        .fillMaxSize(),
                    contentAlignment = Alignment.Center
                ){
                    ErrorItem(stringResource(id = R.string.user_profile_error))
                }
            }
        }
        else -> {}
    }










}