from fastapi import status
from api.database.database_models.metadata.constraint_name import *

# constantes para las excepciones de integridad
_DEFAULT_ERROR_MESSAGE = "Something unexpected has happened on the server, please contact the system administrator."
_NULL_IN_RELATION_ERROR = "null value in column of relation violates not-null constraint"


# constantes para las excepciones
CREDENTIALS_EXCEPTION = {
    "status_code":status.HTTP_401_UNAUTHORIZED,
    "headers":{"WWW-Authenticate": "Bearer"},
    "detail":"Could not validate user.",
}

FORBIDDEN_EXCEPTION = {
    "status_code":status.HTTP_403_FORBIDDEN,
    "headers":{"WWW-Authenticate": "Bearer"},
    "detail":"Permission denied."
}

USER_NOT_FOUND_EXCEPTION = {
    "status_code":status.HTTP_404_NOT_FOUND,
    "detail":"User not found."
}


INTEGRATION_EXCEPTION = {
    JobCandidateConstraint.JOB_CANDIDATE_PK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Job_candidate primary key already exists."},
    JobCandidateConstraint.CANDIDATE_FK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Problem occurred with the candidate foreign key."},
    JobCandidateConstraint.JOB_FK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Problem occurred with the job foreign key."},

    SectorEducationConstraint.SECTOR_EDUCATION_PK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Sector_education primary key already exists."},
    SectorEducationConstraint.SECTOR_FK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Problem occurred with the sector foreign key."},
    SectorEducationConstraint.EDUCATION_FK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Problem occurred with the education foreign key."},

    CandidateEducationConstraint.CANDIDATE_EDUCATION_PK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Candidate_education primary key already exists."},
    CandidateEducationConstraint.CANDIDATE_FK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Problem occurred with the candidate foreign key."},
    CandidateEducationConstraint.EDUCATION_FK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Problem occurred with the education foreign key."},

    CandidateLanguageConstraint.CANDIDATE_LANGUAGE_PK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Candidate_language primary key already exists."},
    CandidateLanguageConstraint.CANDIDATE_FK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Problem occurred with the candidate foreign key."},
    CandidateLanguageConstraint.LANGUAGE_FK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Problem occurred with the language foreign key."},
    CandidateLanguageConstraint.LANGUAGE_LEVEL_FK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Problem occurred with the language_level foreign key."},

    JobLanguageConstraint.JOB_LANGUAGE_PK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Job_language primary key already exists."},
    JobLanguageConstraint.JOB_FK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Problem occurred with the job foreign key."},
    JobLanguageConstraint.LANGUAGE_FK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Problem occurred with the language foreign key."},
    JobLanguageConstraint.LANGUAGE_LEVEL_FK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Problem occurred with the language_level foreign key."},

    UserConstraint.USER_PK: {"status_code":status.HTTP_409_CONFLICT, "detail":"User primary key already exists."},
    UserConstraint.DUPLICATE_USERNAME: {"status_code":status.HTTP_409_CONFLICT, "detail":"Username already exists."},
    UserConstraint.DUPLICATE_EMAIL: {"status_code":status.HTTP_409_CONFLICT, "detail":"Email already exists."},
    UserConstraint.ADMIN_HAS_TABLE: {"status_code":status.HTTP_409_CONFLICT, "detail":"Admin user cannot have a candidate or company table."},
    UserConstraint.CANDIDATE_HAS_COMPANY_TABLE: {"status_code":status.HTTP_409_CONFLICT, "detail":"Company user cannot have a candidate table."},
    UserConstraint.COMPANY_HAS_CANDIDATE_TABLE: {"status_code":status.HTTP_409_CONFLICT, "detail":"Candidate user cannot have a company table."},
    UserConstraint.ADRESS_FK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Problem occurred with the adress foreign key."},

    CandidateConstraint.CANDIDATE_PK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Candidate primary key already exists."},
    CandidateConstraint.USER_NOT_CANDIDATE: {"status_code":status.HTTP_409_CONFLICT, "detail":"User is not a candidate."},
    CandidateConstraint.USER_FK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Problem occurred with the user foreign key."},

    CompanyConstraint.COMPANY_PK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Company primary key already exists."},
    CompanyConstraint.USER_NOT_COMPANY: {"status_code":status.HTTP_409_CONFLICT, "detail":"User is not a company."},
    CompanyConstraint.DUPLICATE_TIN: {"status_code":status.HTTP_409_CONFLICT, "detail":"TIN already exists."},
    CompanyConstraint.DUPLICATE_COMPANY_NAME: {"status_code":status.HTTP_409_CONFLICT, "detail":"Company name already exists."},
    CompanyConstraint.USER_FK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Problem occurred with the user foreign key."},

    LanguageConstraint.LANGUAGE_PK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Language primary key already exists."},
    LanguageConstraint.DUPLICATE_LANGUAGE_NAME: {"status_code":status.HTTP_409_CONFLICT, "detail":"Language name already exists."},

    SectorConstraint.SECTOR_PK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Sector primary key already exists."},
    SectorConstraint.DUPLICATE_CATEGORY_SUBCATEGORY: {"status_code":status.HTTP_409_CONFLICT, "detail":"Sector already exists."},

    ExperienceConstraint.EXPERIENCE_PK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Experience primary key already exists."},
    ExperienceConstraint.CANDIDATE_FK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Problem occurred with the candidate foreign key."},
    ExperienceConstraint.SECTOR_FK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Problem occurred with the sector foreign key."},

    EducationConstraint.EDUCATION_PK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Education primary key already exists."},
    EducationConstraint.DUPLICATE_QUALIFICATION: {"status_code":status.HTTP_409_CONFLICT, "detail":"Education qualification already exists"},
    EducationConstraint.LEVEL_FK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Problem occurred with the education_level foreign key."},

    EducationLevelConstraint.EDUCATION_LEVEL_PK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Education_level primary key already exists."},
    EducationLevelConstraint.DUPLICATE_VALUE: {"status_code":status.HTTP_409_CONFLICT, "detail":"Education_level value already exists."},
    EducationLevelConstraint.DUPLICATE_NAME: {"status_code":status.HTTP_409_CONFLICT, "detail":"Education_level name already exists."},

    LanguageLevelConstraint.LANGUAGE_LEVEL_PK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Language_level primary key already exists."},
    LanguageLevelConstraint.DUPLICATE_VALUE: {"status_code":status.HTTP_409_CONFLICT, "detail":"Language_level value already exists."},
    LanguageLevelConstraint.DUPLICATE_NAME: {"status_code":status.HTTP_409_CONFLICT, "detail":"Language_level name already exists."},

    AdressConstraint.ADRESS_PK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Adress primary key already exists."},
    AdressConstraint.DUPLICATE_ADRESS: {"status_code":status.HTTP_409_CONFLICT, "detail":"Adress already exists."},
    AdressConstraint.DUPLICATE_POSTAL_CODE: {"status_code":status.HTTP_409_CONFLICT, "detail":"Postal code already exists."},

    JobConstraint.JOB_PK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Job primary key already exists."},
    JobConstraint.COMPANY_FK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Problem occurred with the company foreign key."},
    JobConstraint.SECTOR_FK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Problem occurred with the sector foreign key."},
    JobConstraint.ADRESS_FK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Problem occurred with the adress foreign key."},
    JobConstraint.LEVEL_EDUCATION_FK: {"status_code":status.HTTP_409_CONFLICT, "detail":"Problem occurred with the education_level foreign key."},

    _NULL_IN_RELATION_ERROR: {"status_code":status.HTTP_409_CONFLICT, "detail":"The resource cannot be deleted because it is being used by another resource."}
}

