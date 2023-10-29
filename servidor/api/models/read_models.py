from api.models.enums import UserType
from typing import Optional
from api.models.base_models import *
from uuid import UUID

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

class ReadLanguage(BaseLanguage):
    """Modelo para leer un idioma

        Atributos:
            id: Identificador del idioma
            name: Nombre del idioma"""
    
    id: UUID = Field(description=LanguageDescription.LANGUAGE_ID)

class ReadSector(BaseSector):
    """Modelo para leer un sector

        Atributos:
            id: Identificador del sector
            category: La categoría del sector
            subcategory: La subcategoría del sector"""
    
    id: UUID = Field(description=SectorDescription.SECTOR_ID)

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
class ReadCandidateJob(BaseModel):
    """Modelo para leer un candidato con un trabajo

        Atributos:
            candidate: Candidato con el trabajo
            job: Trabajo del candidato
            compatibility: Compatibilidad del candidato con el trabajo"""

    candidate: Optional[ReadCandidate] = Field(description=CandidateJobDescriptions.CANDIDATE, default=None)
    job: Optional[ReadJob] = Field(description=CandidateJobDescriptions.JOB, default=None)
    compatibility: float = Field(description=CandidateJobDescriptions.COMPATIBILITY)


class ReadCandidateLanguage(BaseModel):
    """Modelo para leer un candidato con un idioma

        Atributos:
            candidate: Candidato con el idioma
            language: Idioma del candidato
            level: Nivel del idioma del candidato"""

    candidate: Optional[ReadCandidate] = Field(description=CandidateLanguageDescriptions.CANDIDATE, default=None)
    language: Optional[ReadLanguage] = Field(description=CandidateLanguageDescriptions.LANGUAGE, default=None)
    level: ReadLevel = Field(description=CandidateLanguageDescriptions.LANGUAGE_LEVEL)

class ReadCandidateEducation(BaseModel):
    """Modelo para leer un candidato con una formacion

        Atributos:
            candidate: Candidato con la formacion
            education: Formacion del candidato
            completion_date: Fecha de finalizacion de la formacion"""

    candidate: Optional[ReadCandidate] = Field(description=EducationCandidateDescriptions.CANDIDATE, default=None)
    education: Optional[ReadEducation] = Field(description=EducationCandidateDescriptions.EDUCATION, default=None)
    completion_date: date = Field(description=EducationCandidateDescriptions.COMPLETION_DATE)

class ReadJobLanguage(BaseModel):
    """Modelo para leer una oferta con un idioma

        Atributos:
            job: Oferta con el idioma
            language: Idioma de la oferta
            level: Nivel del idioma de la oferta"""

    job: Optional[ReadJob] = Field(description=JobLanguageDescriptions.JOB, default=None)
    language: Optional[ReadLanguage] = Field(description=JobLanguageDescriptions.LANGUAGE, default=None)
    level: ReadLevel = Field(description=JobLanguageDescriptions.LEVEL)



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

    experiences: Optional[list[ReadExperience]] = Field(description=CandidateDescription.EXPERIENCE, default=None)
    education: Optional[list[ReadCandidateEducation]] = Field(description=CandidateDescription.EDUCATION, default=None)
    languages: Optional[list[ReadCandidateLanguage]] = Field(description=CandidateDescription.LANGUAGE, default=None)
    applied_jobs: Optional[list[ReadCandidateJob]] = Field(description=CandidateDescription.JOBS, default=None)

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
    
    jobs: Optional[list[ReadJob]] = Field(description=CompanyDescription.JOB, default=None)


class ReadLanguageComplete(ReadLanguage):
    """Modelo para leer un idioma con todos sus datos incluidos los usuarios que tienen ese idioma.
        Los atributos de las relaciones son opcionales para mostrar solo los datos que se necesiten.

        Atributos:
            name: Nombre del idioma
            jobs: Lista de trabajos que requieren ese idioma
            candidates: Lista de candidatos que tienen ese idioma"""
    
    candidates: Optional[list[ReadCandidateLanguage]] = Field(description=LanguageDescription.CANDIDATE, default=None)
    jobs: Optional[list[ReadJobLanguage]] = Field(description=LanguageDescription.JOB, default=None)

class ReadSectorComplete(ReadSector):
    """Modelo para leer un sector con todos sus datos incluidos las experiencias que tienen ese sector.
        Los atributos de las relaciones son opcionales para mostrar solo los datos que se necesiten.

        Atributos:
            id: Identificador del sector
            category: La categoría del sector
            subcategory: La subcategoría del sector
            experiences: Lista de experiencias del sector"""
    
    experiences: Optional[list[ReadExperience]] = Field(description=SectorDescription.EXPERIENCES)
    educations: Optional[list[ReadEducation]] = Field(description=SectorDescription.EDUCATIONS)
    jobs: Optional[list[ReadJob]] = Field(description=SectorDescription.JOBS)

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
    """Modelo para leer una formacion con todos sus datos incluidos el sector al que pertenece.
        Los atributos de las relaciones son opcionales para mostrar solo los datos que se necesiten.

        Atributos:
            id: Identificador de la formacion
            qualification: Titulo de la formacion
            level: Nivel de la formacion
            sector: Sector de la formacion
            candidates: Lista de candidatos con esa formacion"""
    
    level: Optional[ReadLevel] = Field(description=EducationDescription.LEVEL, default=None)
    sector: Optional[ReadSector] = Field(description=EducationDescription.SECTOR, default=None)
    candidates: Optional[list[ReadCandidateEducation]] = Field(description=EducationDescription.CANDIDATES, default=None)

class ReadLevelLanguage(ReadLevel):
    """Modelo para leer un nivel con todos sus datos incluidos los idiomas que tienen ese nivel.
        Los atributos de las relaciones son opcionales para mostrar solo los datos que se necesiten.

        Atributos:
            id: Identificador del nivel
            name: Nombre del nivel de formacion o idioma
            value: Valor numerico del nivel de formacion o idioma
            candidates: Lista de candidatos con ese nivel de idioma
            jobs: Lista de trabajos que requieren ese nivel de idioma"""
    
    candidates: Optional[list[ReadCandidateLanguage]] = Field(description=LanguageLevelDescription.CANDIDATES, default=None)
    jobs: Optional[list[ReadJobLanguage]] = Field(description=LanguageLevelDescription.JOBS, default=None)

class ReadLevelEducation(ReadLevel):
    """Modelo para leer un nivel con todos sus datos incluidos las formaciones que tienen ese nivel.
        Los atributos de las relaciones son opcionales para mostrar solo los datos que se necesiten.

        Atributos:
            id: Identificador del nivel
            name: Nombre del nivel de formacion o idioma
            value: Valor numerico del nivel de formacion o idioma
            educations: Lista de formaciones con ese nivel"""
    
    educations: Optional[list[ReadEducation]] = Field(description=EducationLevelDescription.EDUCATION, default=None)
    job: Optional[list[ReadJob]] = Field(description=EducationLevelDescription.JOB, default=None)


class ReadAdressComplete(ReadAdress):
    """Modelo para leer una direccion con todos sus datos incluidos los usuarios y trabajos que tienen esa direccion.
        Los atributos de las relaciones son opcionales para mostrar solo los datos que se necesiten.

        Atributos:
            postal_code: Codigo postal
            street: Calle de la direccion
            city: Ciudad de la direccion
            province: Provincia de la direccion"""
    
    users: Optional[list[ReadUser]] = Field(description=AdressDescription.USERS, default=None)
    jobs: Optional[list[ReadJob]] = Field(description=AdressDescription.JOB, default=None)

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
    languages: Optional[list[ReadJobLanguage]] = Field(description=JobDescription.LANGUAGES, default=None)
    candidates: Optional[list[ReadCandidateJob]] = Field(description=JobDescription.CANDIDATES, default=None)