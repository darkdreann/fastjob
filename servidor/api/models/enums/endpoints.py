from enum import Enum
from sqlalchemy.orm import joinedload
from fastapi.exceptions import RequestValidationError
from api.database.database_models.models import Sector, Adress, EducationLevel, Language, LanguageLevel
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



class CandidateField(str,Enum):
    """Enum que representa los campos de la tabla candidate.
    
                WIP: Work In Progress
    """

    user  = "user"
    skills  = "skills"
    availability = "availability"
    experiences = "experiences"
    education = "education"
    language = "language"
    applied_jobs = "applied_jobs"


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
    
class AdressExtraField(ExtraFields):
    """Enum que representa los campos extra de la tabla adress."""

    USER = "users"
    JOB = "jobs"

    
    @classmethod
    def _get_values(cls):
        return {
            cls.USER: joinedload(Adress.users_list),
            cls.JOB: joinedload(Adress.jobs_list)
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