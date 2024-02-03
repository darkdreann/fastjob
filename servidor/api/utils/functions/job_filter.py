from uuid import UUID
from typing import Annotated
from fastapi import Depends
from sqlalchemy import or_
from sqlalchemy.orm import contains_eager
from fastapi.exceptions import RequestValidationError
from api.models.base_models import QueryParams
from api.database.database_models.models import Job
from api.database.database_models.models import Address, Sector, Language, Education, EducationLevel, JobLanguage, JobEducation
from api.utils.constants.error_strings import INVALID_EDUCATION_PARAMS_FOR_JOBS, INVALID_CANDIDATE_SECTOR_PARAMS
from api.utils.constants.endpoints_params import KEYWORD, LANGUAGE_CANDIDATE, SECTOR_CATEGORY_QUERY, EDUCATION_NAME_PARAM, SECTOR_ID_QUERY, ADDRESS_PROVINCE, EDUCATION_LEVEL_VALUE_PARAM, JOB_ACTIVE, JOB_MINIMAL_FIELDS

async def _get_sector_params(sector_category: Annotated[str | None, SECTOR_CATEGORY_QUERY] = None,
                             sector_id: Annotated[UUID | None, SECTOR_ID_QUERY] = None) -> str | None:
    """
    Obtiene los parámetros del sector para la consulta.
    No se pueden pasar ambos parámetros.

    Args:
    - sector_category (str | None): La categoría del sector.
    - sector_id (UUID | None): El ID del sector.

    Returns:
    - str | None: Los parámetros del sector.

    Raises:
    - RequestValidationError: Si se pasan ambos parámetros.
    """

    # Si se pasan ambos parámetros, se lanza una excepción.
    if sector_category and sector_id: raise RequestValidationError([INVALID_CANDIDATE_SECTOR_PARAMS])
    
    # Si se pasa la categoría del sector, se devuelve la categoría.
    if sector_category:
        return sector_category
    
    # Si se pasa el ID del sector, se devuelve el ID.
    if sector_id:
        return sector_id
    
async def _get_province_param(province: Annotated[str | None, ADDRESS_PROVINCE] = None) -> str | None:
    """
    Obtiene el parámetro de provincia para la consulta.

    Args:
    - province (str | None): La provincia a filtrar.

    Returns:
    - str | None: El parámetro de provincia en minúsculas o None si no se proporciona ninguna provincia.
    """

    # si se pasa la provincia, se devuelve la provincia en minúsculas.
    if province:
        return province.lower()
    
async def _get_keyword_param(keyword: Annotated[str | None, KEYWORD] = None) -> str | None:
    """
    Obtiene el parámetro de palabra clave para la consulta.

    Args:
    - keyword (str | None, optional): La palabra clave a filtrar. Defaults to None.

    Returns:
    - str | None: El parámetro de palabra clave en minúsculas o None si no se proporciona ninguna palabra clave.
    """

    # si se pasa la palabra clave, se devuelve la palabra clave en minúsculas.
    if keyword:
        return keyword.lower()
    
async def _get_education_params(education_name: Annotated[str | None, EDUCATION_NAME_PARAM] = None,
                                education_level_value: Annotated[int | None, EDUCATION_LEVEL_VALUE_PARAM] = None) -> dict | None:
    """
    Obtiene los parámetros de educación para la consulta.
    No se pueden pasar ambos parámetros.

    Args:
    - education_name (str | None, optional): El nombre de la educación. Defaults to None.
    - education_level_value (int | None, optional): El valor del nivel de educación. Defaults to None.

    Returns:
    - dict | None: Los parámetros de educación para la consulta.

    Raises:
    - RequestValidationError: Si se pasan ambos parámetros.
    """

    # Si se pasan ambos parámetros, se lanza una excepción.
    if education_name and education_level_value: raise RequestValidationError([INVALID_EDUCATION_PARAMS_FOR_JOBS])
    # Si no se pasa ninguno de los dos parámetros, se devuelve None.
    if not education_name and not education_level_value: return None

    # Se pasan los parámetros de educación a un diccionario, convirtiendo el nombre de la educación a minúsculas si se proporciona.
    education_params = {
        "education_name": education_name.lower() if education_name else None,
        "education_level": education_level_value
    }

    return education_params
 
async def _get_language_params(languages: Annotated[set[str | UUID], LANGUAGE_CANDIDATE] = ()) -> set[str | UUID] | None:
    """
    Obtiene los parámetros de idioma para filtrar candidatos.

    Args:
    - language (str | UUID, optional): El idioma o el identificador UUID del idioma. Defaults to None.

    Returns:
    - str | UUID | None: El identificador UUID del idioma o el nombre del idioma en minúsculas.
    """
    
    # Si no se pasa ningún parámetro, se devuelve None.
    if not languages: return None

    # Se crea un conjunto vacío para almacenar los parámetros de idioma.
    final_languages = set()

    # Se recorren los parámetros de idioma.
    for language in languages:
        # Si el parámetro es un UUID válido, se añade al conjunto de parámetros de idioma.
        try:
            final_languages.add(UUID(language))
        # Si no es un UUID válido, se añade el nombre del idioma en minúsculas al conjunto de parámetros de idioma.
        except:
            final_languages.add(language.lower())

    return languages


def _set_sector_filter_query(query_params: QueryParams, sector_param: str | UUID | None) -> None:
    """
    Establece los parámetros de consulta para filtrar por sector.

    Args:
    - query_params (QueryParams): Los parámetros de consulta.
    - sector_param (str | UUID | None): El parámetro de sector.
    """

    # Si no se pasa ningún parámetro, termina la función.
    if not sector_param: return

    # se anade al join el sector.
    query_params.add_join({
        "target": Sector,
        "onclause": Sector.id == Job.sector_id
    })

    # se anade las opciones de loading para reconstruir el objeto.
    query_params.options.append(contains_eager(Job.sector))

    # obtenemos el campo de sector a filtrar.
    sector_field = Sector.id if isinstance(sector_param, UUID) else Sector.category

    # se anade el filtro de sector.
    query_params.where.append(sector_field == sector_param)

def _set_province_filter_query(query_params: QueryParams, province_param: str | None) -> None:
    """
    Establece los parámetros de consulta para filtrar por provincia.

    Args:
    - query_params (QueryParams): Los parámetros de la consulta.
    - province_param (str | None): El parámetro de provincia.
    """

    # Si no se pasa ningún parámetro, termina la función.
    if not province_param: return

    # se anade al join la dirección.
    query_params.add_join({
        "target": Address,
        "onclause": Address.id == Job.address_id
    })

    # se anade las opciones de loading para reconstruir el objeto.
    query_params.options.append(contains_eager(Job.address))

    # se anade el filtro de provincia.
    query_params.where.append(Address.province == province_param)


def _set_keyword_filter_query(query_params: QueryParams, keyword_param: str | None) -> None:
    """
    Establece el filtro de palabra clave en la consulta.

    Args:
    - query_params (QueryParams): Los parámetros de la consulta.
    - keyword_param (str | None): El parámetro de palabra clave.
    """

    # Si no se pasa ningún parámetro, termina la función.
    if not keyword_param: return

    # se anade el filtro de palabra clave. Que el título o la descripción contengan la palabra clave.
    query_params.where.append(or_(Job.title.contains(keyword_param), Job.description.contains(keyword_param)))

def _set_education_filter_query(query_params: QueryParams, education_params: dict | None) -> None:
    """
    Establece los parámetros de consulta para filtrar por educación.

    Args:
    - query_params (QueryParams): Los parámetros de consulta.
    - education_params (dict | None): Los parámetros de educación.
    """

    # Si no se pasa ningún parámetro, termina la función.
    if not education_params: return

    # Se obtienen los parámetros de educación.
    education_name = education_params.get("education_name", None)
    education_level = education_params.get("education_level", None)

    # Se anade al join la educación.
    query_params.add_join_list((
        {
            "target": JobEducation,
            "onclause": JobEducation.job_id == Job.id,
        },
        {
            "target": Education,
            "onclause": Education.id == JobEducation.education_id
        },
        {
            "target": EducationLevel,
            "onclause": EducationLevel.id == Education.level_id
        }
    ))

    # Se anaden las opciones de loading para reconstruir el objeto.
    query_params.options.append(contains_eager(Job.required_education).contains_eager(JobEducation.education).contains_eager(Education.level))

    # si se ha pasado el nombre de la educación, se anade el filtro de nombre de educación.
    if education_name:
        query_params.where.append(Education.qualification.contains(education_name))
    
    # si se ha pasado el nivel de educación, se anade el filtro de nivel de educación.
    if education_level:
        query_params.where.append(EducationLevel.value <= education_level)

def _set_language_filter_query(query_params: QueryParams, language_params: set[str | UUID] | None) -> None:
    """
    Establece la consulta de filtro de idioma en los parámetros de consulta.

    Args:
    - query_params (QueryParams): Los parámetros de consulta.
    - language_params (set[str | UUID] | None): Los parámetros de idioma.
    """
    
    # Si no se pasa ningún parámetro, termina la función.
    if not language_params: return
    
    # Se anade al join el idioma.
    query_params.add_join_list((
        {
            "target": JobLanguage,
            "onclause": JobLanguage.job_id == Job.id
        },
        {
            "target": Language,
            "onclause": Language.id == JobLanguage.language_id
        }
    ))
    
    # Se anaden las opciones de loading para reconstruir el objeto.
    query_params.options.append(contains_eager(Job.language_list).contains_eager(JobLanguage.language))
    
    # Se obtiene el campo de idioma a filtrar.
    language_field = Language.id if isinstance(language_params, UUID) else Language.name
    
    # Se anade el filtro de idioma.
    for param in language_params:
        query_params.where.append(language_field == param)


async def get_job_filter_params(
                                sector: Annotated[str | None, Depends(_get_sector_params)],
                                province: Annotated[str | None, Depends(_get_province_param)],
                                keyword: Annotated[str | None, Depends(_get_keyword_param)],
                                education: Annotated[dict | None, Depends(_get_education_params)],
                                language: Annotated[set[str|UUID]|None, Depends(_get_language_params)],
                                active: Annotated[bool, JOB_ACTIVE] = True,
                                minimal_fields: Annotated[bool, JOB_MINIMAL_FIELDS] = False) -> dict:
    """
    Obtiene los parámetros de filtro para la búsqueda de ofertas de empleo.
    
    Args:
    - sector (str | None): El sector de los empleos a filtrar.
    - province (str | None): La provincia de los empleos a filtrar.
    - keyword (str | None): La palabra clave para buscar en los empleos.
    - education (dict | None): El nivel de educación requerido para los empleos.
    - language (set[str|UUID] | None): El idioma requerido para los empleos.
    - active (bool, optional): Indica si se deben filtrar solo los empleos activos. Defaults to True.
    - minimal_fields (bool, optional): Indica si se deben devolver solo los campos mínimos de los empleos. Defaults to False.

    Returns:
    - dict: Los parámetros de filtro para la búsqueda de empleos.
    """
    
    # Si se piden los campos mínimos, se establecen los campos mínimos y se excluyen las opciones de loading.
    fields = (Job,) if not minimal_fields else (Job.id, Job.title, Job.description, Address.province)
    exclude = "options" if minimal_fields else None

    # Se crean los parámetros de consulta.
    query_params = QueryParams(
        fields = fields, 
        scalar = not minimal_fields,
        unique = not minimal_fields  
    )

    # si se piden los campos mínimos, se anade al join la dirección. Ya que se usa la provincia.
    if minimal_fields:
        query_params.add_join({
            "target": Address,
            "onclause": Address.id == Job.address_id
        })

    # establece los parámetros de consulta pasando los parámetros obtenidos a las funciones correspondientes
    _set_sector_filter_query(query_params, sector)
    _set_province_filter_query(query_params, province)
    _set_keyword_filter_query(query_params, keyword)
    _set_education_filter_query(query_params, education)
    _set_language_filter_query(query_params, language)

    # si solo se quieren los empleos activos, se anade el filtro de empleos activos.
    if active:
        query_params.where.append(Job.active == active)

    # se obtienen los parámetros de consulta.
    final_query = query_params.model_dump(exclude_defaults=True, exclude=exclude)

    return final_query



    