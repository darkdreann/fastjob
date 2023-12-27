from typing import Optional
from uuid import UUID
from api.models.base_models import *
from api.models.enums.models import UserType


class CreateAddress(BaseAddress):
    """
    Modelo para crear una dirección

    Atributos:
    - postal_code: Código postal
    - street: Calle de la dirección
    - city: Ciudad de la dirección
    - province: Provincia de la dirección
    """


class CreateUser(BaseUser):
    """
    Modelo para crear un usuario

    Atributos:
    - username: Nombre identificador del usuario
    - email: Correo electrónico
    - name: Nombre del usuario
    - surname: Apellido del usuario
    - phone_numbers: Lista de números de teléfono
    - password: Contraseña del usuario
    - address: Dirección del usuario
    """

    password: str = Field(description=UserDescriptions.PASSWORD)
    address: CreateAddress = Field(description=UserDescriptions.ADDRESS, exclude=True)

    @field_validator('password')
    @classmethod
    def password_validate(cls, password):
        """Valida que la contraseña cumpla los requisitos de seguridad."""

        return validate_password(password)


class CreateCandidate(BaseCandidate):
    """
    Modelo para crear un candidato

    Atributos:
    - username: Nombre identificador del usuario
    - email: Correo electrónico
    - name: Nombre del usuario
    - surname: Apellido del usuario
    - phone_numbers: Lista de números de teléfono
    - password: Contraseña del usuario
    - address: Dirección del usuario
    - skills: Lista de habilidades del candidato
    - availability: Lista de disponibilidad de jornada laboral del candidato
    """

    user: CreateUser = Field(description=CandidateDescription.USER)


class CreateCompany(BaseCompany):
    """
    Modelo para crear una empresa

    Atributos:
    - username: Nombre identificador del usuario
    - email: Correo electrónico
    - name: Nombre del usuario
    - surname: Apellido del usuario
    - phone_numbers: Lista de números de teléfono
    - password: Contraseña del usuario
    - address: Dirección del usuario
    - tin: Número de identificación de la empresa
    - company_name: Nombre de la empresa
    """

    user: CreateUser = Field(description=CandidateDescription.USER)


class CreateLanguage(BaseLanguage):
    """
    Modelo para crear un idioma

    Atributos:
    - name: Nombre del idioma
    """


class CreateSector(BaseSector):
    """
    Modelo para crear un sector

    Atributos:
    - category: Categoría del sector
    - subcategory: Subcategoría del sector
    """


class CreateExperience(BaseExperience):
    """
    Modelo para crear una experiencia

    Atributos:
    - company_name: Nombre de la empresa
    - position: Puesto de trabajo
    - position_description: Descripción del puesto de trabajo
    - start_date: Fecha de inicio
    - end_date: Fecha de finalización
    - sector_id: Sector de la experiencia
    """

    sector_id: UUID = Field(description=ExperienceDescription.SECTOR_ID)


class CreateEducation(BaseEducation):
    """
    Modelo para crear una formación

    Atributos:
    - qualification: Título de la formación
    - level_id: Nivel de la formación
    - sector_id: Sector de la formación si lo tiene
    """

    level_id: UUID = Field(description=EducationDescription.LEVEL_ID)
    sector_id: Optional[UUID] = Field(description=EducationDescription.SECTOR_ID, default=None)


class CreateLevel(BaseLevel):
    """
    Modelo para crear un nivel de formación o idioma

    Atributos:
    - name: Nombre del nivel de formación o idioma
    - value: Valor numérico del nivel de formación o idioma
    """


class CreateJobLanguage(BaseModel):
    """
    Modelo para crear un trabajo de idioma.

    Atributos:
    - language_id: ID del idioma.
    - language_level_id: ID del nivel de idioma.
    """

    language_id: UUID = Field(description=LanguageDescription.LANGUAGE_ID)
    language_level_id: UUID = Field(description=LevelDescription.LEVEL_ID)


class CreateJob(BaseJob):
    """
    Modelo para crear una oferta

    Atributos:
    - title: Título del puesto de trabajo
    - description: Descripción del puesto de trabajo
    - skills: Lista de habilidades requeridas para el trabajo
    - work_schedule: Disponibilidad de jornada laboral requerida
    - required_experience_months: Experiencia requerida en meses
    - active: Estado de la oferta de trabajo (abierta o cerrada)
    - address: Dirección de la oferta
    - required_education: Formación requerida
    - required_language_list: Lista de idiomas requeridos
    - sector_id: Sector de la oferta
    - company_id: Empresa que publica la oferta
    """

    address: CreateAddress = Field(description=JobDescription.ADDRESS)
    required_education: Optional[UUID] = Field(description=JobDescription.REQUIRED_EDUCATION_ID, default=None)
    sector_id: UUID = Field(description=JobDescription.SECTOR_ID)
    company_id: UUID = Field(description=JobDescription.COMPANY_ID)
