from typing import Optional
from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic.networks import EmailStr
from api.models.enums.models import WorkSchedule
from api.models.metadata import *
from api.models.functions.validate_functions import *


class BaseUser(BaseModel):
    """Modelo base para los usuarios
    
        Atributos:
            username: nombre identificador del usuario
            email: Correo electronico
            name: Nombre del usuario
            surname: Apellido del usuario
            phone_numbers: Lista de numeros de telefono"""

    username: str = Field(description=UserDescriptions.USERNAME, examples=UserExamples.USERNAME, max_length=UserValidators.MAX_LENGHT_USERNAME, min_length=UserValidators.MIN_LENGHT_USERNAME)
    email: EmailStr = Field(description=UserDescriptions.EMAIL)
    name: str = Field(description=UserDescriptions.NAME, max_length=UserValidators.MAX_LENGHT_NAME)
    surname: str = Field(description=UserDescriptions.SURNAME, max_length=UserValidators.MAX_LENGHT_SURNAME)
    phone_numbers: list[int] = Field(description=UserDescriptions.PHONE_NUMBER, max_length=UserValidators.MAX_ITEMS_PHONE_NUMBERS)

    @field_validator('phone_numbers')
    @classmethod
    def phone_validate(cls, list):
        return validate_phone_numbers(list)
    

class BaseCandidate(BaseModel):
    """Modelo base para los candidatos
    
        Atributos:
            skills: Lista de habilidades del candidato
            availability: Lista de disponibilidad de jornada laboral del candidato"""

    skills: list[str] = Field(description=CandidateDescription.SKILLS, max_length=CandidateValidators.MAX_ITEMS_SKILLS)
    availability: list[WorkSchedule] = Field(description=CandidateDescription.AVAILABILITY, max_length=CandidateValidators.MAX_ITEMS_AVAILABILITY)

    @field_validator('skills')
    @classmethod
    def validate(cls, list):
            return validate_skills_len(list)
    
class BaseCompany(BaseModel):
    """Modelo base para las empresas
    
        Atributos:
            tin: Numero de identificacion de la empresa
            company_name: Nombre de la empresa"""
     
    tin: str = Field(description=CompanyDescription.TIN, pattern=CompanyValidators.REGEX_TIN)
    company_name: str = Field(description=CompanyDescription.COMPANY_NAME, max_length=CompanyValidators.MAX_LENGHT_COMPANY_NAME)


class BaseLanguage(BaseModel):
    """Modelo base para los idiomas
    
        Atributos:
            name: Nombre del idioma"""
     
    name: str = Field(description=LanguageDescription.NAME, max_length=LanguageValidators.MAX_LENGHT_NAME)

class BaseSector(BaseModel):
    """Modelo base para los sectores
    
        Atributos:
            category: Categoria del sector
            subcategory: Subcategoria del sector"""
     
    category: str = Field(description=SectorDescription.CATEGORY, max_length=SectorValidators.MAX_LENGHT_CATEGORY)
    subcategory: str = Field(description=SectorDescription.SUBCATEGORY, max_length=SectorValidators.MAX_LENGHT_SUBCATEGORY)

class BaseExperience(BaseModel):
    """Modelo base para las experiencias laborales
    
        Atributos:
            company_name: Nombre de la empresa
            position: Posicion en la empresa
            position_description: Descripcion del puesto
            start_date: Fecha de inicio
            end_date: Fecha de finalizacion"""
     
    company_name: str = Field(description=ExperienceDescription.COMPANY_NAME, max_length=ExperienceValidators.MAX_LENGHT_COMPANY_NAME)
    job_position: str = Field(description=ExperienceDescription.POSITION, max_length=ExperienceValidators.MAX_LENGHT_POSITION)
    job_position_description: str = Field(description=ExperienceDescription.POSITION_DESC, max_length=ExperienceValidators.MAX_LENGHT_POSITION_DESC)
    start_date: date = Field(description=ExperienceDescription.START_DATE)
    end_date: Optional[date] = Field(description=ExperienceDescription.END_DATE, default=None)

    @model_validator(mode='after')
    def end_date_validate(self):
        """Valida que las fechas"""

        validate_dates(self.start_date)
        if self.end_date is not None:
            validate_dates(self.end_date)
            validate_end_date(self.start_date, self.end_date)

        return self
        


class BaseEducation(BaseModel):
    """Modelo base para la formacion academica
    
        Atributos:
            qualification: Titulacion obtenida"""

    qualification: str = Field(description=EducationDescription.QUALIFICATION, max_length=EducationValidators.MAX_LENGHT_QUALIFICATION)


class BaseLevel(BaseModel):
    """Modelo base para los niveles de estudios|idiomas
    
        Atributos:
            name: Nombre del nivel de estudios|idiomas
            value: Valor del nivel de estudios|idiomas"""

    name: str = Field(description=LevelDescription.NAME, max_length=LevelValidators.MAX_LENGHT_NAME)
    value: int = Field(description=LevelDescription.VALUE, ge=LevelValidators.MIN_VALUE)

class BaseAddress(BaseModel):
    """Modelo base para las direcciones
    
        Atributos:
            postal_code: Codigo postal
            street: Calle
            city: Ciudad
            province: Provincia"""

    postal_code: int = Field(description=AddressDescription.POSTAL_CODE, ge=AddressValidators.MIN_POSTAL_CODE, le=AddressValidators.MAX_POSTAL_CODE)
    street: str = Field(description=AddressDescription.STREET, max_length=AddressValidators.MAX_LENGHT_STREET)
    city: str = Field(description=AddressDescription.CITY, max_length=AddressValidators.MAX_LENGHT_CITY)
    province: str = Field(description=AddressDescription.PROVINCE, max_length=AddressValidators.MAX_LENGHT_PROVINCE)


class BaseJob(BaseModel):
    """Modelo base para los trabajos
    
        Atributos:
            title: Titulo del puesto de trabajo (ejemplo: Desarrollador web)
            description: Descripcion del puesto de trabajo
            skills: Lista de habilidades requeridas para el trabajo
            work_schedule: Disponibilidad de jornada laboral requerida
            required_experience_months: Experiencia requerida en meses
            active: Estado de la oferta de trabajo (abierta o cerrada))"""

    title: str = Field(description=JobDescription.TITLE, max_length=JobValidators.MAX_LENGHT_TITLE)
    description: str = Field(description=JobDescription.DESC, max_length=JobValidators.MAX_LENGHT_DESC)
    skills: list[str] = Field(description=JobDescription.SKILLS, max_length=JobValidators.MAX_ITEMS_SKILLS)
    work_schedule: WorkSchedule = Field(description=JobDescription.WORK_SHEDULE)
    required_experience: int = Field(description=JobDescription.REQUIRED_EXP, ge=JobValidators.MIN_REQUIRED_EXP)
    active: bool = Field(description=JobDescription.ACTIVE)

    @field_validator('skills')
    @classmethod
    def validate(cls, list):
        return validate_skills_len(list)


class Token(BaseModel):
    """Clase para representar un token de seguridad.
    
       Atributos:
        - acess_token: token de seguridad
        - token_type: tipo de token de seguridad"""
    
    access_token: str
    token_type: str