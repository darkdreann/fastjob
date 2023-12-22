from typing import Optional, Any
from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic.networks import EmailStr
from api.models.enums.models import WorkSchedule
from api.models.metadata import *
from api.models.functions.validate_functions import *

class BaseUser(BaseModel):
    """
    Modelo base para los usuarios
    
    Atributos:
    - username: Nombre identificador del usuario
    - email: Correo electrónico
    - name: Nombre del usuario
    - surname: Apellido del usuario
    - phone_numbers: Lista de números de teléfono
    """

    username: str = Field(description=UserDescriptions.USERNAME, max_length=UserValidators.MAX_LENGTH_USERNAME, min_length=UserValidators.MIN_LENGTH_USERNAME)
    email: EmailStr = Field(description=UserDescriptions.EMAIL)
    name: str = Field(description=UserDescriptions.NAME, max_length=UserValidators.MAX_LENGTH_NAME)
    surname: str = Field(description=UserDescriptions.SURNAME, max_length=UserValidators.MAX_LENGTH_SURNAME)
    phone_numbers: list[int] = Field(description=UserDescriptions.PHONE_NUMBER, max_length=UserValidators.MAX_ITEMS_PHONE_NUMBERS)

    @field_validator('phone_numbers')
    @classmethod
    def phone_validate(cls, list):
        return validate_phone_numbers(list)
    

class BaseCandidate(BaseModel):
    """
    Modelo base para los candidatos
    
    Atributos:
    - skills: Lista de habilidades del candidato
    - availability: Lista de disponibilidad de jornada laboral del candidato
    """

    skills: list[str] = Field(description=CandidateDescription.SKILLS, max_length=CandidateValidators.MAX_ITEMS_SKILLS)
    availability: list[WorkSchedule] = Field(description=CandidateDescription.AVAILABILITY, max_length=CandidateValidators.MAX_ITEMS_AVAILABILITY)

    @field_validator('skills')
    @classmethod
    def validate(cls, list):
        return validate_skills_len(list)
    
class BaseCompany(BaseModel):
    """
    Modelo base para las empresas
    
    Atributos:
    - tin: Número de identificación de la empresa
    - company_name: Nombre de la empresa
    """
     
    tin: str = Field(description=CompanyDescription.TIN, pattern=CompanyValidators.REGEX_TIN)
    company_name: str = Field(description=CompanyDescription.COMPANY_NAME, max_length=CompanyValidators.MAX_LENGTH_COMPANY_NAME)


class BaseLanguage(BaseModel):
    """
    Modelo base para los idiomas
    
    Atributos:
    - name: Nombre del idioma
    """
     
    name: str = Field(description=LanguageDescription.NAME, max_length=LanguageValidators.MAX_LENGTH_NAME)

class BaseSector(BaseModel):
    """
    Modelo base para los sectores
    
    Atributos:
    - category: Categoría del sector
    - subcategory: Subcategoría del sector
    """
     
    category: str = Field(description=SectorDescription.CATEGORY, max_length=SectorValidators.MAX_LENGTH_CATEGORY)
    subcategory: str = Field(description=SectorDescription.SUBCATEGORY, max_length=SectorValidators.MAX_LENGTH_SUBCATEGORY)

class BaseExperience(BaseModel):
    """
    Modelo base para las experiencias laborales
    
    Atributos:
    - company_name: Nombre de la empresa
    - job_position: Posición en la empresa
    - job_position_description: Descripción del puesto
    - start_date: Fecha de inicio
    - end_date: Fecha de finalización
    """
     
    company_name: str = Field(description=ExperienceDescription.COMPANY_NAME, max_length=ExperienceValidators.MAX_LENGTH_COMPANY_NAME)
    job_position: str = Field(description=ExperienceDescription.POSITION, max_length=ExperienceValidators.MAX_LENGTH_POSITION)
    job_position_description: str = Field(description=ExperienceDescription.POSITION_DESC, max_length=ExperienceValidators.MAX_LENGTH_POSITION_DESC)
    start_date: date = Field(description=ExperienceDescription.START_DATE)
    end_date: Optional[date] = Field(description=ExperienceDescription.END_DATE, default=None)

    @model_validator(mode='after')
    def end_date_validate(self):
        """Valida las fechas"""

        validate_dates(self.start_date)
        if self.end_date is not None:
            validate_dates(self.end_date)
            validate_end_date(self.start_date, self.end_date)

        return self
        


class BaseEducation(BaseModel):
    """
    Modelo base para la formación académica
    
    Atributos:
    - qualification: Titulación obtenida
    """

    qualification: str = Field(description=EducationDescription.QUALIFICATION, max_length=EducationValidators.MAX_LENGTH_QUALIFICATION)


class BaseLevel(BaseModel):
    """
    Modelo base para los niveles de estudios|idiomas
    
    Atributos:
    - name: Nombre del nivel de estudios|idiomas
    - value: Valor del nivel de estudios|idiomas
    """

    name: str = Field(description=LevelDescription.NAME, max_length=LevelValidators.MAX_LENGTH_NAME)
    value: int = Field(description=LevelDescription.VALUE, ge=LevelValidators.MIN_VALUE)

class BaseAddress(BaseModel):
    """
    Modelo base para las direcciones
    
    Atributos:
    - postal_code: Código postal
    - street: Calle
    - city: Ciudad
    - province: Provincia
    """

    postal_code: int = Field(description=AddressDescription.POSTAL_CODE, ge=AddressValidators.MIN_POSTAL_CODE, le=AddressValidators.MAX_POSTAL_CODE)
    street: str = Field(description=AddressDescription.STREET, max_length=AddressValidators.MAX_LENGTH_STREET)
    city: str = Field(description=AddressDescription.CITY, max_length=AddressValidators.MAX_LENGTH_CITY)
    province: str = Field(description=AddressDescription.PROVINCE, max_length=AddressValidators.MAX_LENGTH_PROVINCE)


class BaseJob(BaseModel):
    """
    Modelo base para los trabajos
    
    Atributos:
    - title: Título del puesto de trabajo
    - description: Descripción del puesto de trabajo
    - skills: Lista de habilidades requeridas para el trabajo
    - work_schedule: Disponibilidad de jornada laboral requerida
    - required_experience: Experiencia requerida en meses
    - active: Estado de la oferta de trabajo (abierta o cerrada)
    """

    title: str = Field(description=JobDescription.TITLE, max_length=JobValidators.MAX_LENGTH_TITLE)
    description: str = Field(description=JobDescription.DESC, max_length=JobValidators.MAX_LENGTH_DESC)
    skills: list[str] = Field(description=JobDescription.SKILLS, max_length=JobValidators.MAX_ITEMS_SKILLS)
    work_schedule: WorkSchedule = Field(description=JobDescription.WORK_SCHEDULE)
    required_experience: int = Field(description=JobDescription.REQUIRED_EXP, ge=JobValidators.MIN_REQUIRED_EXP)
    active: bool = Field(description=JobDescription.ACTIVE)

    @field_validator('skills')
    @classmethod
    def validate(cls, list):
        return validate_skills_len(list)


class Token(BaseModel):
    """
    Clase para representar un token de seguridad.
    
    Atributos:
    - access_token: Token de seguridad
    - token_type: Tipo de token de seguridad
    """
    
    access_token: str
    token_type: str


class QueryParams(BaseModel):
    """
    Clase que representa los parámetros para filtrar candidatos.
    """

    joins: list[dict[str, Any]] = Field(default=[])
    where: list[Any] = Field(default=[])
    options: list[Any] = Field(default=[])

    fields: list[Any]
    scalar: bool
    unique: bool

    joined: set[Any] = Field(default=set(), exclude=True)

    def add_join(self, join_table: dict[str, Any]):
        """
        Agrega una tabla de unión a los parámetros del candidato.

        Args:
            join_table (dict[str, Any]): La tabla de unión a agregar.
        """
        if join_table["target"] in self.joined:
            return

        self.joined.add(join_table["target"])
        self.joins.append(join_table)
    
    def add_join_list(self, join_list: tuple[dict[str, Any]]) -> None:
        """
        Agrega una lista de tablas de unión a los parámetros del candidato.

        Args:
            join_list (tuple[dict[str, Any]]): La lista de tablas de unión a agregar.
        """
        for join in join_list:
            self.add_join(join)