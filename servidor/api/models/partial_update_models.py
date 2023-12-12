from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic.networks import EmailStr
from api.models.enums.models import WorkSchedule
from api.models.create_models import CreateAddress
from api.models.metadata import *
from api.models.functions.validate_functions import *


class PartialUpdateAddress(BaseModel):
    """Modelo para actualizar parcialmente una direccion 

        Atributos:
            postal_code: Codigo postal
            street: Calle de la direccion
            city: Ciudad de la direccion
            province: Provincia de la direccion"""
    
    postal_code: Optional[int] = Field(description=AddressDescription.POSTAL_CODE, ge=AddressValidators.MIN_POSTAL_CODE, le=AddressValidators.MAX_POSTAL_CODE, default=None)
    street: Optional[str] = Field(description=AddressDescription.STREET, max_length=AddressValidators.MAX_LENGHT_STREET, default=None)
    city: Optional[str] = Field(description=AddressDescription.CITY, max_length=AddressValidators.MAX_LENGHT_CITY, default=None)
    province: Optional[str] = Field(description=AddressDescription.PROVINCE, max_length=AddressValidators.MAX_LENGHT_PROVINCE, default=None)


class PartialUpdateUser(BaseModel):
    """Modelo para actualizar parcialmente un usuario

        Atributos:
            username: nombre identificador del usuario
            email: Correo electronico
            name: Nombre del usuario
            surname: Apellido del usuario
            phone_numbers: Lista de numeros de telefono
            password: Contraseña del usuario
            address: Direccion del usuario"""
    
    username: Optional[str] = Field(description=UserDescriptions.USERNAME, examples=UserExamples.USERNAME, max_length=UserValidators.MAX_LENGHT_USERNAME, min_length=UserValidators.MIN_LENGHT_USERNAME, default=None)
    email: Optional[EmailStr] = Field(description=UserDescriptions.EMAIL, default=None)
    name: Optional[str] = Field(description=UserDescriptions.NAME, max_length=UserValidators.MAX_LENGHT_NAME, default=None)
    surname: Optional[str] = Field(description=UserDescriptions.SURNAME, max_length=UserValidators.MAX_LENGHT_SURNAME, default=None)
    phone_numbers: Optional[list[int]] = Field(description=UserDescriptions.PHONE_NUMBER, max_length=UserValidators.MAX_ITEMS_PHONE_NUMBERS, default=None)
    password: Optional[str] = Field(description=UserDescriptions.PASSWORD, max_length=UserValidators.MAX_LENGHT_PASSWORD, default=None)
    address: Optional[CreateAddress] = Field(description=UserDescriptions.ADRESS, default=None, exclude=True)

    @field_validator('password')
    @classmethod
    def password_validate(cls, password):
        """Valida que la contraseña cumpla los requisitos de seguridad."""

        return validate_password(password)

    @field_validator('phone_numbers')
    @classmethod
    def phone_validate(cls, list):
        """Valida los numeros de telefono de una lista."""	

        return validate_phone_numbers(list)
    
    
class PartialUpdateCandidate(BaseModel):
    """Modelo para actualizar parcialmente un candidato

        Atributos:
            username: nombre identificador del usuario
            email: Correo electronico
            name: Nombre del usuario
            surname: Apellido del usuario
            phone_numbers: Lista de numeros de telefono
            password: Contraseña del usuario
            address: Direccion del usuario
            skills: Lista de habilidades del candidato
            availability: Lista de disponibilidad de jornada laboral del candidato"""
    
    skills: Optional[list[str]] = Field(description=CandidateDescription.SKILLS, max_length=CandidateValidators.MAX_ITEMS_SKILLS, default=None)
    availability: Optional[list[WorkSchedule]] = Field(description=CandidateDescription.AVAILABILITY, max_length=CandidateValidators.MAX_ITEMS_AVAILABILITY, default=None)
    user: Optional[PartialUpdateUser] = Field(description=CandidateDescription.USER, default=None)

    @field_validator('skills')
    @classmethod
    def validate(cls, list):
            return validate_skills_len(list)
    
class PartialUpdateCompany(BaseModel):
    """Modelo para actualizar parcialmente una empresa

        Atributos:
            username: nombre identificador del usuario
            email: Correo electronico
            name: Nombre del usuario
            surname: Apellido del usuario
            phone_numbers: Lista de numeros de telefono
            password: Contraseña del usuario
            address: Direccion del usuario
            tin: Numero de identificacion de la empresa
            company_name: Nombre de la empresa"""
    
    tin: Optional[str] = Field(description=CompanyDescription.TIN, pattern=CompanyValidators.REGEX_TIN, default=None)
    company_name: Optional[str] = Field(description=CompanyDescription.COMPANY_NAME, max_length=CompanyValidators.MAX_LENGHT_COMPANY_NAME, default=None)
    user: Optional[PartialUpdateUser] = Field(description=CandidateDescription.USER, default=None)

class PartialUpdateSector(BaseModel):
    """Modelo para actualizar parcialmente un sector

        Atributos:
            category: Categoria del sector
            subcategory: Subcategoria del sector"""
    
    category: Optional[str] = Field(description=SectorDescription.CATEGORY, max_length=SectorValidators.MAX_LENGHT_CATEGORY, default=None)
    subcategory: Optional[str] = Field(description=SectorDescription.SUBCATEGORY, max_length=SectorValidators.MAX_LENGHT_SUBCATEGORY, default=None)
    
class PartialUpdateExperience(BaseModel):
    """Modelo para actualizar parcialmente una experiencia

        Atributos:
            company_name: Nombre de la empresa
            position: Puesto de trabajo
            position_description: Descripcion del puesto de trabajo
            start_date: Fecha de inicio
            end_date: Fecha de finalizacion
            sector_id: Sector de la experiencia"""
    
    company_name: Optional[str] = Field(description=ExperienceDescription.COMPANY_NAME, max_length=ExperienceValidators.MAX_LENGHT_COMPANY_NAME, default=None)
    position: Optional[str] = Field(description=ExperienceDescription.POSITION, max_length=ExperienceValidators.MAX_LENGHT_POSITION, default=None)
    position_description: Optional[str] = Field(description=ExperienceDescription.POSITION_DESC, max_length=ExperienceValidators.MAX_LENGHT_POSITION_DESC, default=None)
    start_date: Optional[date] = Field(description=ExperienceDescription.START_DATE, default=None)
    end_date: Optional[date] = Field(description=ExperienceDescription.END_DATE, default=None)
    sector_id: Optional[UUID] = Field(description=ExperienceDescription.SECTOR_ID, default=None)

    @model_validator(mode='after')
    def end_date_validate(self):
        """Valida que las fechas"""

        validate_dates(self.start_date)
        if self.end_date is not None:
            validate_dates(self.end_date)
            validate_end_date(self.start_date, self.end_date)

        return self


class PartialUpdateEducation(BaseModel):
    """Modelo para actualizar parcialmente una formacion

        Atributos:
            qualification: Titulo de la formacion
            level_id: Nivel de la formacion
            sector_id: Sector de la formacion si lo tiene"""
    
    qualification: Optional[str] = Field(description=EducationDescription.QUALIFICATION, max_length=EducationValidators.MAX_LENGHT_QUALIFICATION, default=None)
    level_id: Optional[UUID] = Field(description=EducationDescription.LEVEL_ID, default=None)
    sector_id: Optional[UUID] = Field(description=EducationDescription.SECTOR_ID, default=None)
    

class PartialUpdateLevel(BaseModel):
    """
    Modelo para actualizar parcialmente un nivel de formacion o idioma

    Atributos:
        name: Nombre del nivel de formacion o idioma
        value: Valor numerico del nivel de formacion o idioma
    """
    
    name: Optional[str] = Field(description=LevelDescription.NAME, max_length=LevelValidators.MAX_LENGHT_NAME, default=None)
    value: Optional[int] = Field(description=LevelDescription.VALUE, ge=LevelValidators.MIN_VALUE, default=None)




class PartialUpdateJob(BaseModel):
    """
    Modelo para actualizar parcialmente una oferta

    Atributos:
        title: Titulo del puesto de trabajo (ejemplo: Desarrollador web)
        description: Descripcion del puesto de trabajo
        skills: Lista de habilidades requeridas para el trabajo
        work_schedule: Disponibilidad de jornada laboral requerida
        required_experience_months: Experiencia requerida en meses
        active: Estado de la oferta de trabajo (abierta o cerrada))
        address: Direccion de la oferta
        required_education_level_id: Nivel de formacion requerido
        sector_id: Sector de la oferta
        company_id: Empresa que publica la oferta
    """
    
    title: Optional[str] = Field(description=JobDescription.TITLE, max_length=JobValidators.MAX_LENGHT_TITLE, default=None)
    description: Optional[str] = Field(description=JobDescription.DESC, max_length=JobValidators.MAX_LENGHT_DESC, default=None)
    skills: Optional[list[str]] = Field(description=JobDescription.SKILLS, max_length=JobValidators.MAX_ITEMS_SKILLS, default=None)
    work_schedule: Optional[WorkSchedule] = Field(description=JobDescription.WORK_SHEDULE, default=None)
    required_experience: Optional[int] = Field(description=JobDescription.REQUIRED_EXP, ge=JobValidators.MIN_REQUIRED_EXP, default=None)
    active: Optional[bool] = Field(description=JobDescription.ACTIVE, default=None)
    address: Optional[PartialUpdateAddress] = Field(description=JobDescription.ADRESS, default=None)
    required_education: Optional[UUID] = Field(description=JobDescription.REQUIRED_EDUCATION_ID, default=None)
    sector_id: Optional[UUID] = Field(description=JobDescription.SECTOR_ID, default=None)
    company_id: Optional[UUID] = Field(description=JobDescription.COMPANY_ID, default=None)

    @field_validator('skills')
    @classmethod
    def validate(cls, list):
        return validate_skills_len(list)
