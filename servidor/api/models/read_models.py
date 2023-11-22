from uuid import UUID
from pydantic import BaseModel, root_validator
from typing import Optional
from api.models.base_models import *
from api.models.enums.models import UserType



class ReadAdress(BaseAdress):
    """Modelo para leer una direccion

        Atributos:
            id: Identificador de la direccion
            postal_code: Codigo postal
            street: Calle de la direccion
            city: Ciudad de la direccion
            province: Provincia de la direccion"""
    
    id: UUID = Field(description=AdressDescription.ID)
    
class ReadUser(BaseUser):
    """Modelo para leer un usuario

        Atributos:
            id: Identificador del usuario
            username: nombre identificador del usuario
            email: Correo electronico
            name: Nombre del usuario
            surname: Apellido del usuario
            phone_numbers: Lista de numeros de telefono
            user_type: Tipo de usuario"""
    
    id: UUID = Field(description=UserDescriptions.USER_ID)
    user_type: UserType = Field(description=UserDescriptions.USER_TYPE)


class ReadUserComplete(ReadUser):
    """Modelo para leer un usuario

    Atributos:
        id: Identificador del usuario
        username: nombre identificador del usuario
        email: Correo electronico
        name: Nombre del usuario
        surname: Apellido del usuario
        phone_numbers: Lista de numeros de telefono
        user_type: Tipo de usuario
        adress: Direccion del usuario"""
    
    adress: ReadAdress = Field(description=UserDescriptions.ADRESS)

class ReadCandidate(BaseCandidate, ReadUserComplete):
    """Modelo para leer un candidato

        Atributos:
            id: Identificador del usuario
            username: nombre identificador del usuario
            email: Correo electronico
            name: Nombre del usuario
            surname: Apellido del usuario
            phone_numbers: Lista de numeros de telefono
            adress: Direccion del usuario
            user_type: Tipo de usuario
            skills: Lista de habilidades del candidato
            availability: Lista de disponibilidad de jornada laboral del candidato"""
    
    @root_validator(pre=True)
    def extract_user_data(cls, candidate) -> dict:
        """Extrae los datos del usuario y los añade a un diccionario con los datos del candidato."""

        data = {key: value for key, value in vars(candidate).items() if key != "user"}

        user = candidate.user

        if user is not None:
            user_data = {key: value for key, value in vars(user).items()}
            data.update(user_data)

        return data


class ReadCompany(BaseCompany, ReadUserComplete):
    """Modelo para leer una empresa

        Atributos:
            id: Identificador del usuario
            username: nombre identificador del usuario
            email: Correo electronico
            name: Nombre del usuario
            surname: Apellido del usuario
            phone_numbers: Lista de numeros de telefono
            adress: Direccion del usuario
            user_type: Tipo de usuario
            tin: Numero de identificacion de la empresa
            company_name: Nombre de la empresa"""
    
    @root_validator(pre=True)
    def extract_user_data(cls, company) -> dict:
        """Extrae los datos del usuario y los añade a un diccionario con los datos de la empresa."""


        data = {key: value for key, value in vars(company).items() if key != "user"}

        user = company.user

        if user is not None:
            user_data = {key: value for key, value in vars(user).items()}
            data.update(user_data)

        return data

class ReadLanguage(BaseLanguage):
    """Modelo para leer un idioma

        Atributos:
            id: Identificador del idioma
            name: Nombre del idioma"""
    
    id: UUID = Field(description=LanguageDescription.LANGUAGE_ID)
    
class ReadSector(BaseModel):
    """Modelo para leer un sector

        Atributos:
            id: Identificador del sector
            category: La categoría del sector
            subcategory: La subcategoría del sector"""
    
    id: Optional[UUID] = Field(description=SectorDescription.SECTOR_ID, default=None)
    category: Optional[str] = Field(description=SectorDescription.CATEGORY, max_length=SectorValidators.MAX_LENGHT_CATEGORY, default=None)
    subcategory: Optional[str] = Field(description=SectorDescription.SUBCATEGORY, max_length=SectorValidators.MAX_LENGHT_SUBCATEGORY, default=None)

class ReadExperience(BaseExperience):
    """Modelo para leer una experiencia

        Atributos:
            id: Identificador de la experiencia
            company_name: Nombre de la empresa
            position: Puesto de trabajo
            position_description: Descripcion del puesto de trabajo
            start_date: Fecha de inicio
            end_date: Fecha de finalizacion"""
    
    id: UUID = Field(description=ExperienceDescription.EXPERIENCE_ID)

class ReadEducation(BaseEducation):
    """Modelo para leer una formacion

        Atributos:
            id: Identificador de la formacion
            qualification: Titulo de la formacion"""
    
    id: UUID = Field(description=EducationDescription.EDUCATION_ID)

class ReadLevel(BaseLevel):
    """Modelo para leer un nivel

        Atributos:
            id: Identificador del nivel
            name: Nombre del nivel de formacion o idioma
            value: Valor numerico del nivel de formacion o idioma"""
    
    id: UUID = Field(description=LevelDescription.LEVEL_ID)


class ReadJob(BaseJob):
    """Modelo para leer una oferta

        Atributos:
            id: Identificador de la oferta
            title: Titulo de la oferta
            description: Descripcion de la oferta
            skills: Lista de habilidades de la oferta
            required_experience_months: Experiencia requerida para la oferta
            active: Estado de la oferta (abierta o cerrada)
            publication_date: Fecha de publicacion de la oferta"""
    
    id: UUID = Field(description=JobDescription.JOB_ID)
    publication_date: date = Field(description=JobDescription.PUBLICATION_DATE)


############################################################################################################################################################################
class ReadCandidateRelationJob(BaseModel):
    """
    Modelo para leer la relación entre un candidato y un trabajo.

    Atributos:
    - candidate: objeto ReadCandidate que representa al candidato.
    - compatibility: float que representa la compatibilidad del candidato con el trabajo.
    """
    
    job: ReadJob = Field(description=CandidateJobDescriptions.JOB)
    compatibility: float = Field(description=CandidateJobDescriptions.COMPATIBILITY)

class ReadJobRelationCandidate(BaseModel):
    """
    Modelo para leer la relación entre un trabajo y un candidato.

    Atributos:
    - job: objeto ReadJob que representa al trabajo.
    - compatibility: float que representa la compatibilidad del candidato con el trabajo.
    """

    candidate: ReadCandidate = Field(description=CandidateJobDescriptions.CANDIDATE)
    compatibility: float = Field(description=CandidateJobDescriptions.COMPATIBILITY)


class ReadCandidateRelationLanguage(BaseModel):
    """
    Modelo para leer la relación entre un candidato y un idioma.

    Atributos:
    - language: objeto ReadLanguage que representa el idioma del candidato.
    - level: objeto ReadLevel que representa el nivel del idioma del candidato.
    """

    language: ReadLanguage = Field(description=CandidateLanguageDescriptions.LANGUAGE)
    level: ReadLevel = Field(description=CandidateLanguageDescriptions.LANGUAGE_LEVEL)

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

class ReadCandidateRelationEducation(BaseModel):
    """
    Modelo para leer la relación entre un candidato y una formación.

    Atributos:
    - education: objeto ReadEducation que representa la formación del candidato.
    - completion_date: fecha de finalización de la formación del candidato.
    """

    education: ReadEducation = Field(description=EducationCandidateDescriptions.EDUCATION)
    completion_date: date = Field(description=EducationCandidateDescriptions.COMPLETION_DATE)

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
    - level: objeto ReadLevel que representa el nivel del idioma del trabajo.
    """

    language: ReadLanguage = Field(description=JobLanguageDescriptions.LANGUAGE)
    level: ReadLevel = Field(description=JobLanguageDescriptions.LEVEL)

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

class ReadCandidateComplete(ReadCandidate):
    """Modelo para leer un candidato con todos sus datos incluidos las relaciones con otras tablas experiencia, educacion, idiomas y trabajos a los que se ha aplicado.
        Los atributos de las relaciones son opcionales para mostrar solo los datos que se necesiten.

    Atributos:
        id: Identificador del usuario
        username: nombre identificador del usuario
        email: Correo electronico
        name: Nombre del usuario
        surname: Apellido del usuario
        phone_numbers: Lista de numeros de telefono
        adress: Direccion del usuario
        user_type: Tipo de usuario
        skills: Lista de habilidades del candidato
        availability: Lista de disponibilidad de jornada laboral del candidato
        experiences: Lista de experiencias del candidato
        education: Lista de educaciones del candidato
        languages: Lista de idiomas del candidato
        applied_jobs: Lista de trabajos a los que se ha aplicado"""

    experiences: Optional[list[ReadExperience]] = Field(description=CandidateDescription.EXPERIENCE, default=[])
    education: Optional[list[ReadCandidateRelationEducation]] = Field(description=CandidateDescription.EDUCATION, default=[])
    languages: Optional[list[ReadCandidateRelationLanguage]] = Field(description=CandidateDescription.LANGUAGE, default=[])
    applied_jobs: Optional[list[ReadCandidateRelationJob]] = Field(description=CandidateDescription.JOBS, default=[])

class ReadCompanyComplete(ReadCompany):
    """Modelo para leer una empresa con todos sus datos incluidos sus ofertas de trabajo.
        Los atributos de las relaciones son opcionales para mostrar solo los datos que se necesiten.

    Atributos:
        id: Identificador del usuario
        username: nombre identificador del usuario
        email: Correo electronico
        name: Nombre del usuario
        surname: Apellido del usuario
        phone_numbers: Lista de numeros de telefono
        adress: Direccion del usuario
        user_type: Tipo de usuario
        tin: Numero de identificacion de la empresa
        company_name: Nombre de la empresa
        jobs: Lista de trabajos de la empresa"""
    
    jobs: Optional[list[ReadJob]] = Field(description=CompanyDescription.JOB, default=[])

class ReadLanguageComplete(ReadLanguage):
    """Modelo para leer un idioma con todos sus datos incluidos los usuarios que tienen ese idioma.
        Los atributos de las relaciones son opcionales para mostrar solo los datos que se necesiten.

        Atributos:
            name: Nombre del idioma
            jobs: Lista de trabajos que requieren ese idioma
            candidates: Lista de candidatos que tienen ese idioma"""
    
    candidates_list: Optional[list[ReadLanguageRelationCandidate]] = Field(description=LanguageDescription.CANDIDATE, default=[])
    jobs_list: Optional[list[ReadLanguageRelationJob]] = Field(description=LanguageDescription.JOB, default=[])


class ReadSectorComplete(ReadSector):
    """Modelo para leer un sector con todos sus datos incluidos las formaciones, experiencias y trabajos que tienen ese sector.

        Atributos:
            id: Identificador del sector
            category: La categoría del sector
            subcategory: La subcategoría del sector
            education_list: Lista de formaciones que pertenecen al sector
            experience_list: Lista de experiencias que pertenecen al sector
            job_list: Lista de trabajos que pertenecen al sector
    """
    
    education_list: Optional[list[ReadSectorRelationEducation]] = Field(description=SectorDescription.EDUCATIONS, default=[])
    experience_list: Optional[list[ReadExperience]] = Field(description=SectorDescription.EXPERIENCES, default=[])
    job_list: Optional[list[ReadJob]] = Field(description=SectorDescription.JOBS, default=[])

    

class ReadExperienceComplete(ReadExperience):
    """Modelo para leer una experiencia con todos sus datos incluidos el sector al que pertenece.
        Los atributos de las relaciones son opcionales para mostrar solo los datos que se necesiten.

        Atributos:
            id: Identificador de la experiencia
            company_name: Nombre de la empresa
            position: Puesto de trabajo
            position_description: Descripcion del puesto de trabajo
            start_date: Fecha de inicio
            end_date: Fecha de finalizacion
            sector: Sector de la experiencia"""
    
    sector: Optional[ReadSector] = Field(description=ExperienceDescription.SECTOR, default=None)

class ReadEducationComplete(ReadEducation):
    """
    Modelo para leer una formacion con todos sus datos incluidos el sector y el nivel de formacion.
    Puede no tener sector.

    Atributos:
        id: Identificador de la formacion
        qualification: Titulo de la formacion
        level: Nivel de la formacion
        sector: Sector de la formacion
    """
    
    level: ReadLevel = Field(description=EducationDescription.LEVEL)
    sector: Optional[ReadEducationRelationSector] = Field(description=EducationDescription.SECTOR, default=None)

class ReadEducationCompleteWithCandidates(ReadEducationComplete):
    """
    Modelo para leer una formacion con todos sus datos incluidos los candidatos que tienen esa formacion.

    Atributos:
        id: Identificador de la formacion
        qualification: Titulo de la formacion
        level: Nivel de la formacion
        sector: Sector de la formacion
        candidates_list: Lista de candidatos con esa formacion
    """
    
    candidates_list: list[ReadEducationRelationCandidate] = Field(description=EducationDescription.CANDIDATES, default=[])

class ReadLevelLanguage(ReadLevel):
    """Modelo para leer un nivel con todos sus datos incluidos los idiomas que tienen ese nivel.
        Los atributos de las relaciones son opcionales para mostrar solo los datos que se necesiten.

        Atributos:
            id: Identificador del nivel
            name: Nombre del nivel de formacion o idioma
            value: Valor numerico del nivel de formacion o idioma
            candidates: Lista de candidatos con ese nivel de idioma
            jobs: Lista de trabajos que requieren ese nivel de idioma"""
    
    candidates: Optional[list[ReadLevelLanguageRelationsCandidate]] = Field(description=LanguageLevelDescription.CANDIDATES, default=[])
    jobs: Optional[list[ReadLevelLanguageRelationsJob]] = Field(description=LanguageLevelDescription.JOBS, default=[])

class ReadLevelEducation(ReadLevel):
    """Modelo para leer un nivel con todos sus datos incluidos las formaciones que tienen ese nivel.
        Los atributos de las relaciones son opcionales para mostrar solo los datos que se necesiten.

        Atributos:
            id: Identificador del nivel
            name: Nombre del nivel de formacion o idioma
            value: Valor numerico del nivel de formacion o idioma
            educations: Lista de formaciones con ese nivel"""
    
    education_list: Optional[list[ReadEducation]] = Field(description=EducationLevelDescription.EDUCATION, default=[])
    jobs_list: Optional[list[ReadJob]] = Field(description=EducationLevelDescription.JOB, default=[])


class ReadAdressComplete(ReadAdress):
    """Modelo para leer una direccion con todos sus datos incluidos los usuarios y trabajos que tienen esa direccion.
        Los atributos de las relaciones son opcionales para mostrar solo los datos que se necesiten.

        Atributos:
            postal_code: Codigo postal
            street: Calle de la direccion
            city: Ciudad de la direccion
            province: Provincia de la direccion"""
    
    users_list: Optional[list[ReadUser]] = Field(description=AdressDescription.USERS, default=[])
    jobs_list: Optional[list[ReadJob]] = Field(description=AdressDescription.JOB, default=[])

class ReadJobComplete(ReadJob):
    """Modelo para leer una oferta con todos sus datos incluidos la empresa, el sector, la direccion, el nivel de formacion requerido y los idiomas requeridos.
        Los atributos de las relaciones son opcionales para mostrar solo los datos que se necesiten.

        Atributos:
            id: Identificador de la oferta
            title: Titulo de la oferta
            description: Descripcion de la oferta
            skills: Lista de habilidades de la oferta
            required_experience_months: Experiencia requerida para la oferta
            active: Estado de la oferta (abierta o cerrada)
            publication_date: Fecha de publicacion de la oferta
            company: Empresa a la que pertenece la oferta
            required_education_level: Nivel de formacion requerido para la oferta
            sector: Sector al que pertenece la oferta
            adress: Direccion de la oferta
            languages: Lista de idiomas requeridos por la oferta
            candidates: Lista con candidatos inscritos en la oferta"""

    
    company: Optional[ReadCompany] = Field(description=JobDescription.COMPANY, default=None)
    sector: Optional[ReadSector] = Field(description=JobDescription.SECTOR, default=None)
    adress: Optional[ReadAdress] = Field(description=JobDescription.ADRESS, default=None)
    required_education_level: Optional[ReadLevel] = Field(description=JobDescription.REQUIRED_EDUCATION_LEVEL, default=None)
    languages: Optional[list[ReadJobRelationLanguage]] = Field(description=JobDescription.LANGUAGES, default=[])
    candidates: Optional[list[ReadJobRelationCandidate]] = Field(description=JobDescription.CANDIDATES, default=[])