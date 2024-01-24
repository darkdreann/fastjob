from uuid import UUID
from pydantic import BaseModel, field_serializer
from datetime import date, timedelta
from typing import Optional
from api.models.base_models import *
from api.models.enums.models import UserType
from api.models.metadata.constants import DAYS_TO_MONTHS_DIVIDER

class ReadAddress(BaseAddress):
    """
    Modelo para leer una dirección.

    Atributos:
    - id: Identificador de la dirección.
    - postal_code: Código postal.
    - street: Calle de la dirección.
    - city: Ciudad de la dirección.
    - province: Provincia de la dirección.
    """
    
    id: UUID = Field(description=AddressDescription.ID)
    
class ReadUser(BaseUser):
    """
    Modelo para leer un usuario.

    Atributos:
    - id: Identificador del usuario.
    - username: Nombre identificador del usuario.
    - email: Correo electrónico.
    - name: Nombre del usuario.
    - surname: Apellido del usuario.
    - phone_numbers: Lista de números de teléfono.
    - user_type: Tipo de usuario.
    """
    
    id: UUID = Field(description=UserDescriptions.USER_ID)
    user_type: UserType = Field(description=UserDescriptions.USER_TYPE)

class ReadUserComplete(ReadUser):
    """
    Modelo para leer un usuario completo.

    Atributos:
    - id: Identificador del usuario.
    - username: Nombre identificador del usuario.
    - email: Correo electrónico.
    - name: Nombre del usuario.
    - surname: Apellido del usuario.
    - phone_numbers: Lista de números de teléfono.
    - user_type: Tipo de usuario.
    - address: Dirección del usuario.
    """
    
    address: ReadAddress = Field(description=UserDescriptions.ADDRESS)

class ReadCandidate(BaseCandidate):
    """
    Modelo para leer un candidato.

    Atributos:
    - id: Identificador del usuario.
    - username: Nombre identificador del usuario.
    - email: Correo electrónico.
    - name: Nombre del usuario.
    - surname: Apellido del usuario.
    - phone_numbers: Lista de números de teléfono.
    - address: Dirección del usuario.
    - user_type: Tipo de usuario.
    - skills: Lista de habilidades del candidato.
    - availability: Lista de disponibilidad de jornada laboral del candidato.
    """
    
    user: ReadUserComplete = Field(description=CandidateDescription.USER)

class ReadCompany(BaseCompany):
    """
    Modelo para leer una empresa.

    Atributos:
    - id: Identificador del usuario.
    - username: Nombre identificador del usuario.
    - email: Correo electrónico.
    - name: Nombre del usuario.
    - surname: Apellido del usuario.
    - phone_numbers: Lista de números de teléfono.
    - address: Dirección del usuario.
    - user_type: Tipo de usuario.
    - tin: Número de identificación de la empresa.
    - company_name: Nombre de la empresa.
    """
    
    user: ReadUserComplete = Field(description=CompanyDescription.USER)
    

class ReadLanguage(BaseLanguage):
    """
    Modelo para leer un idioma.

    Atributos:
    - id: Identificador del idioma.
    - name: Nombre del idioma.
    """
    
    id: UUID = Field(description=LanguageDescription.LANGUAGE_ID)


class ReadSectorNoCategory(BaseModel):
    """
    Modelo para leer un sector.

    Atributos:
    - id: Identificador del sector.
    - subcategory: La subcategoría del sector.
    """
    
    id: UUID = Field(description=SectorDescription.SECTOR_ID)
    subcategory: str = Field(description=SectorDescription.SUBCATEGORY, max_length=SectorValidators.MAX_LENGTH_SUBCATEGORY)


class ReadSector(ReadSectorNoCategory):
    """
    Modelo para leer un sector.

    Atributos:
    - id: Identificador del sector.
    - category: La categoría del sector.
    - subcategory: La subcategoría del sector.
    """
    
    category: str = Field(description=SectorDescription.CATEGORY, max_length=SectorValidators.MAX_LENGTH_CATEGORY)

class ReadExperience(BaseExperience):
    """
    Modelo para leer una experiencia.

    Atributos:
    - id: Identificador de la experiencia.
    - company_name: Nombre de la empresa.
    - position: Puesto de trabajo.
    - position_description: Descripción del puesto de trabajo.
    - start_date: Fecha de inicio.
    - end_date: Fecha de finalización.
    """
    
    id: UUID = Field(description=ExperienceDescription.EXPERIENCE_ID)

class ReadEducation(BaseEducation):
    """
    Modelo para leer una formación.

    Atributos:
    - id: Identificador de la formación.
    - qualification: Título de la formación.
    """
    
    id: UUID = Field(description=EducationDescription.EDUCATION_ID)

class ReadLevel(BaseLevel):
    """
    Modelo para leer un nivel.

    Atributos:
    - id: Identificador del nivel.
    - name: Nombre del nivel de formación o idioma.
    - value: Valor numérico del nivel de formación o idioma.
    """
    
    id: UUID = Field(description=LevelDescription.LEVEL_ID)


class ReadJob(BaseJob):
    """
    Modelo para leer una oferta.

    Atributos:
    - id: Identificador de la oferta.
    - title: Título de la oferta.
    - description: Descripción de la oferta.
    - skills: Lista de habilidades de la oferta.
    - required_experience: Experiencia requerida para la oferta.
    - active: Estado de la oferta (abierta o cerrada).
    - publication_date: Fecha de publicación de la oferta.
    """
    
    id: UUID = Field(description=JobDescription.JOB_ID)
    publication_date: date = Field(description=JobDescription.PUBLICATION_DATE)
    required_experience: timedelta = Field(description=JobDescription.REQUIRED_EXP, ge=JobValidators.MIN_REQUIRED_EXP)

    @field_serializer('required_experience', when_used="always")
    def convert_num(value):
        return round(value.days / DAYS_TO_MONTHS_DIVIDER)


############################################################################################################################################################################
class ReadCandidateRelationJob(BaseModel):
    """
    Modelo para leer la relación entre un candidato y un trabajo.

    Atributos:
    - job: objeto ReadJob que representa al trabajo.
    - inscription_date: fecha de inscripción del candidato al trabajo.
    """
    
    job: ReadJob = Field(description=CandidateJobDescriptions.JOB)
    inscription_date: date = Field(description=CandidateJobDescriptions.INCRIPTION_DATE)

class ReadJobRelationCandidate(BaseModel):
    """
    Modelo para leer la relación entre un trabajo y un candidato.

    Atributos:
    - candidate: objeto ReadCandidate que representa al candidato.
    - inscription_date: fecha de inscripción del candidato al trabajo.
    """

    candidate: ReadCandidate = Field(description=CandidateJobDescriptions.CANDIDATE)
    inscription_date: date = Field(description=CandidateJobDescriptions.INCRIPTION_DATE)


class ReadCandidateRelationLanguage(BaseModel):
    """
    Modelo para leer la relación entre un candidato y un idioma.

    Atributos:
    - language: objeto ReadLanguage que representa el idioma del candidato.
    - language_level: objeto ReadLevel que representa el nivel del idioma del candidato.
    """

    language: ReadLanguage = Field(description=CandidateLanguageDescriptions.LANGUAGE)
    language_level: ReadLevel = Field(description=CandidateLanguageDescriptions.LANGUAGE_LEVEL)

class ReadLanguageRelationCandidate(BaseModel):
    """	
    Modelo para leer la relación entre un idioma y un candidato.

    Atributos:
    - candidate: objeto ReadCandidate que representa al candidato.
    - level: objeto ReadLevel que representa el nivel del idioma del candidato.
    """

    candidate: ReadCandidate = Field(description=CandidateLanguageDescriptions.CANDIDATE)
    level: ReadLevel = Field(description=CandidateLanguageDescriptions.LANGUAGE_LEVEL)

class ReadLevelLanguageRelationsCandidate(BaseModel):
    """
    Modelo para leer la relación entre un candidato y un idioma.

    Atributos:
    - language: objeto ReadLanguage que representa el idioma del candidato.
    - candidate: objeto ReadCandidate que representa al candidato.
    """

    language: ReadLanguage = Field(description=CandidateLanguageDescriptions.LANGUAGE)
    candidate: ReadCandidate = Field(description=CandidateLanguageDescriptions.CANDIDATE)

class ReadEducationRelationCandidate(BaseModel):
    """
    Modelo para leer la relación entre una formación y un candidato.

    Atributos:
    - candidate: objeto ReadCandidate que representa al candidato.
    - completion_date: fecha de finalización de la formación del candidato.
    """

    candidate: ReadCandidate = Field(description=EducationCandidateDescriptions.CANDIDATE)
    completion_date: date = Field(description=EducationCandidateDescriptions.COMPLETION_DATE)

class ReadJobRelationLanguage(BaseModel):
    """
    Modelo para leer la relación entre un trabajo y un idioma.

    Atributos:
    - language: objeto ReadLanguage que representa el idioma del trabajo.
    - language_level: objeto ReadLevel que representa el nivel del idioma del trabajo.
    """

    language: ReadLanguage = Field(description=JobLanguageDescriptions.LANGUAGE)
    language_level: ReadLevel = Field(description=JobLanguageDescriptions.LEVEL)

class ReadLanguageRelationJob(BaseModel):
    """
    Modelo para leer la relación entre un idioma y un trabajo.

    Atributos:
    - job: objeto ReadJob que representa al trabajo.
    - level: objeto ReadLevel que representa el nivel del idioma del trabajo.
    """

    job: ReadJob = Field(description=JobLanguageDescriptions.JOB)
    level: ReadLevel = Field(description=JobLanguageDescriptions.LEVEL)

class ReadLevelLanguageRelationsJob(BaseModel):
    """
    Modelo para leer la relación entre un idioma y un trabajo.

    Atributos:
    - job: objeto ReadJob que representa al trabajo.
    - language: objeto ReadLanguage que representa el idioma del trabajo.
    """

    job: ReadJob = Field(description=JobLanguageDescriptions.JOB)
    language: ReadLanguage = Field(description=JobLanguageDescriptions.LANGUAGE)

class ReadSectorRelationEducation(BaseModel):
    """
    Modelo para leer la relación entre un sector y una formación.

    Atributos:
    - education: objeto ReadEducation que representa la formación del sector.
    """

    education: ReadEducation = Field(description=SectorEducationDescriptions.EDUCATION)


class ReadEducationRelationSector(BaseModel):
    """
    Modelo para leer la relación entre una formación y un sector.

    Atributos:
    - sector: objeto ReadSector que representa el sector de la formación.
    """

    sector: ReadSector = Field(description=SectorEducationDescriptions.SECTOR)


############################################################################################################################################################################
class ReadExperienceComplete(ReadExperience):
    """
    Modelo para leer una experiencia con todos sus datos incluidos el sector al que pertenece.
    Los atributos de las relaciones son opcionales para mostrar solo los datos que se necesiten.

    Atributos:
    - id: Identificador de la experiencia
    - company_name: Nombre de la empresa
    - position: Puesto de trabajo
    - position_description: Descripción del puesto de trabajo
    - start_date: Fecha de inicio
    - end_date: Fecha de finalización
    - sector: Sector de la experiencia
    """
    
    sector: Optional[ReadSector] = Field(description=ExperienceDescription.SECTOR, default=None)

class ReadEducationComplete(ReadEducation):
    """
    Modelo para leer una formación con todos sus datos incluidos el sector y el nivel de formación.
    Puede no tener sector.

    Atributos:
    - id: Identificador de la formación
    - qualification: Título de la formación
    - level: Nivel de la formación
    - sector: Sector de la formación
    """
    
    level: ReadLevel = Field(description=EducationDescription.LEVEL)
    sector: Optional[ReadEducationRelationSector] = Field(description=EducationDescription.SECTOR, default=None)


class ReadCandidateRelationEducation(BaseModel):
    """
    Modelo para leer la relación entre un candidato y una formación.

    Atributos:
    - education: Objeto ReadEducation que representa la formación del candidato.
    - completion_date: Fecha de finalización de la formación del candidato.
    """

    education: ReadEducationComplete = Field(description=EducationCandidateDescriptions.EDUCATION)
    completion_date: date = Field(description=EducationCandidateDescriptions.COMPLETION_DATE)

class ReadCandidateMinimal(BaseModel):

    id: UUID = Field(description=UserDescriptions.USER_ID)
    name: str = Field(description=UserDescriptions.NAME)
    surname: str = Field(description=UserDescriptions.SURNAME)
    province: str = Field(description=AddressDescription.PROVINCE)
    skills: list[str] = Field(description=CandidateDescription.SKILLS, default=[])
    availability: list[str] = Field(description=CandidateDescription.AVAILABILITY, default=[])

class ReadCandidateComplete(ReadCandidate):
    """
    Modelo para leer un candidato con todos sus datos incluidas las relaciones con otras tablas experiencia, educación, idiomas y trabajos a los que se ha aplicado.
    Los atributos de las relaciones son opcionales para mostrar solo los datos que se necesiten.

    Atributos:
    - id: Identificador del usuario
    - username: Nombre identificador del usuario
    - email: Correo electrónico
    - name: Nombre del usuario
    - surname: Apellido del usuario
    - phone_numbers: Lista de números de teléfono
    - address: Dirección del usuario
    - user_type: Tipo de usuario
    - skills: Lista de habilidades del candidato
    - availability: Lista de disponibilidad de jornada laboral del candidato
    - experience_list: Lista de experiencias del candidato
    - language_list: Lista de educaciones del candidato
    - language_list: Lista de idiomas del candidato
    - applied_jobs_list: Lista de trabajos a los que se ha aplicado
    """

    experience_list: Optional[list[ReadExperienceComplete]] = Field(description=CandidateDescription.EXPERIENCE, default=[])
    education_list: Optional[list[ReadCandidateRelationEducation]] = Field(description=CandidateDescription.EDUCATION, default=[])
    language_list: Optional[list[ReadCandidateRelationLanguage]] = Field(description=CandidateDescription.LANGUAGE, default=[])
    applied_jobs_list: Optional[list[ReadCandidateRelationJob]] = Field(description=CandidateDescription.JOBS, default=[])

class ReadCompanyComplete(ReadCompany):
    """
    Modelo para leer una empresa con todos sus datos incluidas sus ofertas de trabajo.
    Los atributos de las relaciones son opcionales para mostrar solo los datos que se necesiten.

    Atributos:
    - id: Identificador del usuario
    - username: Nombre identificador del usuario
    - email: Correo electrónico
    - name: Nombre del usuario
    - surname: Apellido del usuario
    - phone_numbers: Lista de números de teléfono
    - address: Dirección del usuario
    - user_type: Tipo de usuario
    - tin: Número de identificación de la empresa
    - company_name: Nombre de la empresa
    - jobs: Lista de trabajos de la empresa
    """
    
    jobs: Optional[list[ReadJob]] = Field(description=CompanyDescription.JOB, default=[])

class ReadLanguageComplete(ReadLanguage):
    """
    Modelo para leer un idioma con todos sus datos incluidos los usuarios que tienen ese idioma.
    Los atributos de las relaciones son opcionales para mostrar solo los datos que se necesiten.

    Atributos:
    - name: Nombre del idioma
    - jobs_list: Lista de trabajos que requieren ese idioma
    - candidates_list: Lista de candidatos que tienen ese idioma
    """
    
    candidates_list: Optional[list[ReadLanguageRelationCandidate]] = Field(description=LanguageDescription.CANDIDATE, default=[])
    jobs_list: Optional[list[ReadLanguageRelationJob]] = Field(description=LanguageDescription.JOB, default=[])


class ReadSectorComplete(ReadSector):
    """
    Modelo para leer un sector con todos sus datos incluidas las formaciones, experiencias y trabajos que tienen ese sector.

    Atributos:
    - id: Identificador del sector
    - category: La categoría del sector
    - subcategory: La subcategoría del sector
    - education_list: Lista de formaciones que pertenecen al sector
    - experience_list: Lista de experiencias que pertenecen al sector
    - job_list: Lista de trabajos que pertenecen al sector
    """
    
    education_list: Optional[list[ReadSectorRelationEducation]] = Field(description=SectorDescription.EDUCATIONS, default=[])
    experience_list: Optional[list[ReadExperience]] = Field(description=SectorDescription.EXPERIENCES, default=[])
    job_list: Optional[list[ReadJob]] = Field(description=SectorDescription.JOBS, default=[])

    

class ReadEducationWithUses(ReadEducationComplete):
    """
    Modelo para leer una formación con todos sus datos incluidos los candidatos que tienen esa formación.

    Atributos:
    - id: Identificador de la formación
    - qualification: Título de la formación
    - level: Nivel de la formación
    - sector: Sector de la formación
    - candidates_list: Lista de candidatos con esa formación
    - jobs_list: Lista de trabajos que requieren esa formación
    """

    candidates_list: Optional[list[ReadEducationRelationCandidate]] = Field(description=EducationDescription.CANDIDATES, default=[])
    jobs_list: Optional[list[ReadJob]] = Field(description=EducationDescription.JOB, default=[])

class ReadLevelLanguage(ReadLevel):
    """
    Modelo para leer un nivel con todos sus datos incluidos los idiomas que tienen ese nivel.
    Los atributos de las relaciones son opcionales para mostrar solo los datos que se necesiten.

    Atributos:
    - id: Identificador del nivel
    - name: Nombre del nivel de formación o idioma
    - value: Valor numérico del nivel de formación o idioma
    - candidates: Lista de candidatos con ese nivel de idioma
    - jobs: Lista de trabajos que requieren ese nivel de idioma
    """
    
    candidates: Optional[list[ReadLevelLanguageRelationsCandidate]] = Field(description=LanguageLevelDescription.CANDIDATES, default=[])
    jobs: Optional[list[ReadLevelLanguageRelationsJob]] = Field(description=LanguageLevelDescription.JOBS, default=[])

class ReadLevelEducation(ReadLevel):
    """
    Modelo para leer un nivel con todos sus datos incluidas las formaciones que tienen ese nivel.
    Los atributos de las relaciones son opcionales para mostrar solo los datos que se necesiten.

    Atributos:
    - id: Identificador del nivel
    - name: Nombre del nivel de formación o idioma
    - value: Valor numérico del nivel de formación o idioma
    - education_list: Lista de formaciones con ese nivel
    """
    
    education_list: Optional[list[ReadEducation]] = Field(description=EducationLevelDescription.EDUCATION, default=[])
    


class ReadAddressComplete(ReadAddress):
    """
    Modelo para leer una dirección con todos sus datos incluidos los usuarios y trabajos que tienen esa dirección.
    Los atributos de las relaciones son opcionales para mostrar solo los datos que se necesiten.

    Atributos:
    - postal_code: Código postal
    - street: Calle de la dirección
    - city: Ciudad de la dirección
    - province: Provincia de la dirección
    - users_list: Lista de usuarios que tienen esa dirección
    - jobs_list: Lista de trabajos que tienen esa dirección
    """
    
    users_list: Optional[list[ReadUser]] = Field(description=AddressDescription.USERS, default=[])
    jobs_list: Optional[list[ReadJob]] = Field(description=AddressDescription.JOB, default=[])


class ReadJobRelationEducation(BaseModel):
    """
    Modelo para leer la relación entre un trabajo y una formación.

    Atributos:
    - education: Objeto ReadEducation que representa la formación del trabajo.
    """

    education: ReadEducationComplete = Field(description=JobDescription.REQUIRED_EDUCATION)

class ReadJobMinimal(BaseModel):
    """
    Modelo para leer una oferta con los datos mínimos.

    Atributos:
    - id: Identificador de la oferta
    - title: Título de la oferta
    - description: Descripción de la oferta
    - province: Provincia de la dirección de la oferta
    """

    id: UUID = Field(description=JobDescription.JOB_ID)
    title: str = Field(description=JobDescription.TITLE)
    description: str = Field(description=JobDescription.DESC)
    province: str = Field(description=AddressDescription.PROVINCE)


class ReadJobComplete(ReadJob):
    """
    Modelo para leer una oferta con todos sus datos incluidos la empresa, el sector, la dirección, el nivel de formación requerido y los idiomas requeridos.
    Los atributos de las relaciones son opcionales para mostrar solo los datos que se necesiten.

    Atributos:
    - id: Identificador de la oferta
    - title: Título de la oferta
    - description: Descripción de la oferta
    - skills: Lista de habilidades de la oferta
    - required_experience_months: Experiencia requerida para la oferta
    - active: Estado de la oferta (abierta o cerrada)
    - publication_date: Fecha de publicación de la oferta
    - required_education: Formación requerida
    - sector: Sector al que pertenece la oferta
    - address: Dirección de la oferta
    - language_list: Lista de idiomas requeridos por la oferta
    """

    sector: ReadSector = Field(description=JobDescription.SECTOR, default=None)
    address: ReadAddress = Field(description=JobDescription.ADDRESS, default=None)
    required_education: Optional[ReadJobRelationEducation] = Field(description=JobDescription.REQUIRED_EDUCATION, default=None)
    language_list: Optional[list[ReadJobRelationLanguage]] = Field(description=JobDescription.LANGUAGES, default=[])


class ReadJobCompleteWithUsers(ReadJobComplete):
    """
    Clase que representa un trabajo completo con información adicional detallada.

    Atributos:
    - company: Opcional[ReadCompany]: La empresa asociada al trabajo.
    - candidates: Opcional[list[ReadJobRelationCandidate]]: La lista de candidatos relacionados al trabajo.
    """
    
    company: Optional[ReadCompany] = Field(description=JobDescription.COMPANY, default=None)
    candidates: Optional[list[ReadJobRelationCandidate]] = Field(description=JobDescription.CANDIDATES, default=[])