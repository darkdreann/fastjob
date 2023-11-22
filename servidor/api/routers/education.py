from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID, uuid4
from typing import Annotated
from sqlalchemy.orm import joinedload, noload
from sqlalchemy import asc
from api.database.database_models.models import Education, EducationLevel, User, Candidate, CandidateEducation, SectorEducation
from api.database.connection import get_session
from api.utils.constants.endpoints_params import LIMIT, OFFSET, EDUCATION_ID, DEFAULT_LIMIT, DEFAULT_OFFSET, EDUCATION_LEVEL_ID, EDUCATION_LEVEL_EXTRA_FIELD
from api.security.permissions import PermissionsManager
from api.models.read_models import ReadLevel, ReadLevelEducation, ReadEducationComplete, ReadEducationCompleteWithCandidates
from api.models.create_models import CreateEducation, CreateLevel
from api.models.update_models import UpdateEducation, UpdateLevel
from api.models.partial_update_models import PartialUpdateEducation, PartialUpdateLevel
from api.utils.functions.management_utils import endpoint_request_log
from api.utils.functions.database_utils import update_model, secure_commit, get_record_by_id, get_database_records
from api.models.enums.endpoints import EducationLevelExtraField

educationRoute = APIRouter(prefix="/educations", tags=["educations"], dependencies=[Depends(endpoint_request_log)])



# GET METHODS #
@educationRoute.get("/", response_model=list[ReadEducationComplete], response_model_exclude_none=True, dependencies=[Depends(PermissionsManager.is_logged)])
async def get_educations(*,
                        session: Annotated[AsyncSession, Depends(get_session)],
                        limit: Annotated[int | None, LIMIT] = DEFAULT_LIMIT,
                        offset: Annotated[int | None, OFFSET] = DEFAULT_OFFSET) -> list[Education]:
    
    """
    Obtiene todas las formaciones con su nivel de formación y sector si lo tiene.
    
    Args:
        session (AsyncSession): La sesión de la base de datos.
        limit (int | None, optional): El límite de registros devueltos. Defaults to DEFAULT_LIMIT.
        offset (int | None, optional): Permite omitir un número específico de registros en el conjunto de resultados. Defaults to DEFAULT_OFFSET.
        
    Returns:
        list[Education]: La lista de formaciones.
    """

    educations = await get_database_records(session, Education, limit=limit, offset=offset)

    return educations

from sqlalchemy import select

@educationRoute.get("/education-levels/", response_model=list[ReadLevel], dependencies=[Depends(PermissionsManager.is_logged)])
async def get_education_levels(*,
                            session: Annotated[AsyncSession, Depends(get_session)], 
                            limit: Annotated[int | None, LIMIT] = DEFAULT_LIMIT,
                            offset: Annotated[int | None, OFFSET] = DEFAULT_OFFSET) -> list[EducationLevel]:
    """
    Obtiene todos los niveles de formación.

    Args:
        session (AsyncSession): La sesión de la base de datos.
        limit (int | None, optional): El límite de registros devueltos. Defaults to DEFAULT_LIMIT.
        offset (int | None, optional): Permite omitir un número específico de registros en el conjunto de resultados. Defaults to DEFAULT_OFFSET.

    Returns:
        list[EducationLevel]: La lista de niveles de formación.
    """
    
    education_levels = await get_database_records(session, EducationLevel, limit=limit, offset=offset, order=asc(EducationLevel.value))

    return education_levels


@educationRoute.get("/admin/", response_model=list[ReadEducationCompleteWithCandidates], response_model_exclude_none=True, response_model_exclude_defaults=True, dependencies=[Depends(PermissionsManager.is_admin)])
async def get_educations_with_candidates(*,
                        session: Annotated[AsyncSession, Depends(get_session)], 
                        limit: Annotated[int | None, LIMIT] = DEFAULT_LIMIT,
                        offset: Annotated[int | None, OFFSET] = DEFAULT_OFFSET) -> list[Education]:
    
    """
    Obtiene una lista de todas las educaciones con sus candidatos asociados.

    Args:
        session (AsyncSession): Sesión de base de datos.
        limit (int | None, optional): Límite de resultados. Defaults to DEFAULT_LIMIT.
        offset (int | None, optional): Desplazamiento de resultados. Defaults to DEFAULT_OFFSET.

    Returns:
        list[Education]: Lista de educaciones con sus candidatos asociados.
    """

    joined_load = joinedload(Education.candidates_list).defaultload(CandidateEducation.candidate).joinedload(Candidate.user).joinedload(User.adress)

    educations = await get_database_records(session, Education, options=joined_load, limit=limit, offset=offset, unique = True)

    return educations


@educationRoute.get("/admin/education-levels/", response_model=list[ReadLevelEducation], response_model_exclude_defaults=True, dependencies=[Depends(PermissionsManager.is_admin)])
async def get_education_levels(*,
                            session: Annotated[AsyncSession, Depends(get_session)], 
                            limit: Annotated[int | None, LIMIT] = DEFAULT_LIMIT,
                            offset: Annotated[int | None, OFFSET] = DEFAULT_OFFSET,
                            extra_fields: Annotated[set[EducationLevelExtraField], EDUCATION_LEVEL_EXTRA_FIELD] = ()) -> list[EducationLevel]:
    """
    Obtiene los niveles de educación. Si se especifican campos extra, se obtienen los campos de las relaciones especificadas.

    Args:
        session (AsyncSession): Sesión de base de datos.
        limit (int | None, optional): Límite de resultados. Defaults to DEFAULT_LIMIT.
        offset (int | None, optional): Desplazamiento de resultados. Defaults to DEFAULT_OFFSET.
        extra_fields (set[EducationLevelExtraField], optional): Campos extra de nivel de educación. Defaults to ().

    Returns:
        list[EducationLevel]: Lista de niveles de educación.
    """
    
    education_levels = await get_database_records(session, EducationLevel, limit=limit, offset=offset, options=[EducationLevelExtraField.get_field_value(field) for field in extra_fields], order=asc(EducationLevel.value), unique=True)

    return education_levels


@educationRoute.get("/admin/education-levels/{education_level_id}/", response_model=ReadLevelEducation, response_model_exclude_defaults=True, dependencies=[Depends(PermissionsManager.is_admin)])
async def get_education_levels(*,
                            session: Annotated[AsyncSession, Depends(get_session)], 
                            education_level_id: Annotated[UUID, EDUCATION_LEVEL_ID],
                            extra_fields: Annotated[set[EducationLevelExtraField], EDUCATION_LEVEL_EXTRA_FIELD] = ()) -> EducationLevel:
    """
    Obtiene un nivel de educación por su ID. Si se especifican campos extra, se obtienen los campos de las relaciones especificadas.

    Args:
        session (AsyncSession): Sesión de base de datos.
        education_level_id (UUID): ID del nivel de educación.
        extra_fields (set[EducationLevelExtraField], optional): Campos extra del nivel de educación. Por defecto, no se incluyen.

    Returns:
        EducationLevel: Nivel de educación.
    """
    
    education_level: EducationLevel = await get_record_by_id(session, EducationLevel, education_level_id, options=[EducationLevelExtraField.get_field_value(field) for field in extra_fields])

    return education_level




@educationRoute.get("/education-levels/{education_level_id}/", response_model=ReadLevel, dependencies=[Depends(PermissionsManager.is_logged)])
async def get_education_levels(*,
                            session: Annotated[AsyncSession, Depends(get_session)], 
                            education_level_id: Annotated[UUID, EDUCATION_LEVEL_ID]) -> EducationLevel:
    """
    Obtiene un nivel de educación por su ID.

    Args:
        session (AsyncSession): Sesión de base de datos.
        education_level_id (UUID): ID del nivel de educación.

    Returns:
        EducationLevel: El nivel de educación solicitado.
    """
    
    education_level: EducationLevel = await get_record_by_id(session, EducationLevel, education_level_id)

    return education_level



@educationRoute.get("/admin/{education_id}/", response_model=ReadEducationCompleteWithCandidates, response_model_exclude_none=True, response_model_exclude_defaults=True, dependencies=[Depends(PermissionsManager.is_admin)])
async def get_education_with_candidates(*,
               session: Annotated[AsyncSession, Depends(get_session)], 
               education_id: Annotated[UUID, EDUCATION_ID]) -> Education:
    """
    Obtiene una educación con sus candidatos por su ID.

    Args:
        session (AsyncSession): Sesión de base de datos.
        education_id (UUID): ID de la educación.

    Returns:
        Education: Educación con sus candidatos.
    """
    joined_load = joinedload(Education.candidates_list).defaultload(CandidateEducation.candidate).joinedload(Candidate.user).joinedload(User.adress)

    education: Education = await get_record_by_id(session, Education, education_id, options=joined_load)

    return education


@educationRoute.get("/{education_id}/", response_model=ReadEducationComplete, response_model_exclude_none=True, dependencies=[Depends(PermissionsManager.is_logged)])
async def get_education(*,
                        session: Annotated[AsyncSession, Depends(get_session)], 
                        education_id: Annotated[UUID, EDUCATION_ID]) -> Education:
    """
    Obtiene una educación por su ID.

    Args:
        session (AsyncSession): La sesión de base de datos.
        education_id (UUID): El ID de la educación.

    Returns:
        Education: La educación encontrada.
    """

    education: Education = await get_record_by_id(session, Education, education_id)

    return education



# POST METHODS #
@educationRoute.post("/", response_model=ReadEducationComplete, status_code=status.HTTP_201_CREATED, dependencies=[Depends(PermissionsManager.is_admin)], response_model_exclude_none=True)
async def create_education(*,
                            session: Annotated[AsyncSession, Depends(get_session)],
                            new_education: CreateEducation) -> Education:
    """
    Crea una nueva educación en la base de datos.

    Args:
        session (AsyncSession): Sesión de base de datos.
        new_education (CreateEducation): Datos de la educación a crear.

    Returns:
        Education: La educación creada.
    """
    
    education_dict = new_education.model_dump()
    education_dict["id"] = uuid4()

    sector_id = education_dict.pop("sector_id", None)

    new_database_education = Education(**education_dict)

    session.add(new_database_education)

    if sector_id:
        new_sector_education = SectorEducation(education_id=new_database_education.id, sector_id=sector_id)
        session.add(new_sector_education)

    await secure_commit(session)

    await session.refresh(new_database_education, ["sector", "level"])

    return new_database_education
        

@educationRoute.post("/education-levels/", response_model=ReadLevel, status_code=status.HTTP_201_CREATED, dependencies=[Depends(PermissionsManager.is_admin)])
async def create_education_level(*,
                                session: Annotated[AsyncSession, Depends(get_session)], 
                                new_education: CreateLevel) -> EducationLevel:
    """
    Crea un nuevo nivel educativo en la base de datos.

    Args:
        session (AsyncSession): Sesión de base de datos.
        new_education (CreateLevel): Datos del nuevo nivel educativo.

    Returns:
        EducationLevel: El nivel educativo creado.
    """
    education_level = EducationLevel(**new_education.model_dump())

    session.add(education_level)

    await secure_commit(session)

    return education_level


# PUT METHODS #

@educationRoute.put("/education-levels/{education_level_id}/", response_model=ReadLevel, dependencies=[Depends(PermissionsManager.is_admin)])
async def update_education_level(*,
                            session: Annotated[AsyncSession, Depends(get_session)], 
                            education_level_id: Annotated[UUID, EDUCATION_LEVEL_ID],
                            education_update: UpdateLevel) -> EducationLevel:
    """
    Actualiza un nivel educativo existente en la base de datos.

    Args:
        session (AsyncSession): Sesión de base de datos.
        education_level_id (UUID): ID del nivel educativo a actualizar.
        education_update (UpdateLevel): Datos actualizados del nivel educativo.

    Returns:
        EducationLevel: El nivel educativo actualizado.
    """
    
    education_level_to_update: EducationLevel = await get_record_by_id(session, EducationLevel, education_level_id)

    update_model(education_level_to_update, education_update.model_dump())

    await secure_commit(session)

    return education_level_to_update


@educationRoute.put("/{education_id}/", response_model=ReadEducationComplete, dependencies=[Depends(PermissionsManager.is_admin)])
async def update_education(*,
                            session: Annotated[AsyncSession, Depends(get_session)], 
                            education_id: Annotated[UUID, EDUCATION_ID],
                            education_update: UpdateEducation) -> Education:
    """
    Actualiza una educación existente en la base de datos.

    Args:
        session (AsyncSession): Sesión de base de datos.
        education_id (UUID): ID de la educación a actualizar.
        education_update (UpdateEducation): Datos de la educación actualizada.

    Returns:
        Education: La educación actualizada.
    """
    
    update_education_dict = education_update.model_dump()
    sector_id = update_education_dict.pop("sector_id", None)

    education_to_update: Education = await get_record_by_id(session, Education, education_id)

    update_model(education_to_update, update_education_dict)

    if sector_id:
        if education_to_update.sector is not None:
            education_to_update.sector.sector_id = sector_id
        else:
            new_sector_education = SectorEducation(education_id=education_to_update.id, sector_id=sector_id)
            session.add(new_sector_education)

    await secure_commit(session)

    await session.refresh(education_to_update, ["sector", "level"])

    return education_to_update



# PATCH METHODS #

@educationRoute.patch("/education-levels/{education_level_id}/", response_model=ReadLevel, dependencies=[Depends(PermissionsManager.is_admin)])
async def partial_update_education_level(*,
                                        session: Annotated[AsyncSession, Depends(get_session)], 
                                        education_level_id: Annotated[UUID, EDUCATION_LEVEL_ID],
                                        education_update: PartialUpdateLevel) -> EducationLevel:
    """
    Actualiza parcialmente un nivel educativo existente en la base de datos.

    Args:
        session (AsyncSession): sesión de base de datos.
        education_level_id (UUID): id del nivel educativo a actualizar.
        education_update (PartialUpdateLevel): modelo de actualización parcial.

    Returns:
        EducationLevel: el nivel educativo actualizado.
    """
    education_level_to_update: EducationLevel = await get_record_by_id(session, EducationLevel, education_level_id)

    update_model(education_level_to_update, education_update.model_dump(exclude_unset=True))

    await secure_commit(session)

    return education_level_to_update


@educationRoute.patch("/{education_id}/", response_model=ReadEducationComplete, dependencies=[Depends(PermissionsManager.is_admin)], response_model_exclude_none=True)
async def partial_update_education(*,
                                    session: Annotated[AsyncSession, Depends(get_session)], 
                                    education_id: Annotated[UUID, EDUCATION_ID],
                                    education_update: PartialUpdateEducation) -> Education:
    """
    Actualiza parcialmente una educación existente en la base de datos.

    Args:
        session (AsyncSession): sesión de base de datos.
        education_id (UUID): id de la educación a actualizar.
        education_update (PartialUpdateEducation): objeto que contiene los campos a actualizar.

    Returns:
        Education: objeto de la educación actualizada.
    """
    
    update_education_dict = education_update.model_dump(exclude_unset=True)

    sector_id = update_education_dict.pop("sector_id", None)

    education_to_update: Education = await get_record_by_id(session, Education, education_id)

    update_model(education_to_update, update_education_dict)

    if sector_id:
        if education_to_update.sector is not None:
            education_to_update.sector.sector_id = sector_id
        else:
            new_sector_education = SectorEducation(education_id=education_to_update.id, sector_id=sector_id)
            session.add(new_sector_education)

    await secure_commit(session)

    await session.refresh(education_to_update, ["sector", "level"])

    return education_to_update



# DELETE METHODS #

@educationRoute.delete("/education-levels/{education_level_id}/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(PermissionsManager.is_admin)])
async def delete_education_level(*,
                                session: Annotated[AsyncSession, Depends(get_session)],
                                education_level_id: Annotated[UUID, EDUCATION_LEVEL_ID]) -> None:
    """
    Elimina un nivel educativo de la base de datos.

    Args:
        session (AsyncSession): sesión de base de datos.
        education_level_id (UUID): id del nivel educativo a eliminar.
    """

    education_level_to_delete: EducationLevel = await get_record_by_id(session, EducationLevel, education_level_id)

    await session.delete(education_level_to_delete)

    await secure_commit(session)


@educationRoute.delete("/{education_id}/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(PermissionsManager.is_admin)])
async def delete_education(*,
                            session: Annotated[AsyncSession, Depends(get_session)], 
                            education_id: Annotated[UUID, EDUCATION_ID]) -> None:
    """
    Elimina un registro de educación de la base de datos.

    Args:
        session (AsyncSession): sesión de base de datos.
        education_id (UUID): id de la educación a eliminar.
    """
    education_to_delete: Education = await get_record_by_id(session, Education, education_id, options=(noload(Education.level), noload(Education.sector)))

    await session.delete(education_to_delete)

    await secure_commit(session)

