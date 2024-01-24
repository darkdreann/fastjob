from fastapi import status
from api.database.database_models.metadata.constraint_name import *

# clave para la excepción de null
_NULL_IN_RELATION_ERROR = "null value in column of relation violates not-null constraint"

PARAMS_EXCEPTION = {
    "status_code": status.HTTP_400_BAD_REQUEST,
    "detail": "Parámetros inválidos."
}

INCORRECT_RESOURCE_EXCEPTION = {
    "status_code": status.HTTP_400_BAD_REQUEST,
    "detail": "El tipo de recurso no es válido para este endpoint."
}

CREDENTIALS_EXCEPTION = {
    "status_code": status.HTTP_401_UNAUTHORIZED,
    "headers": {"WWW-Authenticate": "Bearer"},
    "detail": "No se pudo validar el usuario."
}

FORBIDDEN_EXCEPTION = {
    "status_code": status.HTTP_403_FORBIDDEN,
    "headers": {"WWW-Authenticate": "Bearer"},
    "detail": "Permiso denegado."
}

RESOURCE_NOT_FOUND_EXCEPTION = {
    "status_code": status.HTTP_404_NOT_FOUND,
    "detail": "Recurso no encontrado."
}

INTEGRATION_EXCEPTION = {
    JobCandidateConstraint.JOB_CANDIDATE_PK: {"status_code": status.HTTP_409_CONFLICT, "detail": "La clave primaria de Job_candidate ya existe."},
    JobCandidateConstraint.CANDIDATE_FK: {"status_code": status.HTTP_409_CONFLICT, "detail": "Se produjo un problema con la clave externa de candidate."},
    JobCandidateConstraint.JOB_FK: {"status_code": status.HTTP_409_CONFLICT, "detail": "Se produjo un problema con la clave externa de job."},

    SectorEducationConstraint.SECTOR_EDUCATION_PK: {"status_code": status.HTTP_409_CONFLICT, "detail": "La clave primaria de Sector_education ya existe."},
    SectorEducationConstraint.SECTOR_FK: {"status_code": status.HTTP_409_CONFLICT, "detail": "Se produjo un problema con la clave externa de sector."},
    SectorEducationConstraint.EDUCATION_FK: {"status_code": status.HTTP_409_CONFLICT, "detail": "Se produjo un problema con la clave externa de education."},
    SectorEducationConstraint.DUPLICATE_EDUCATION_ID: {"status_code": status.HTTP_409_CONFLICT, "detail": "La educación solo puede tener un sector."},

    CandidateEducationConstraint.CANDIDATE_EDUCATION_PK: {"status_code": status.HTTP_409_CONFLICT, "detail": "La clave primaria de Candidate_education ya existe."},
    CandidateEducationConstraint.CANDIDATE_FK: {"status_code": status.HTTP_409_CONFLICT, "detail": "Se produjo un problema con la clave externa de candidate."},
    CandidateEducationConstraint.EDUCATION_FK: {"status_code": status.HTTP_409_CONFLICT, "detail": "Se produjo un problema con la clave externa de education."},

    CandidateLanguageConstraint.CANDIDATE_LANGUAGE_PK: {"status_code": status.HTTP_409_CONFLICT, "detail": "La clave primaria de Candidate_language ya existe."},
    CandidateLanguageConstraint.CANDIDATE_FK: {"status_code": status.HTTP_409_CONFLICT, "detail": "Se produjo un problema con la clave externa de candidate."},
    CandidateLanguageConstraint.LANGUAGE_FK: {"status_code": status.HTTP_409_CONFLICT, "detail": "Se produjo un problema con la clave externa de language."},
    CandidateLanguageConstraint.LANGUAGE_LEVEL_FK: {"status_code": status.HTTP_409_CONFLICT, "detail": "Se produjo un problema con la clave externa de language_level."},

    JobLanguageConstraint.JOB_LANGUAGE_PK: {"status_code": status.HTTP_409_CONFLICT, "detail": "La clave primaria de Job_language ya existe."},
    JobLanguageConstraint.JOB_FK: {"status_code": status.HTTP_409_CONFLICT, "detail": "Se produjo un problema con la clave externa de job."},
    JobLanguageConstraint.LANGUAGE_FK: {"status_code": status.HTTP_409_CONFLICT, "detail": "Se produjo un problema con la clave externa de language."},
    JobLanguageConstraint.LANGUAGE_LEVEL_FK: {"status_code": status.HTTP_409_CONFLICT, "detail": "Se produjo un problema con la clave externa de language_level."},

    UserConstraint.USER_PK: {"status_code": status.HTTP_409_CONFLICT, "detail": "La clave primaria de User ya existe."},
    UserConstraint.DUPLICATE_USERNAME: {"status_code": status.HTTP_409_CONFLICT, "detail": "El nombre de usuario ya existe."},
    UserConstraint.DUPLICATE_EMAIL: {"status_code": status.HTTP_409_CONFLICT, "detail": "El email ya existe."},
    UserConstraint.ADMIN_HAS_TABLE: {"status_code": status.HTTP_409_CONFLICT, "detail": "El usuario administrador no puede tener una tabla de candidato o empresa."},
    UserConstraint.CANDIDATE_HAS_COMPANY_TABLE: {"status_code": status.HTTP_409_CONFLICT, "detail": "El usuario de empresa no puede tener una tabla de candidato."},
    UserConstraint.COMPANY_HAS_CANDIDATE_TABLE: {"status_code": status.HTTP_409_CONFLICT, "detail": "El usuario de candidato no puede tener una tabla de empresa."},
    UserConstraint.ADDRESS_FK: {"status_code": status.HTTP_409_CONFLICT, "detail": "Se produjo un problema con la clave externa de address."},

    CandidateConstraint.CANDIDATE_PK: {"status_code": status.HTTP_409_CONFLICT, "detail": "La clave primaria de Candidate ya existe."},
    CandidateConstraint.USER_NOT_CANDIDATE: {"status_code": status.HTTP_409_CONFLICT, "detail": "El usuario no es un candidato."},
    CandidateConstraint.USER_FK: {"status_code": status.HTTP_409_CONFLICT, "detail": "Se produjo un problema con la clave externa de user."},

    CompanyConstraint.COMPANY_PK: {"status_code": status.HTTP_409_CONFLICT, "detail": "La clave primaria de Company ya existe."},
    CompanyConstraint.USER_NOT_COMPANY: {"status_code": status.HTTP_409_CONFLICT, "detail": "El usuario no es una empresa."},
    CompanyConstraint.DUPLICATE_TIN: {"status_code": status.HTTP_409_CONFLICT, "detail": "El NIF ya existe."},
    CompanyConstraint.DUPLICATE_COMPANY_NAME: {"status_code": status.HTTP_409_CONFLICT, "detail": "El nombre de la empresa ya existe."},
    CompanyConstraint.USER_FK: {"status_code": status.HTTP_409_CONFLICT, "detail": "Se produjo un problema con la clave externa de user."},

    LanguageConstraint.LANGUAGE_PK: {"status_code": status.HTTP_409_CONFLICT, "detail": "La clave primaria de Language ya existe."},
    LanguageConstraint.DUPLICATE_LANGUAGE_NAME: {"status_code": status.HTTP_409_CONFLICT, "detail": "El nombre del idioma ya existe."},

    SectorConstraint.SECTOR_PK: {"status_code": status.HTTP_409_CONFLICT, "detail": "La clave primaria de Sector ya existe."},
    SectorConstraint.DUPLICATE_CATEGORY_SUBCATEGORY: {"status_code": status.HTTP_409_CONFLICT, "detail": "El sector ya existe."},

    ExperienceConstraint.EXPERIENCE_PK: {"status_code": status.HTTP_409_CONFLICT, "detail": "La clave primaria de Experience ya existe."},
    ExperienceConstraint.CANDIDATE_FK: {"status_code": status.HTTP_409_CONFLICT, "detail": "Se produjo un problema con la clave externa de candidate."},
    ExperienceConstraint.SECTOR_FK: {"status_code": status.HTTP_409_CONFLICT, "detail": "Se produjo un problema con la clave externa de sector."},

    EducationConstraint.EDUCATION_PK: {"status_code": status.HTTP_409_CONFLICT, "detail": "La clave primaria de Education ya existe."},
    EducationConstraint.DUPLICATE_QUALIFICATION: {"status_code": status.HTTP_409_CONFLICT, "detail": "La calificación de la educación ya existe."},
    EducationConstraint.LEVEL_FK: {"status_code": status.HTTP_409_CONFLICT, "detail": "Se produjo un problema con la clave externa de education_level."},

    EducationLevelConstraint.EDUCATION_LEVEL_PK: {"status_code": status.HTTP_409_CONFLICT, "detail": "La clave primaria de Education_level ya existe."},
    EducationLevelConstraint.DUPLICATE_VALUE: {"status_code": status.HTTP_409_CONFLICT, "detail": "El valor de education_level ya existe."},
    EducationLevelConstraint.DUPLICATE_NAME: {"status_code": status.HTTP_409_CONFLICT, "detail": "El nombre de education_level ya existe."},

    LanguageLevelConstraint.LANGUAGE_LEVEL_PK: {"status_code": status.HTTP_409_CONFLICT, "detail": "La clave primaria de Language_level ya existe."},
    LanguageLevelConstraint.DUPLICATE_VALUE: {"status_code": status.HTTP_409_CONFLICT, "detail": "El valor de language_level ya existe."},
    LanguageLevelConstraint.DUPLICATE_NAME: {"status_code": status.HTTP_409_CONFLICT, "detail": "El nombre de language_level ya existe."},

    AddressConstraint.ADDRESS_PK: {"status_code": status.HTTP_409_CONFLICT, "detail": "La clave primaria de Address ya existe."},
    AddressConstraint.DUPLICATE_ADDRESS: {"status_code": status.HTTP_409_CONFLICT, "detail": "La dirección ya existe."},
    AddressConstraint.DUPLICATE_POSTAL_CODE: {"status_code": status.HTTP_409_CONFLICT, "detail": "El código postal ya existe."},

    JobConstraint.JOB_PK: {"status_code": status.HTTP_409_CONFLICT, "detail": "La clave primaria de Job ya existe."},
    JobConstraint.COMPANY_FK: {"status_code": status.HTTP_409_CONFLICT, "detail": "Se produjo un problema con la clave externa de company."},
    JobConstraint.SECTOR_FK: {"status_code": status.HTTP_409_CONFLICT, "detail": "Se produjo un problema con la clave externa de sector."},
    JobConstraint.ADDRESS_FK: {"status_code": status.HTTP_409_CONFLICT, "detail": "Se produjo un problema con la clave externa de address."},
    JobConstraint.LEVEL_EDUCATION_FK: {"status_code": status.HTTP_409_CONFLICT, "detail": "Se produjo un problema con la clave externa de education_level."},

    _NULL_IN_RELATION_ERROR: {"status_code": status.HTTP_409_CONFLICT, "detail": "La columna no puede ser nula."}
}

DEFAULT_EXCEPTION = {
    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
    "detail": "Ha ocurrido algo inesperado en el servidor, por favor contacta al administrador del sistema."
}
