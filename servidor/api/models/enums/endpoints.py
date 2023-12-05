from enum import Enum
from sqlalchemy.orm import joinedload, contains_eager, defaultload
from fastapi.exceptions import RequestValidationError
from api.database.database_models.models import Sector, Address, EducationLevel, Language, LanguageLevel, Candidate, CandidateLanguage, CandidateEducation, Experience, Education, SectorEducation, JobCandidate, Job
from api.utils.constants.error_strings import INVALID_EXTRA_FIELDS

# ENUMS ENDPOINTS #

class ExtraFields(str, Enum):
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
        return {
            cls.USER: joinedload(Address.users_list),
            cls.JOB: joinedload(Address.jobs_list)
        }
    
class EducationLevelExtraField(ExtraFields):
    """Enum que representa los campos extra de la tabla education level."""

    EDUCATION = "educations"
    JOB = "jobs"

    @classmethod
    def _get_values(cls):
        return {
            cls.EDUCATION: joinedload(EducationLevel.education_list),
            cls.JOB: joinedload(EducationLevel.jobs_list)
        }
    
class LanguageExtraField(ExtraFields):
    """Enum que representa los campos extra de la tabla language."""

    CANDIDATE = "candidates"
    JOB = "jobs"

    @classmethod
    def _get_values(cls):
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
        return {
            cls.LANGUAGE: joinedload(LanguageLevel.candidates_language_list),
            cls.CANDIDATE: joinedload(LanguageLevel.jobs_language_list)
        }
    

class CandidateExtraField(ExtraFields):
    """Enum que representa los campos de la tabla candidate."""

    EXPERIENCE = "experiences"
    EDUCATION = "education"
    LANGUAGE = "language"
    APPLIED_JOBS = "applied_jobs"

    @classmethod
    def _get_values(cls):
        return {
            cls.LANGUAGE: joinedload(Candidate.language_list),
            cls.EXPERIENCE: joinedload(Candidate.experience_list),
            cls.EDUCATION: joinedload(Candidate.education_list),          
            cls.APPLIED_JOBS: joinedload(Candidate.applied_jobs_list)
        }
    
    @classmethod
    def get_join_table(cls, field: str):

        values = {
            cls.LANGUAGE: {
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

            cls.EXPERIENCE:{ 
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

            cls.EDUCATION:{
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

            cls.APPLIED_JOBS: {
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

        if field not in values:
            return RequestValidationError(INVALID_EXTRA_FIELDS.format(field=field))
        
        return values[field]
        