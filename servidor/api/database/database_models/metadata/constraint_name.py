class JobCandidateConstraint:
    JOB_CANDIDATE_PK = "job_candidate_pk"
    CANDIDATE_FK = "job_candidate_candidate_id_fk"
    JOB_FK = "job_candidate_job_id_fk"

class JobEducationConstraint:
    JOB_EDUCATION_PK = "job_education_pk"
    JOB_FK = "job_education_job_id_fk"
    EDUCATION_FK = "job_education_education_id_fk"
    DUPLICATE_JOB_ID = "job_education_duplicate_job_id"

class SectorEducationConstraint:
    SECTOR_EDUCATION_PK = "sector_education_pk"
    SECTOR_FK = "sector_education_sector_id_fk"
    EDUCATION_FK = "sector_education_education_id_fk"
    DUPLICATE_EDUCATION_ID = "sector_education_duplicate_education_id"

class CandidateEducationConstraint:
    CANDIDATE_EDUCATION_PK = "candidate_education_pk"
    CANDIDATE_FK = "candidate_education_candidate_id_fk"
    EDUCATION_FK = "candidate_education_education_id_fk"

class CandidateLanguageConstraint:
    CANDIDATE_LANGUAGE_PK = "candidate_language_pk"
    CANDIDATE_FK = "candidate_language_candidate_id_fk"
    LANGUAGE_FK = "candidate_language_language_id_fk"
    LANGUAGE_LEVEL_FK = "candidate_language_language_level_id_fk"

class JobLanguageConstraint:
    JOB_LANGUAGE_PK = "job_language_pk"
    JOB_FK = "job_language_job_id_fk"
    LANGUAGE_FK = "job_language_language_id_fk"
    LANGUAGE_LEVEL_FK = "job_language_language_level_id_fk"

class UserConstraint:
    USER_PK = "user_pk"
    DUPLICATE_EMAIL = "unique_email"
    DUPLICATE_USERNAME = "unique_username"
    ADMIN_HAS_TABLE = "check_admin_has_candidate_or_company_table"
    CANDIDATE_HAS_COMPANY_TABLE = "check_candidate_has_company_table"
    COMPANY_HAS_CANDIDATE_TABLE = "check_company_has_candidate_table"
    ADDRESS_FK = "user_address_id_fk"

class CandidateConstraint:
    CANDIDATE_PK = "candidate_pk"
    USER_NOT_CANDIDATE = "check_user_is_candidate"
    USER_FK = "candidate_user_id_fk"

class CompanyConstraint:
    COMPANY_PK = "company_pk"
    USER_NOT_COMPANY = "check_user_is_company"
    DUPLICATE_TIN = "unique_tin"
    DUPLICATE_COMPANY_NAME = "unique_company_name"
    USER_FK = "company_user_id_fk"

class LanguageConstraint:
    LANGUAGE_PK = "language_pk"
    DUPLICATE_LANGUAGE_NAME = "unique_language_name"

class SectorConstraint:
    SECTOR_PK = "sector_pk"
    DUPLICATE_CATEGORY_SUBCATEGORY = "unique_sector_name"

class ExperienceConstraint:
    EXPERIENCE_PK = "experience_pk"
    CANDIDATE_FK = "experience_candidate_id_fk"
    SECTOR_FK = "experience_sector_id_fk"

class EducationConstraint:
    EDUCATION_PK = "education_pk"
    DUPLICATE_QUALIFICATION = "unique_education_qualification"
    LEVEL_FK = "education_level_id_fk"

class EducationLevelConstraint:
    EDUCATION_LEVEL_PK = "education_level_pk"
    DUPLICATE_NAME = "unique_education_level_name"
    DUPLICATE_VALUE = "unique_education_level_value"

class LanguageLevelConstraint:
    LANGUAGE_LEVEL_PK = "language_level_pk"
    DUPLICATE_NAME = "unique_language_level_name"
    DUPLICATE_VALUE = "unique_language_level_value"

class AddressConstraint:
    ADDRESS_PK = "address_pk"
    DUPLICATE_ADDRESS = "unique_street"

class JobConstraint:
    JOB_PK = "job_pk"
    ADDRESS_FK = "job_address_id_fk"
    COMPANY_FK = "job_company_id_fk"
    SECTOR_FK = "job_sector_id_fk"
    LEVEL_EDUCATION_FK = "job_education_level_id_fk"