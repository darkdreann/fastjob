# pendiente si descripcion separada por cada clase o dejarla con el diccionario
DESCRIPTIONS_ID =  {
    "ADDRESS_ID": "El id de la dirección.",
    "USER_ID": "El id del usuario.",
    "LANGUAGE_ID": "El id del idioma.",
    "SECTOR_ID" : "El id del sector.",
    "EXPERIENCE_ID" : "El id de la experiencia.",
    "EDUCATION_ID" : "El id de formación.",
    "LEVEL_ID" : "El id del nivel.",
    "COMPANY_ID" : "El id de la empresa.",
    "JOB_ID" : "El id de la oferta de trabajo.",
    "CANDIDATE_ID" : "El id del candidato."
}

#-------------------USER----------------------------
class UserDescriptions:
    USER_ID = DESCRIPTIONS_ID["USER_ID"]
    USERNAME = "El username del usuario."
    EMAIL = "El email del usuario."
    NAME = "El nombre del usuario."
    SURNAME = "El apellido del usuario."
    PHONE_NUMBER = "Lista con los números de teléfonos del usuario."
    PASSWORD = "La contraseña del usuario."
    ADDRESS = "La dirección del usuario."
    USER_TYPE = "El tipo de usuario."

#-------------------CANDIDATE----------------------------
class CandidateDescription:
    SKILLS = "Las habilidades de un candidato."
    AVAILABILITY = "Las jornadas de trabajo que puede aceptar el usuario."
    USER = "La información de usuario del candidato."
    EXPERIENCE = "Lista con las experiencias laborales del candidato."
    EDUCATION = "Lista con las formaciones del candidato."
    LANGUAGE = "Lista con los idiomas del candidato."
    JOBS = "Lista con las ofertas de trabajo aplicadas del candidato."
    CREATE_CANDIDATE = "Información adicional del candidato."

#-------------------COMPANY----------------------------
class CompanyDescription:
    TIN = "El cif de la empresa."
    COMPANY_NAME = "El nombre de la empresa."
    USER = "La información de usuario de la empresa."
    JOB = "Lista con las ofertas de trabajo creadas de la empresa."

#-------------------LANGUAGE----------------------------
class LanguageDescription:
    NAME = "El nombre del idioma."
    LANGUAGE_ID = DESCRIPTIONS_ID["LANGUAGE_ID"]
    CANDIDATE = "Lista con los candidatos con el idioma."
    JOB = "Lista con las ofertas de trabajo con el idioma."

#-------------------SECTOR---------------------------------
class SectorDescription:
    CATEGORY = "La categoría del sector."
    SUBCATEGORY = "La subcategoría del sector."
    SECTOR_ID = DESCRIPTIONS_ID["SECTOR_ID"]
    EXPERIENCES = "Lista con las experiencias laborales del sector."
    EDUCATIONS = "Lista con las formaciones del sector."
    JOBS = "Lista con las ofertas de trabajo del sector."

#-------------------EXPERIENCE---------------------------------
class ExperienceDescription:
    COMPANY_NAME = "El nombre de la empresa donde ha trabajado."
    START_DATE = "Fecha cuando empezó a trabajar en la empresa."
    END_DATE = "Fecha cuando termino el trabajo. Puede ser None si el candidato sigue trabajando."
    POSITION = "El puesto de trabajo en la empresa."
    POSITION_DESC = "La descripción del puesto de trabajo."
    EXPERIENCE_ID = DESCRIPTIONS_ID["EXPERIENCE_ID"]
    SECTOR_ID = DESCRIPTIONS_ID["SECTOR_ID"]
    SECTOR = "El sector de la experiencia laboral."
    CANDIDATE = "El candidato al que pertenece la experiencia laboral."  

#-------------------EDUCATION---------------------------------
class EducationDescription:
    QUALIFICATION = "El nombre del titulo de la formación."
    EDUCATION_ID = DESCRIPTIONS_ID["EDUCATION_ID"]
    LEVEL = "El nivel de la formación."
    SECTOR = "El sector que pertenece la formación. Puede no tener sector."
    CANDIDATES = "Los candidatos que tienen la formación."
    JOB = "Lista de ofertas que requieren la formación."
    LEVEL_ID = DESCRIPTIONS_ID["LEVEL_ID"]
    SECTOR_ID = DESCRIPTIONS_ID["SECTOR_ID"]

#-------------------LEVEL--------------------------------------
class LevelDescription:
    VALUE = "Valor númerico del nivel de la formación o idioma."
    NAME = "El nombre del nivel de la formación o idioma."
    LEVEL_ID = DESCRIPTIONS_ID["LEVEL_ID"]

class EducationLevelDescription:
    EDUCATION = "Lista de formaciones pertenecientes al nivel."

class LanguageLevelDescription:
    CANDIDATES = "Lista de candidatos con ese nivel de idioma"
    JOBS = "Lista de ofertas que requieren el nivel de idioma"

#-------------------ADDRESS--------------------------------------

class AddressDescription:
    POSTAL_CODE = "Código postal de la dirección. Es un número de 5 digitos."
    STREET = "Nombre de la calle de la dirección."
    CITY = "Ciudad a la que pertenece la dirección."
    PROVINCE = "Provincia a la que pertenece la dirección."
    USERS = "Lista de usuarios en la dirección"
    JOB = "Lista de ofertas en la dirección"
    ID = DESCRIPTIONS_ID["ADDRESS_ID"]

#-------------------JOB--------------------------------------
class JobDescription:
    TITLE = "El titulo de la oferta."
    REQUIRED_EXP = "La experiencia requerida en el sector en meses."
    WORK_SCHEDULE = "La jornada requerida en la oferta."
    DESC = "La descripción de la oferta."
    SKILLS = "Lista de habilidades requeridas para la oferta."
    ACTIVE = "Si la oferta esta cerrada o abierta."
    COMPANY_ID = DESCRIPTIONS_ID["COMPANY_ID"]
    REQUIRED_EDUCATION_ID = DESCRIPTIONS_ID["EDUCATION_ID"]
    SECTOR_ID = DESCRIPTIONS_ID["SECTOR_ID"]
    ADDRESS = "La dirección de la oferta."
    JOB_ID = DESCRIPTIONS_ID["JOB_ID"]
    PUBLICATION_DATE = "Fecha de publicación de la oferta."
    COMPANY = "Empresa a la que pertenece la oferta."
    REQUIRED_EDUCATION = "La formación requerida por la oferta."
    SECTOR = "El sector al que pertenece la oferta."
    LANGUAGES = "Lista de idiomas requeridos por la oferta."
    CANDIDATES = "Lista con candidatos inscritos en la oferta."

######################  LINKS  ######################
#-------------------JOB CANDIDATE----------------------------
class JobCandidateDescriptions:
    CANDIDATE_ID = DESCRIPTIONS_ID["CANDIDATE_ID"]
    JOB_ID = DESCRIPTIONS_ID["JOB_ID"]
   
#-------------------Education Sector----------------------------
class EducationSectorDescriptions:
    EDUCATION_ID = DESCRIPTIONS_ID["EDUCATION_ID"]
    SECTOR_ID = DESCRIPTIONS_ID["SECTOR_ID"]

#-------------------Education Candidate----------------------------
class EducationCandidateDescriptions:
    COMPLETION_DATE = "Fecha de finalización de la formación"
    EDUCATION_ID = DESCRIPTIONS_ID["EDUCATION_ID"]
    CANDIDATE_ID = DESCRIPTIONS_ID["CANDIDATE_ID"]
    EDUCATION = "Formación del usuario."
    CANDIDATE = "El candidato con la formación."

#-------------------CANDIDATE LANGUAGE----------------------------
class CandidateLanguageDescriptions:
    LEVEL_ID = DESCRIPTIONS_ID["LEVEL_ID"]
    CANDIDATE_ID = DESCRIPTIONS_ID["CANDIDATE_ID"]
    LANGUAGE_ID = DESCRIPTIONS_ID["LANGUAGE_ID"]
    LANGUAGE_LEVEL = "El nivel del idioma."
    LANGUAGE = "El idioma del usuario."
    CANDIDATE = "El candidato con la formación."

#-------------------JOB LANGUAGE----------------------------
class JobLanguageDescriptions:
    JOB_ID = DESCRIPTIONS_ID["JOB_ID"]
    LANGUAGE_ID = DESCRIPTIONS_ID["LANGUAGE_ID"]
    LEVEL_ID = DESCRIPTIONS_ID["LEVEL_ID"]
    LEVEL = "El nivel del idioma requerido por la oferta."
    LANGUAGE = "El idioma requerido por la oferta."
    JOB = "La oferta que requiere este idioma."

#-------------------JOB CANDIDATE----------------------------
class CandidateJobDescriptions:
    CANDIDATE = "El candidato que se ha inscrito en la oferta."
    JOB = "La oferta en la que se ha inscrito el candidato."
    INCRIPTION_DATE = "La fecha de inscripción del candidato en la oferta."

#-------------------EDUCATION SECTOR----------------------------
class SectorEducationDescriptions:
    SECTOR = "El sector al que pertenece la formación."
    EDUCATION = "La formación que pertenece al sector."