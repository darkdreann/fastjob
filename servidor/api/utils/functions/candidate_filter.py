from typing import Annotated, Any
from fastapi import Depends
from uuid import UUID
from pydantic import BaseModel, Field
from sqlalchemy import func, text, select
from sqlalchemy.orm import contains_eager, defaultload
from fastapi.exceptions import RequestValidationError
from api.routers.job import GetJob
from api.database.database_models.models import Job
from api.database.database_models.models import Candidate, Address, Experience, Sector, User, Language, LanguageLevel, CandidateLanguage, CandidateEducation, Education, EducationLevel, SectorEducation, JobCandidate
from api.models.enums.endpoints import CandidateExtraField, JobCandidateExtraField
from api.utils.constants.endpoints_params import ADRESS_POSTAL_CODE_QUERY, ADRESS_PROVINCE, EXPERIENCE_MONTHS, RESOURCE_SECTOR, AVAILABILITY_PARAM
from api.utils.constants.endpoints_params import CANDIDATE_EXTRA_FIELD, LANGUAGE_CANDIDATE, LANGUAGE_LEVEL_VALUE, EDUCATION_NAME_PARAM, EDUCATION_LEVEL_PARAM, SKILLS_PARAM
from api.utils.constants.error_strings import INVALID_CANDIDATE_DIR_PARAMS, INVALID_CANDIDATE_LANGUAGE_PARAMS, INVALID_EDUCATION_PARAMS
from api.models.enums.models import WorkSchedule

class _CandidateParams(BaseModel):
    """
    Clase que representa los parámetros para filtrar candidatos.
    """

    joins: list[dict[str, Any]] = Field(default=[])
    where: list[Any] = Field(default=[])
    options: list[Any] = Field(default=[])

    joined: set[Any] = Field(default=set(), exclude=True)

    def add_join(self, join_table: dict[str, Any]):
        """
        Agrega una tabla de unión a los parámetros del candidato.

        Args:
            join_table (dict[str, Any]): La tabla de unión a agregar.
        """
        if join_table["target"] in self.joined:
            return

        self.joined.add(join_table["target"])
        self.joins.append(join_table)
    
    def add_join_list(self, join_list: tuple[dict[str, Any]]) -> None:
        """
        Agrega una lista de tablas de unión a los parámetros del candidato.

        Args:
            join_list (tuple[dict[str, Any]]): La lista de tablas de unión a agregar.
        """
        for join in join_list:
            self.add_join(join)

# ENDPOINT DEPENDENCIES #
def _get_uuid_or_str(string: str) -> UUID | str:
    """
    Obtiene el UUID de un string. Si no es un UUID válido, devuelve el string.

    Args:
        string (str): El string a convertir.

    Returns:
        UUID | str: El UUID o el string.
    """

    try:
        return UUID(string)
    except:
        return string.lower() if string is not None else string

async def _get_extra_fields(extra_fields: Annotated[set[CandidateExtraField], CANDIDATE_EXTRA_FIELD] = ()) -> set[CandidateExtraField]:
    """
    Obtiene los campos extra para incluir en el resultado de la consulta.

    Args:
        extra_fields (set[CandidateExtraField], optional): Conjunto de campos extra. Defaults to ().

    Returns:
        set[CandidateExtraField]: Conjunto de campos extra para el candidato.
    """
    return extra_fields

async def _get_extra_fields_applied_candidates(extra_fields: Annotated[set[JobCandidateExtraField], CANDIDATE_EXTRA_FIELD] = ()) -> set[CandidateExtraField]:
    """
    Obtiene los campos extra para incluir en el resultado de la consulta.

    Args:
        extra_fields (set[CandidateExtraField], optional): Conjunto de campos extra. Defaults to ().

    Returns:
        set[CandidateExtraField]: Conjunto de campos extra para el candidato.
    """
    return extra_fields

async def _get_direction_params(postal_code: Annotated[int, ADRESS_POSTAL_CODE_QUERY] = None,
                                province: Annotated[str, ADRESS_PROVINCE] = None) -> bool | None:
    """
    Obtiene los datos para filtrar los candidatos por dirección.

    Args:
        postal_code: El código postal para filtrar los candidatos. (Opcional)
        province: La provincia para filtrar los candidatos. (Opcional)

    Return:
        bool | None: Los candidatos que cumplen con los criterios de filtrado, o None si no se especificaron criterios.

    Raise:
        RequestValidationError: Si se especifican tanto el código postal como la provincia.
    """
    
    if postal_code and province: raise RequestValidationError([INVALID_CANDIDATE_DIR_PARAMS])

    if postal_code:
        return Address.postal_code == postal_code
    
    if province:
        return Address.province == province.lower()

async def _get_experience_params(experience_months: Annotated[int, EXPERIENCE_MONTHS] = None,
                                 experience_sector: Annotated[str | UUID, RESOURCE_SECTOR] = None) -> dict | None:
    """
    Obtiene los datos para filtrar los candidatos por experiencia.
    
    Args:
        experience_months (int, opcional): Los meses de experiencia requeridos.
        experience_sector (UUID | str, opcional): El sector de experiencia requerido.
    
    Return:
        dict | None: Un diccionario con los meses de experiencia y el sector de experiencia, o None si no se especifica ninguno.
    """
    
    if not experience_months and not experience_sector: return None

    experience_sector = _get_uuid_or_str(experience_sector)

    experience = {
        "experience_months": experience_months,
        "experience_sector": experience_sector
    }

    return experience

async def _get_language_params(language: Annotated[str | UUID, LANGUAGE_CANDIDATE] = None,
                               language_level: Annotated[int, LANGUAGE_LEVEL_VALUE] = None) -> dict | None:
    """
    Obtiene los parámetros de idioma para filtrar candidatos.

    Args:
        language (str | UUID, optional): El idioma o el identificador UUID del idioma. Defaults to None.
        language_level (int, optional): El nivel de idioma. Defaults to None.

    Returns:
        dict | None: Los parámetros de idioma para filtrar candidatos o None si no se proporcionan los parámetros.

    Raises:
        RequestValidationError: Si no se proporciona el idioma pero se proporciona el nivel de idioma.
    """
    
    if not language and language_level: raise RequestValidationError([INVALID_CANDIDATE_LANGUAGE_PARAMS])
    if not language and not language_level: return None
    
    language = _get_uuid_or_str(language)

    language_params = {
        "language": language,
        "language_level": language_level
    }

    return language_params

async def _get_education_params(education_name: Annotated[str, EDUCATION_NAME_PARAM] = None,
                                education_level: Annotated[int, EDUCATION_LEVEL_PARAM] = None,
                                education_sector: Annotated[str | UUID, RESOURCE_SECTOR] = None) -> dict | None:
    """
    Obtiene los parámetros de educación para filtrar candidatos.

    Args:
        education_name (str, optional): El nombre de la educación. Defaults to None.
        education_level (int, optional): El nivel de educación. Defaults to None.
        education_sector (str | UUID, optional): El sector de educación. Defaults to None.

    Returns:
        dict | None: Los parámetros de educación para filtrar candidatos o None si no se proporcionan parámetros.

    Raises:
        RequestValidationError: Si se proporciona el nombre de educación junto con el nivel o sector de educación.
    """
    
    if education_name and (education_level or education_sector): raise RequestValidationError([INVALID_EDUCATION_PARAMS])
    if not education_name and not education_level and not education_sector: return None

    education_sector = _get_uuid_or_str(education_sector)

    education_params = {
        "education_name": education_name.lower() if education_name else None,
        "education_level": education_level,
        "education_sector": education_sector
    }

    return education_params

async def _get_skills_and_availability_params(skills: Annotated[list[str], SKILLS_PARAM] = None,
                                              availability: Annotated[list[WorkSchedule], AVAILABILITY_PARAM] = None) -> dict | None:
    """
    Obtiene los parámetros de habilidades y disponibilidad.

    Args:
        skills (list[str], optional): Lista de habilidades. Defaults to None.
        availability (list[WorkSchedule], optional): Lista de horarios de disponibilidad. Defaults to None.

    Returns:
        dict | None: Diccionario con los parámetros de habilidades y disponibilidad, o None si no se proporcionan habilidades ni disponibilidad.
    """
    
    if not skills and not availability: return None

    skills_and_availability_params = {
        "skills": skills,
        "availability": availability
    }

    return skills_and_availability_params


# SET QUERY PARAMS #

def _set_params_extra_field(query_params: _CandidateParams, extra_fields: set[CandidateExtraField]) -> None:
    """
    Establece los datos a incluir de las tablas de unión en el resultado de la consulta.

    Args:
        query_params (_CandidateParams): Los parámetros de consulta para el filtro de candidatos.
        extra_fields (set[CandidateExtraField]): Los campos adicionales de candidatos.
    """
    for field in extra_fields:
        param = CandidateExtraField.get_join_table(field)

        query_params.add_join_list(param["joins"])
        query_params.options.extend(param["options"])
            

def _set_params_dir(query_params: _CandidateParams, dir_condition: bool | None) -> None:
    """
    Establece los parámetros de dirección en los query_params.

    Args:
        query_params (_CandidateParams): Los parámetros de consulta del candidato.
        dir_condition (bool | None): La condición de dirección.
    """

    if dir_condition is not None:
        query_params.where.append(dir_condition)


def _set_params_experience(query_params: _CandidateParams, experience_params: dict | None) -> None:
    """
    Establece los parámetros de experiencia en los parámetros de consulta.

    Args:
        query_params (_CandidateParams): Los parámetros de consulta de candidato.
        experience_params (dict | None): Los parámetros de experiencia.
    """
    if not experience_params: return

    experience_months = experience_params.get("experience_months", None)
    experience_sector = experience_params.get("experience_sector", None)

    if experience_months:
        experience_months_sum = select(
                Experience.candidate_id, 
                func.sum(func.age(func.coalesce(Experience.end_date, text("CURRENT_DATE")), Experience.start_date)).label('total_experience')
            ).group_by(Experience.candidate_id)

    if experience_sector:
        sector_field = Sector.id if isinstance(experience_sector, UUID) else Sector.category
    
        if experience_months:
            experience_months_sum = experience_months_sum.join(Sector, Experience.sector_id == Sector.id).where(sector_field == experience_sector)
            
        else:
            query_params.add_join({
                            "target": Sector,
                            "onclause": Experience.sector_id == Sector.id
                        })
            
            query_params.where.append(sector_field == experience_sector)


    if experience_months:

        experience_months_sum = experience_months_sum.alias('experience_sum')
            
        query_params.add_join_list((
                    {            
                        "target": Experience,
                        "onclause": Experience.candidate_id == Candidate.user_id
                    },
                    {
                        "target": experience_months_sum,
                        "onclause": Candidate.user_id == experience_months_sum.c.candidate_id
                    }
        ))
        
        query_params.where.append(experience_months_sum.c.total_experience >= text(f"interval '{experience_months} months'"))



def _set_params_language(query_params: _CandidateParams, language_params: dict | None) -> None:
    """
    Establece los parámetros de idioma en los query_params.

    Args:
        query_params (_CandidateParams): Los parámetros de consulta para filtrar candidatos.
        language_params (dict | None): Los parámetros de idioma para filtrar candidatos.
    """
    if not language_params: return

    language = language_params.get("language")
    language_level = language_params.get("language_level", None)

    language_field = Language.id if isinstance(language, UUID) else Language.name

    query_params.add_join_list((
                        {
                            "target": CandidateLanguage,
                            "onclause": CandidateLanguage.candidate_id == Candidate.user_id
                        },
                        {
                            "target": Language,
                            "onclause": CandidateLanguage.language_id == Language.id
                        }
                    ))
    query_params.where.append(language_field == language)

    if language_level:
        query_params.add_join({
                        "target": LanguageLevel,
                        "onclause": CandidateLanguage.language_level_id == LanguageLevel.id
                    })
        query_params.where.append(LanguageLevel.value >= language_level)


def _set_params_education(query_params: _CandidateParams, education_params: dict | None) -> None:
    """
    Establece los parámetros de educación en los query_params.

    Args:
        query_params (_CandidateParams): Los parámetros de consulta para filtrar candidatos.
        education_params (dict | None): Los parámetros de educación para filtrar candidatos.
    """
    if not education_params: return

    education_name = education_params.get("education_name", None)
    education_level = education_params.get("education_level", None)
    education_sector = education_params.get("education_sector", None)

    query_params.add_join_list((        
        {
            "target": CandidateEducation,
            "onclause": CandidateEducation.candidate_id == Candidate.user_id
        },
        {
            "target": Education,
            "onclause": CandidateEducation.education_id == Education.id
        }
    ))

    if education_name:
        query_params.where.append(Education.qualification == education_name)

    if education_level:
        query_params.add_join(
            {
                "target": EducationLevel,
                "onclause": Education.level_id == EducationLevel.id
            }
        )
        query_params.where.append(EducationLevel.value >= education_level)

    if education_sector:
        education_sector_field = Sector.id if isinstance(education_sector, UUID) else Sector.category

        query_params.add_join_list((
            {
                "target": SectorEducation,
                "onclause": Education.id == SectorEducation.education_id
            },
            {
                "target": Sector,
                "onclause": SectorEducation.sector_id == Sector.id
            }
        ))
        query_params.where.append(education_sector_field == education_sector)

def _set_params_skills_and_availability(query_params: _CandidateParams, skills_and_availability_params: dict | None) -> None:
    """
    Establece los parámetros de habilidades y disponibilidad en los parámetros de consulta.

    Args:
        query_params (_CandidateParams): Los parámetros de consulta de candidatos.
        skills_and_availability_params (dict | None): Los parámetros de habilidades y disponibilidad.
    """
    if not skills_and_availability_params: return

    skills = skills_and_availability_params.get("skills", None)
    availability = skills_and_availability_params.get("availability", None)

    if skills:
        query_params.where.append(Candidate.skills.contains(skills))

    if availability:
        query_params.where.append(Candidate.availability.contains(availability))


async def get_candidate_params(extra_fields_params: Annotated[set, Depends(_get_extra_fields)],
                               direction_params: Annotated[bool | None, Depends(_get_direction_params)],
                               experience_params: Annotated[dict | None, Depends(_get_experience_params)],
                               language_params: Annotated[dict | None, Depends(_get_language_params)],
                               education_params: Annotated[dict, Depends(_get_education_params)],
                               skills_and_availability_params: Annotated[dict, Depends(_get_skills_and_availability_params)]) -> dict:
    """
    Obtiene los parámetros de candidato para filtrar la búsqueda.

    Args:
        extra_fields_params (set): Conjunto de campos adicionales para incluir en la consulta.
        direction_params (bool | None): Dirección de los candidatos a filtrar.
        experience_params (dict | None): Parámetros de experiencia para filtrar los candidatos.

    Returns:
        dict: Los parámetros finales de la consulta.
    """
                    
    query_params = _CandidateParams(
        options = [contains_eager(Candidate.user).contains_eager(User.address)]
    )

    query_params.add_join_list((
                {
                    "target": User,
                    "onclause": Candidate.user_id == User.id
                },
                {
                    "target": Address,
                    "onclause": User.address_id == Address.id
                }
    ))

    _set_params_extra_field(query_params, extra_fields_params)
    _set_params_dir(query_params, direction_params)
    _set_params_experience(query_params, experience_params)
    _set_params_language(query_params, language_params)
    _set_params_education(query_params, education_params)
    _set_params_skills_and_availability(query_params, skills_and_availability_params)

    final_query_params = query_params.model_dump(exclude_defaults=True)

    return final_query_params

async def get_candidate_applied(extra_fields_params: Annotated[set, Depends(_get_extra_fields_applied_candidates)],
                               direction_params: Annotated[bool | None, Depends(_get_direction_params)],
                               experience_params: Annotated[dict | None, Depends(_get_experience_params)],
                               language_params: Annotated[dict | None, Depends(_get_language_params)],
                               education_params: Annotated[dict, Depends(_get_education_params)],
                               skills_and_availability_params: Annotated[dict, Depends(_get_skills_and_availability_params)],
                               job: Annotated[Job, Depends(GetJob(False))])  -> dict:
    """
    Obtiene los parámetros de búsqueda de candidatos aplicados y devuelve un diccionario con los parámetros de consulta.

    Args:
    - extra_fields_params (set): Conjunto de campos adicionales aplicados a los candidatos.
    - direction_params (bool | None): Parámetro de dirección de búsqueda de candidatos.
    - experience_params (dict | None): Parámetros de experiencia de búsqueda de candidatos.
    - language_params (dict | None): Parámetros de idioma de búsqueda de candidatos.
    - education_params (dict): Parámetros de educación de búsqueda de candidatos.
    - skills_and_availability_params (dict): Parámetros de habilidades y disponibilidad de búsqueda de candidatos.

    Returns:
    - dict: Diccionario con los parámetros de consulta.

    """
    query_params = await get_candidate_params(extra_fields_params, direction_params, experience_params, language_params, education_params, skills_and_availability_params)

    if "where" not in query_params:
        query_params["where"] = []

    query_params["joins"].append({
        "target": JobCandidate,
        "onclause": Candidate.user_id == JobCandidate.candidate_id
    })


    query_params["where"].append(JobCandidate.job_id == job.id)

    query_params["options"].append(defaultload(Candidate.applied_jobs_list).noload(JobCandidate.job))

    query_params["order"] = (JobCandidate.inscription_date.desc())

    return query_params
    