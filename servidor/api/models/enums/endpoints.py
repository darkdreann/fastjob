from enum import Enum
from sqlalchemy.orm import joinedload, contains_eager, defaultload
from fastapi.exceptions import RequestValidationError
from api.database.database_models.models import Sector, Address, EducationLevel, Language, LanguageLevel, Candidate, CandidateLanguage
from api.database.database_models.models import CandidateEducation, Experience, Education, SectorEducation, JobCandidate, Job, User, Company
from api.utils.constants.error_strings import INVALID_EXTRA_FIELDS

# ENUMS ENDPOINTS #

class ExtraFields(str, Enum):
    """Enum base para los campos extra de las tablas."""

    @classmethod
    def get_field_value(cls, field: str):
        """Retorna el load del campo de la tabla que corresponde al campo extra"""

        values = cls._get_values()

        if field not in values:
            return RequestValidationError(INVALID_EXTRA_FIELDS.format(field=field))

        return values[field]

class SectorExtraField(ExtraFields):
    """Enum que representa los campos extra de la tabla sector."""

    EDUCATION = "educations"
    EXPERIENCE = "experiences"
    JOB = "jobs"

    @classmethod
    def _get_values(cls):
        """Retorna un diccionario con los campos extra de la tabla sector."""

        return {
            cls.EDUCATION: joinedload(Sector.education_list),
            cls.EXPERIENCE: joinedload(Sector.experience_list),
            cls.JOB: joinedload(Sector.job_list)
        }
    
class AddressExtraField(ExtraFields):
    """Enum que representa los campos extra de la tabla address."""

    USER = "users"
    JOB = "jobs"

    
    @classmethod
    def _get_values(cls):
        """Retorna un diccionario con los campos extra de la tabla address."""

        return {
            cls.USER: joinedload(Address.users_list),
            cls.JOB: joinedload(Address.jobs_list)
        }
    
class EducationExtraField(ExtraFields):
    """Enum que representa los campos extra de la tabla education level."""

    CANDIDATE = "candidates"
    JOB = "jobs"

    @classmethod
    def _get_values(cls):
        """Retorna un diccionario con los campos extra de la tabla education level."""

        return {
            cls.CANDIDATE: joinedload(Education.candidates_list).defaultload(CandidateEducation.candidate).joinedload(Candidate.user).joinedload(User.address),
            cls.JOB: joinedload(Education.Jobs_list)
        }
    
class LanguageExtraField(ExtraFields):
    """Enum que representa los campos extra de la tabla language."""

    CANDIDATE = "candidates"
    JOB = "jobs"

    @classmethod
    def _get_values(cls):
        """Retorna un diccionario con los campos extra de la tabla language."""

        return {
            cls.CANDIDATE: joinedload(Language.candidates_list),
            cls.JOB: joinedload(Language.jobs_list)
        }
    
class LanguageLevelExtraField(ExtraFields):
    """Enum que representa los campos extra de la tabla language level."""

    LANGUAGE = "languages"
    CANDIDATE = "candidates"

    @classmethod
    def _get_values(cls):
        """Retorna un diccionario con los campos extra de la tabla language level."""

        return {
            cls.LANGUAGE: joinedload(LanguageLevel.candidates_language_list),
            cls.CANDIDATE: joinedload(LanguageLevel.jobs_language_list)
        }
    

class JobExtraField(ExtraFields):
    """Enum que representa los campos extra de la tabla job."""
    
    CANDIDATE = "candidates"
    COMPANY = "company"

    @classmethod
    def _get_values(cls):
        """Retorna un diccionario con los campos extra de la tabla job."""

        return {
            cls.CANDIDATE: joinedload(Job.candidates_list).defaultload(JobCandidate.candidate).joinedload(Candidate.user).joinedload(User.address),
            cls.COMPANY: joinedload(Job.company).joinedload(Company.user).joinedload(User.address)
        }

class CandidateFieldsValues:
    @classmethod
    def get_values(cls):
        """Retorna un diccionario con los campos extra de la tabla candidate."""

        return {
            CandidateExtraField.LANGUAGE: joinedload(Candidate.language_list),
            CandidateExtraField.EXPERIENCE: joinedload(Candidate.experience_list),
            CandidateExtraField.EDUCATION: joinedload(Candidate.education_list),          
            CandidateExtraField.APPLIED_JOBS: joinedload(Candidate.applied_jobs_list)
        }
    
    @classmethod
    def get_join_table(cls):
        """Retorna los valores de los joins y options de la tabla candidate. Se utiliza para los filtros."""

        values = {
            CandidateExtraField.LANGUAGE: {
                            "joins":
                                (
                                    {
                                        "target": CandidateLanguage,
                                        "onclause": Candidate.user_id == CandidateLanguage.candidate_id,
                                        "isouter": True
                                    },
                                    {
                                        "target": LanguageLevel,
                                        "onclause": CandidateLanguage.language_level_id == LanguageLevel.id,
                                        "isouter": True
                                    },
                                    {
                                        "target": Language,
                                        "onclause": CandidateLanguage.language_id == Language.id,
                                        "isouter": True
                                    }
                                ),
                            "options": (contains_eager(Candidate.language_list).contains_eager(CandidateLanguage.language),
                                        defaultload(Candidate.language_list).contains_eager(CandidateLanguage.language_level))
            },

            CandidateExtraField.EXPERIENCE:{ 
                            "joins":
                                (
                                    {
                                        "target": Experience,
                                        "onclause": Candidate.user_id == Experience.candidate_id,
                                        "isouter": True
                                    },
                                    {
                                        "target": Sector,
                                        "onclause": Experience.sector_id == Sector.id,
                                        "isouter": True
                                    }
                                ),
                            "options": (contains_eager(Candidate.experience_list).contains_eager(Experience.sector),)
            },

            CandidateExtraField.EDUCATION:{
                            "joins":
                                (
                                    {
                                        "target": CandidateEducation,
                                        "onclause": Candidate.user_id == CandidateEducation.candidate_id,
                                        "isouter": True
                                    },
                                    {
                                        "target": Education,
                                        "onclause": CandidateEducation.education_id == Education.id,
                                        "isouter": True
                                    },
                                    {
                                        "target": EducationLevel,
                                        "onclause": Education.level_id == EducationLevel.id,
                                        "isouter": True
                                    },
                                    {
                                        "target": SectorEducation,
                                        "onclause": SectorEducation.education_id == Education.id,
                                        "isouter": True
                                    },
                                    {
                                        "target": Sector,
                                        "onclause": SectorEducation.sector_id == Sector.id,
                                        "isouter": True
                                    }
                                ),
                            "options": (contains_eager(Candidate.education_list).contains_eager(CandidateEducation.education).contains_eager(Education.level),
                                        defaultload(Candidate.education_list).defaultload(CandidateEducation.education).contains_eager(Education.sector).contains_eager(SectorEducation.sector))
            },

            CandidateExtraField.APPLIED_JOBS: {
                                "joins": 
                                    (
                                        {
                                            "target": JobCandidate,
                                            "onclause": Candidate.user_id == JobCandidate.candidate_id,
                                            "isouter": True
                                        },
                                        {
                                            "target": Job,
                                            "onclause": JobCandidate.job_id == Job.id,
                                            "isouter": True
                                        }
                                    ),
                                "options": (contains_eager(Candidate.applied_jobs_list).contains_eager(JobCandidate.job),)
            }
        }

        return values
    
class CandidateExtraField(ExtraFields):
    """Enum que representa los campos de la tabla candidate."""

    EXPERIENCE = "experiences"
    EDUCATION = "education"
    LANGUAGE = "language"
    APPLIED_JOBS = "applied_jobs"

    @classmethod
    def _get_values(cls):
        """Retorna un diccionario con los campos extra de la tabla candidate."""

        return CandidateFieldsValues.get_values()
    
    @classmethod
    def get_join_table(cls, field: str):
        """Retorna un diccionario con los joins y options de la tabla candidate. Se utiliza para los filtros."""

        values = CandidateFieldsValues.get_join_table()

        if field not in values:
            return RequestValidationError(INVALID_EXTRA_FIELDS.format(field=field))
        
        return values[field]
        

class JobCandidateExtraField(ExtraFields):
    """Enum que representa los campos de la tabla candidate."""

    EXPERIENCE = "experiences"
    EDUCATION = "education"
    LANGUAGE = "language"

    @classmethod
    def _get_values(cls):
        """Retorna un diccionario con los campos extra de la tabla candidate."""

        return CandidateFieldsValues.get_values()
    
    @classmethod
    def get_join_table(cls, field: str):
        """Retorna un diccionario con los joins y options de la tabla candidate. Se utiliza para los filtros."""

        values = CandidateFieldsValues.get_join_table()

        if field not in values:
            return RequestValidationError(INVALID_EXTRA_FIELDS.format(field=field))
        
        return values[field]
        