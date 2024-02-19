from uuid import UUID
from typing import Annotated
from fastapi import Depends
from sqlalchemy import func, text, select
from sqlalchemy.orm import contains_eager, defaultload
from fastapi.exceptions import RequestValidationError
from api.models.enums.models import WorkSchedule
from api.models.base_models import QueryParams
from api.utils.functions.models_utils import GetJob
from api.models.enums.endpoints import CandidateExtraField, JobCandidateExtraField
from api.database.database_models.models import Job, CandidateEducation, Education, EducationLevel, SectorEducation, JobCandidate
from api.database.database_models.models import Candidate, Address, Experience, Sector, User, Language, LanguageLevel, CandidateLanguage
from api.utils.constants.error_strings import INVALID_CANDIDATE_DIR_PARAMS, INVALID_CANDIDATE_LANGUAGE_PARAMS, INVALID_EDUCATION_PARAMS
from api.utils.constants.endpoints_params import ADDRESS_POSTAL_CODE_QUERY, ADDRESS_PROVINCE, EXPERIENCE_MONTHS, RESOURCE_SECTOR, AVAILABILITY_PARAM, CANDIDATE_MINIMAL_FIELDS
from api.utils.constants.endpoints_params import CANDIDATE_EXTRA_FIELD, LANGUAGE_CANDIDATE, LANGUAGE_LEVEL_VALUE, EDUCATION_NAME_PARAM, EDUCATION_LEVEL_PARAM, SKILLS_PARAM

def _get_uuid_or_str_lower(string: str | None) -> UUID | str | None:
    """
    Obtiene el UUID de un string. Si no es un UUID válido, devuelve el string.

    Args:
    - string (str | None): El string a convertir.

    Returns:
    - UUID | str | None: El UUID o el string.
    """
    # si no es un string, devuelve el valor
    if not string: return string

    try:
        # si es un UUID válido, devuelve el UUID
        return UUID(string)
    except:
        # si no es un UUID válido, devuelve el string en minúsculas
        return string.lower()

async def _get_extra_fields(extra_fields: Annotated[set[CandidateExtraField], CANDIDATE_EXTRA_FIELD] = ()) -> set[CandidateExtraField]:
    """
    Obtiene los campos de las relaciones para incluir en el resultado de la consulta. Puede especificarse un conjunto de campos extra.
    Por defecto es un conjunto vacío.

    Args:
    - extra_fields (set[CandidateExtraField], optional): Conjunto de campos extra. Por defecto ().

    Returns:
    - set[CandidateExtraField]: Conjunto de campos extra para el candidato.
    """
    return extra_fields

async def _get_extra_fields_applied_candidates(extra_fields: Annotated[set[JobCandidateExtraField], CANDIDATE_EXTRA_FIELD] = ()) -> set[CandidateExtraField]:
    """
    Obtiene los campos de las relaciones para incluir en el resultado de la consulta. Puede especificarse un conjunto de campos extra.
    Por defecto es un conjunto vacío. Para ser usado en los candidatos aplicados a una oferta, por lo que se incluye el campo de la relación con las ofertas.

    Args:
    - extra_fields (set[CandidateExtraField], optional): Conjunto de campos extra. Defaults to ().

    Returns:
    - set[CandidateExtraField]: Conjunto de campos extra para el candidato.
    """
    return extra_fields

async def _get_direction_params(postal_code: Annotated[int | None, ADDRESS_POSTAL_CODE_QUERY] = None,
                                province: Annotated[str | None, ADDRESS_PROVINCE] = None) -> bool | None:
    """
    Obtiene el codigo postal o la provincia para filtrar los candidatos. Si se especifican ambos, devuelve un error.

    Args:
    - postal_code: El código postal para filtrar los candidatos. (Opcional)
    - province: La provincia para filtrar los candidatos. (Opcional)

    Return:
    - bool | None: Los candidatos que cumplen con los criterios de filtrado, o None si no se especificaron criterios.

    Raise:
    - RequestValidationError: Si se especifican tanto el código postal como la provincia.
    """
    
    # si se especifican ambos, devuelve un error
    if postal_code and province: raise RequestValidationError([INVALID_CANDIDATE_DIR_PARAMS])

    # si se especifica el código postal, devuelve la condición
    if postal_code:
        return Address.postal_code == postal_code
    
    # si se especifica la provincia, devuelve la condición
    if province:
        return Address.province == province.lower()

async def _get_experience_params(experience_months: Annotated[int | None, EXPERIENCE_MONTHS] = None,
                                 experience_sector: Annotated[str | UUID | None, RESOURCE_SECTOR] = None) -> dict | None:
    """
    Obtiene la cantidad de meses de experiencia y el sector de experiencia para filtrar candidatos.
    
    Args:
    - experience_months (int, opcional): Los meses de experiencia requeridos.
    - experience_sector (UUID | str, opcional): El sector de experiencia requerido.

    Return:
    - dict | None: Un diccionario con los meses de experiencia y el sector de experiencia, o None si no se especifica ninguno.
    """
    
    # si no se especifica ninguno, devuelve None
    if not experience_months and not experience_sector: return None

    # convierte el sector de experiencia a UUID si es un UUID válido
    experience_sector = _get_uuid_or_str_lower(experience_sector)

    # devuelve el diccionario con los parámetros de experiencia
    experience = {
        "experience_months": experience_months,
        "experience_sector": experience_sector
    }

    return experience

async def _get_language_params(language: Annotated[str | UUID | None, LANGUAGE_CANDIDATE] = None,
                               language_level: Annotated[int | None, LANGUAGE_LEVEL_VALUE] = None) -> dict | None:
    """
    Obtiene los parámetros de idioma para filtrar candidatos.

    Args:
    - language (str | UUID, optional): El idioma o el identificador UUID del idioma. Defaults to None.
    - language_level (int, optional): El nivel de idioma. Defaults to None.

    Returns:
    - dict | None: Los parámetros de idioma para filtrar candidatos o None si no se proporcionan los parámetros.

    Raises:
    - RequestValidationError: Si no se proporciona el idioma pero se proporciona el nivel de idioma.
    """
    
    # si se proporciona el nivel de idioma pero no el idioma, devuelve un error
    if not language and language_level: raise RequestValidationError([INVALID_CANDIDATE_LANGUAGE_PARAMS])
    # si no se proporciona el idioma ni el nivel de idioma, devuelve None
    if not language and not language_level: return None
    
    # convierte el idioma a UUID si es un UUID válido
    language = _get_uuid_or_str_lower(language)

    # devuelve el diccionario con los parámetros de idioma
    language_params = {
        "language": language,
        "language_level": language_level
    }

    return language_params

async def _get_education_params(education_name: Annotated[str | None, EDUCATION_NAME_PARAM] = None,
                                education_level: Annotated[int | None, EDUCATION_LEVEL_PARAM] = None,
                                education_sector: Annotated[str | UUID | None, RESOURCE_SECTOR] = None) -> dict | None:
    """
    Obtiene el nombre de la formación, el nivel de formación y el sector de formación para filtrar candidatos.
    No se pueden proporcionar el nombre de la formación junto con el nivel o el sector de formación.

    Args:
    - education_name (str, optional): El nombre de la formación. Defaults to None.
    - education_level (int, optional): El nivel de formación. Defaults to None.
    - education_sector (str | UUID, optional): El sector de formación. Defaults to None.

    Returns:
    - dict | None: Los parámetros de formación para filtrar candidatos o None si no se proporcionan parámetros.

    Raises:
    - RequestValidationError: Si se proporciona el nombre de formación junto con el nivel o sector de formación.
    """
    
    # si se proporciona el nombre de formación junto con el nivel o sector de formación, devuelve un error
    if education_name and (education_level or education_sector): raise RequestValidationError([INVALID_EDUCATION_PARAMS])

    # si no se proporciona ninguno, devuelve None
    if not education_name and not education_level and not education_sector: return None

    # convierte el sector de formación a UUID si es un UUID válido
    education_sector = _get_uuid_or_str_lower(education_sector)

    # devuelve el diccionario con los parámetros de formación
    education_params = {
        "education_name": education_name.lower() if education_name else None,
        "education_level": education_level,
        "education_sector": education_sector
    }

    return education_params

async def _get_skills_and_availability_params(skills: Annotated[list[str], SKILLS_PARAM] = None,
                                              availability: Annotated[WorkSchedule, AVAILABILITY_PARAM] = None) -> dict | None:
    """
    Obtiene los parámetros de habilidades y disponibilidad para filtrar candidatos.

    Args:
    - skills (list[str], optional): Lista de habilidades. Defaults to None.
    - availability (WorkSchedule, optional): Horario de disponibilidad. Defaults to None.

    Returns:
    - dict | None: Diccionario con los parámetros de habilidades y disponibilidad, o None si no se proporcionan habilidades ni disponibilidad.
    """
    
    # si no se proporcionan habilidades ni disponibilidad, devuelve None 
    if not skills and not availability: return None

    # devuelve el diccionario con los parámetros de habilidades y disponibilidad
    skills_and_availability_params = {
        "skills": skills,
        "availability": availability
    }

    return skills_and_availability_params


# SET QUERY PARAMS #

def _set_params_extra_field(query_params: QueryParams, extra_fields: set[CandidateExtraField]) -> None:
    """
    Establece los datos a mostrar de las relaciones de la tabla de candidatos en los parámetros de consulta.

    Args:
    - query_params (QueryParams): Los parámetros de consulta para el filtro de candidatos.
    - extra_fields (set[CandidateExtraField]): Los campos adicionales de candidatos.
    """
    # recorre los campos adicionales
    for field in extra_fields:
        # obtiene los parámetros del campo adicional
        param = CandidateExtraField.get_join_table(field)

        # anade las tablas al join de los parámetros de consulta
        query_params.add_join_list(param["joins"])

        # anade a las options de los parámetros de consulta las opciones para recontruir el objeto
        query_params.options.extend(param["options"])
            

def _set_params_dir(query_params: QueryParams, dir_condition: bool | None) -> None:
    """
    Establece en los parámetros de consulta la condición de dirección.

    Args:
    - query_params (QueryParams): Los parámetros de consulta del candidato.
    - dir_condition (bool | None): La condición de dirección.
    """

    # si la no es None, anade la condición de dirección a los parámetros de consulta
    if dir_condition is not None:
        query_params.where.append(dir_condition)


def _set_params_experience(query_params: QueryParams, experience_params: dict | None) -> None:
    """
    Establece en los parámetros de consulta los parámetros para filtrar por experiencia.

    Args:
    - query_params (QueryParams): Los parámetros de consulta de candidato.
    - experience_params (dict | None): Los parámetros de experiencia.
    """
    # si no se proporcionan parámetros de experiencia termina la función
    if not experience_params: return

    # obtiene los parámetros de experiencia
    experience_months = experience_params.get("experience_months", None)
    experience_sector = experience_params.get("experience_sector", None)

    # si se proporciona el sector de experiencia, creamos una subconsulta para obtener la suma de los meses de experiencia
    if experience_months:
        experience_months_sum = select(
                Experience.candidate_id, 
                func.sum(func.age(func.coalesce(Experience.end_date, text("CURRENT_DATE")), Experience.start_date)).label('total_experience')
            ).group_by(Experience.candidate_id)

    # si se proporciona el sector de experiencia, anade el sector de experiencia a los parámetros de consulta
    if experience_sector:
        # obtenemos el campo a usar como filtro dependiendo de si es un UUID o un string ( filtro por id o por categoría)
        sector_field = Sector.id if isinstance(experience_sector, UUID) else Sector.category

        # si se ha proporcionado el número de meses de experiencia, se anade el filtro de sector de experiencia a la subconsulta
        if experience_months:
            experience_months_sum = experience_months_sum.join(Sector, Experience.sector_id == Sector.id).where(sector_field == experience_sector)
            
        # si no se ha proporcionado el número de meses de experiencia, se anade el filtro de sector de experiencia a los parámetros de consulta
        else:
            query_params.add_join_list(
                (
                    {
                            "target": Experience,
                            "onclause": Experience.candidate_id == Candidate.user_id
                    },
                    {
                            "target": Sector,
                            "onclause": Experience.sector_id == Sector.id
                    }
                )
            )
            
            query_params.where.append(sector_field == experience_sector)

    # si se ha proporcionado el número de meses de experiencia, anade el filtro de meses de experiencia a los parámetros de consulta
    if experience_months:

        # nombramos la subconsulta
        experience_months_sum = experience_months_sum.alias('experience_sum')
        
        # anadimos la subconsulta a los joins de los parámetros de consulta
        query_params.add_join({
                            "target": experience_months_sum,
                            "onclause": Candidate.user_id == experience_months_sum.c.candidate_id
                        })
        
        # anade el filtro de meses de experiencia a los parámetros de consulta
        query_params.where.append(experience_months_sum.c.total_experience >= text(f"interval '{experience_months} months'"))



def _set_params_language(query_params: QueryParams, language_params: dict | None) -> None:
    """
    Establece los parámetros de idioma en los parámetros de consulta.

    Args:
    - query_params (QueryParams): Los parámetros de consulta para filtrar candidatos.
    - language_params (dict | None): Los parámetros de idioma para filtrar candidatos.
    """
    # si no se proporcionan parámetros de idioma, termina la función
    if not language_params: return

    # obtiene los parámetros de idioma
    language = language_params.get("language")
    language_level = language_params.get("language_level", None)

    # obtenemos el campo a usar como filtro dependiendo de si es un UUID o un string ( filtro por id o por nombre)
    language_field = Language.id if isinstance(language, UUID) else Language.name

    # anade los joins de idioma a los parámetros de consulta
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
    # anade el filtro de idioma a los parámetros de consulta
    query_params.where.append(language_field == language)

    #  si se proporciona el nivel de idioma, anade el filtro de nivel de idioma a los parámetros de consulta
    if language_level:
        # anade el join de nivel de idioma a los parámetros de consulta y el filtro de nivel de idioma
        query_params.add_join({
                        "target": LanguageLevel,
                        "onclause": CandidateLanguage.language_level_id == LanguageLevel.id
                    })
        query_params.where.append(LanguageLevel.value >= language_level)


def _set_params_education(query_params: QueryParams, education_params: dict | None) -> None:
    """
    Establece los parámetros de formación en los parámetros de consulta.

    Args:
    - query_params (QueryParams): Los parámetros de consulta para filtrar candidatos.
    - education_params (dict | None): Los parámetros de formación para filtrar candidatos.
    """

    # si no se proporcionan parámetros de formación, termina la función
    if not education_params: return

    # obtiene los parámetros de formación
    education_name = education_params.get("education_name", None)
    education_level = education_params.get("education_level", None)
    education_sector = education_params.get("education_sector", None)

    # anade los joins de formación a los parámetros de consulta
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

    # si se proporciona el nombre de formación, anade el filtro de nombre de formación a los parámetros de consulta
    if education_name:
        query_params.where.append(Education.qualification.contains(education_name))

    # si se proporciona el nivel de formación, anade el join de nivel de formación a los parámetros de consulta y el filtro de nivel de formación
    if education_level:
        query_params.add_join(
            {
                "target": EducationLevel,
                "onclause": Education.level_id == EducationLevel.id
            }
        )
        query_params.where.append(EducationLevel.value >= education_level)

    # si se proporciona el sector de formación, anade el join de sector de formación a los parámetros de consulta y el filtro de sector de formación
    if education_sector:
        # obtenemos el campo a usar como filtro dependiendo de si es un UUID o un string ( filtro por id o por categoría)
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

def _set_params_skills_and_availability(query_params: QueryParams, skills_and_availability_params: dict | None) -> None:
    """
    Establece los parámetros de habilidades y disponibilidad en los parámetros de consulta.

    Args:
    - query_params (QueryParams): Los parámetros de consulta de candidatos.
    - skills_and_availability_params (dict | None): Los parámetros de habilidades y disponibilidad.
    """

    # si no se proporcionan parámetros de habilidades y disponibilidad, termina la función
    if not skills_and_availability_params: return

    # obtiene los parámetros de habilidades y disponibilidad
    skills = skills_and_availability_params.get("skills", None)
    availability = skills_and_availability_params.get("availability", None)

    # si se proporcionan habilidades, anade el filtro de habilidades a los parámetros de consulta
    if skills:
        query_params.where.append(Candidate.skills.contains(skills))

    # si se proporciona disponibilidad, anade el filtro de disponibilidad a los parámetros de consulta
    if availability:
        query_params.where.append(Candidate.availability.contains(availability))


async def get_candidate_filter_params(
                                    extra_fields_params: Annotated[set, Depends(_get_extra_fields)],
                                    direction_params: Annotated[bool | None, Depends(_get_direction_params)],
                                    experience_params: Annotated[dict | None, Depends(_get_experience_params)],
                                    language_params: Annotated[dict | None, Depends(_get_language_params)],
                                    education_params: Annotated[dict, Depends(_get_education_params)],
                                    skills_and_availability_params: Annotated[dict, Depends(_get_skills_and_availability_params)],
                                    minimal_fields: Annotated[bool, CANDIDATE_MINIMAL_FIELDS] = False) -> dict:
    """
    Obtiene los parámetros de candidato para filtrar la búsqueda.

    Args:
    - extra_fields_params (set): Conjunto de campos adicionales para incluir en la consulta.
    - direction_params (bool | None): Dirección de los candidatos a filtrar.
    - experience_params (dict | None): Parámetros de experiencia para filtrar los candidatos.
    - language_params (dict | None): Parámetros de idioma para filtrar los candidatos.
    - education_params (dict): Parámetros de formación para filtrar los candidatos.
    - skills_and_availability_params (dict): Parámetros de habilidades y disponibilidad para filtrar los candidatos.
    - minimal_fields (bool, optional): Si se deben incluir los campos mínimos. Por defecto False.

    Returns:
    - dict: Los parámetros finales de la consulta.
    """
    # si se especifica que se deben incluir los campos mínimos, se establecen los campos mínimos
    fields = (Candidate,) if not minimal_fields else (User.id, User.name, User.surname, Address.province, Candidate.skills, Candidate.availability)
    # si se especifica que se deben incluir los campos mínimos, se excluyen los campos de las relaciones
    exclude = "options" if minimal_fields else None
                    
    # se crea el objeto de parámetros de consulta
    query_params = QueryParams(
        fields=fields,
        scalar=not minimal_fields,
        unique=not minimal_fields,
        options = [contains_eager(Candidate.user).contains_eager(User.address)]
    )

    # anadimos los joins de las tablas usuario y dirección ya que siempre se necesitan
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

    # establece los parámetros de consulta pasando los parámetros obtenidos a las funciones correspondientes
    if not minimal_fields:
        # si no se especifica que se deben incluir los campos mínimos, se establecen los campos adicionales a mostrar
        _set_params_extra_field(query_params, extra_fields_params)
    _set_params_dir(query_params, direction_params)
    _set_params_experience(query_params, experience_params)
    _set_params_language(query_params, language_params)
    _set_params_education(query_params, education_params)
    _set_params_skills_and_availability(query_params, skills_and_availability_params)

    # se obtiene el diccionario con los parámetros de consulta excluyendo los parámetros por defecto y el campo options si se especifica que se deben incluir los campos mínimos
    final_query_params = query_params.model_dump(exclude_defaults=True, exclude=exclude)

    return final_query_params

async def get_candidate_applied(extra_fields_params: Annotated[set, Depends(_get_extra_fields_applied_candidates)],
                               direction_params: Annotated[bool | None, Depends(_get_direction_params)],
                               experience_params: Annotated[dict | None, Depends(_get_experience_params)],
                               language_params: Annotated[dict | None, Depends(_get_language_params)],
                               education_params: Annotated[dict, Depends(_get_education_params)],
                               skills_and_availability_params: Annotated[dict, Depends(_get_skills_and_availability_params)],
                               job: Annotated[Job, Depends(GetJob(False))],
                               minimal_fields: Annotated[bool, CANDIDATE_MINIMAL_FIELDS] = False)  -> dict:
    """
    Obtiene los parámetros de búsqueda de candidatos aplicados y devuelve un diccionario con los parámetros de consulta.
    Esta función se usa para filtrar los candidatos aplicados a una oferta, por lo que se incluye el campo de la relación con las ofertas.

    Args:
    - extra_fields_params (set): Conjunto de campos adicionales aplicados a los candidatos.
    - direction_params (bool | None): Parámetro de dirección de búsqueda de candidatos.
    - experience_params (dict | None): Parámetros de experiencia de búsqueda de candidatos.
    - language_params (dict | None): Parámetros de idioma de búsqueda de candidatos.
    - education_params (dict): Parámetros de formación de búsqueda de candidatos.
    - skills_and_availability_params (dict): Parámetros de habilidades y disponibilidad de búsqueda de candidatos.

    Returns:
    - dict: Diccionario con los parámetros de consulta.

    """
    # pasa los parámetros a la función get_candidate_filter_params para obtener los parámetros de consulta
    query_params = await get_candidate_filter_params(extra_fields_params, direction_params, experience_params, language_params, education_params, skills_and_availability_params, minimal_fields)

    # si no hay la key where en los parámetros de consulta, la crea con una lista vacía
    if "where" not in query_params:
        query_params["where"] = []

    # anade el join de la tabla de la relacion de las ofertas y los candidatos
    query_params["joins"].append({
        "target": JobCandidate,
        "onclause": Candidate.user_id == JobCandidate.candidate_id
    })

    # anade el filtro de la oferta a los parámetros de consulta
    query_params["where"].append(JobCandidate.job_id == job.id)

    # anade el orden de los parámetros de consulta para que los candidatos se ordenen por fecha de inscripción
    query_params["order"] = (JobCandidate.inscription_date.desc())

    return query_params
    