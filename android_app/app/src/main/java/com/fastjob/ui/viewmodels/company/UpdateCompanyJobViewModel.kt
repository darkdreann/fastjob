package com.fastjob.ui.viewmodels.company

import androidx.core.text.isDigitsOnly
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import androidx.navigation.NavController
import com.fastjob.auth.AuthAPI
import com.fastjob.models.AddressOUT
import com.fastjob.models.PartialUpdateJobOUT
import com.fastjob.network.Client
import com.fastjob.services.JobService
import com.fastjob.ui.enums.LoadState
import com.fastjob.ui.navigation.AppScreens
import com.fastjob.ui.viewmodels.candidate.CandidateExperienceViewModel
import com.fastjob.ui.viewmodels.interfaces.AddressForm
import com.fastjob.ui.viewmodels.interfaces.BasicJobData
import com.fastjob.ui.viewmodels.interfaces.BasicJobDataError
import com.fastjob.ui.viewmodels.interfaces.JobForm
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.util.UUID

/**
 * ViewModel para la pantalla de actualización de la oferta de trabajo
 * @param navController NavController controlador de navegación
 * @param jobId UUID identificador de la oferta de trabajo
 */
class UpdateCompanyJobViewModel(
    val navController: NavController,
    private val jobId: UUID
) : ViewModel(), JobForm, AddressForm {
    // static
    companion object {
        private val jobService = Client.getInstance().getService(JobService::class.java)
        val auth = AuthAPI.getInstance()
    }

    // estado de carga
    private val _loadState = MutableStateFlow(LoadState.LOADING)
    val loadState = _loadState.asStateFlow()

    // job data state
    private val _jobData = MutableStateFlow(BasicJobData())
    override val jobData: StateFlow<BasicJobData> = _jobData.asStateFlow()

    // job data error state
    private val _jobDataError = MutableStateFlow(BasicJobDataError())
    override val jobDataError: StateFlow<BasicJobDataError> = _jobDataError.asStateFlow()

    // job address state
    private val _address = MutableStateFlow(AddressOUT(
        postalCode = 0,
        province = "",
        city = "",
        street = ""
    ))
    override val address: StateFlow<AddressOUT> = _address.asStateFlow()

    private val _addressError = MutableStateFlow(false)
    val addressError: StateFlow<Boolean> = _addressError.asStateFlow()

    private val _jobDialogVisibility = MutableStateFlow(false)
    val jobDialogVisibility = _jobDialogVisibility.asStateFlow()

    /**
     * Establece el codigo postal de la dirección
     * @param postalCode String codigo postal
     */
    override fun setAddressPostalCode(postalCode: String) {
        if(postalCode.isEmpty() || !postalCode.isDigitsOnly()) return
        _address.value = _address.value.copy(postalCode = postalCode.toInt())
    }

    /**
     * Establece la provincia de la dirección
     * @param province String provincia
     */
    override fun setAddressProvince(province: String) {
        _address.value = _address.value.copy(province = province)
    }

    /**
     * Establece la ciudad de la dirección
     * @param city String ciudad
     */
    override fun setAddressCity(city: String) {
        _address.value = _address.value.copy(city = city)
    }

    /**
     * Establece la calle de la dirección
     * @param street String calle
     */
    override fun setAddressStreet(street: String) {
        _address.value = _address.value.copy(street = street)
    }


    /**
     * Establece los datos de la oferta
     * @param jobData BasicJobData datos de la oferta
     */
    override fun setJobData(jobData: BasicJobData) {
        _jobData.value = jobData
    }

    /**
     * Establece los errores de los datos de la oferta
     * @param jobDataError BasicJobDataError errores de los datos de la oferta
     */
    override fun setJobDataError(jobDataError: BasicJobDataError) {
        _jobDataError.value = jobDataError
    }

    /**
     * Establece el error de la dirección
     * @param error Boolean error de la dirección
     */
    fun setAddressError(error: Boolean){
        _addressError.value = error
    }

    /**
     * Establece la visibilidad del dialogo de la oferta
     * @param visibility Boolean visibilidad del dialogo
     */
    fun setJobDialogVisibility(visibility: Boolean) {
        _jobDialogVisibility.value = visibility
    }

    /**
     * Valida los datos de la oferta
     */
    private fun validateJob(){
        _jobDataError.value = _jobDataError.value.copy(
            title = jobData.value.title.isEmpty(),
            description = jobData.value.description.isEmpty(),
            requiredExperience = jobData.value.requiredExperience.isEmpty() || !jobData.value.requiredExperience.isDigitsOnly(),
            sectorId = jobData.value.sectorId == null,
        )
        _addressError.value = (address.value.postalCode < 10000 || address.value.postalCode > 99999)
            .or(address.value.city.isEmpty())
            .or(address.value.province.isEmpty())
            .or(address.value.street.isEmpty())
    }

    /**
     * Carga la oferta de trabajo
     */
    fun loadJob() {
        if(!auth.isAuthenticated()) {
            _loadState.value = LoadState.ERROR
            return
        }

        viewModelScope.launch(Dispatchers.IO){
            val response = jobService.getJob(
                auth = CandidateExperienceViewModel.auth.getToken()!!,
                id = jobId
            )

            if(response.isSuccessful) {
                response.body()?.let {
                    _jobData.value = _jobData.value.copy(
                        title = it.title,
                        description = it.description,
                        skills = it.skills,
                        workSchedule = it.workSchedule,
                        requiredExperience = it.requiredExperience.toString(),
                        sectorId = it.sector.id,
                        active = it.active,
                        sectorCategory = it.sector.category,
                        sectorSubcategory = it.sector.subcategory
                    )
                    _address.value = _address.value.copy(
                        postalCode = it.address.postalCode,
                        province = it.address.province,
                        city = it.address.city,
                        street = it.address.street
                    )

                    _loadState.value = LoadState.LOADED
                } ?: run {
                    _loadState.value = LoadState.ERROR
                }

            } else {
                _loadState.value = LoadState.ERROR
            }
        }
    }

    /**
     * Actualiza la oferta de trabajo
     */
    fun updateJob(){
        if(!auth.isAuthenticated()) return

        validateJob()

        if(jobDataError.value.hasError || addressError.value) {
            _jobDialogVisibility.value = true
            return
        }


        viewModelScope.launch(Dispatchers.IO) {
            val response = jobService.partialUpdateJob(
                auth = auth.getToken()!!,
                id = jobId,
                job = PartialUpdateJobOUT(
                    title = jobData.value.title,
                    description = jobData.value.description,
                    skills = jobData.value.skills,
                    workSchedule = jobData.value.workSchedule,
                    requiredExperience = jobData.value.requiredExperience.toInt(),
                    sector = jobData.value.sectorId!!,
                    address = address.value,
                    active = jobData.value.active,
                )
            )

            _jobDialogVisibility.value = !response.isSuccessful
            if(response.isSuccessful){
                withContext(Dispatchers.Main){ navController.navigate(AppScreens.CompanyJobsListScreen.route) }
            }
        }
    }
}

/**
 * Factoría del ViewModel de la pantalla de actualización de la oferta de trabajo
 * @param navController NavController controlador de navegación
 * @param jobId UUID identificador de la oferta de trabajo
 */
class UpdateCompanyJobViewModelFactory(
    private val navController: NavController,
    private val jobId: UUID
): ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return UpdateCompanyJobViewModel(navController, jobId) as T
    }
}




