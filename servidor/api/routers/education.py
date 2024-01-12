from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID, uuid4
from typing import Annotated
from sqlalchemy.orm import joinedload, noload
from api.database.database_models.models import Education, EducationLevel, SectorEducation
from api.database.connection import get_session
from api.utils.constants.endpoints_params import LIMIT, OFFSET, EDUCATION_ID, DEFAULT_LIMIT, DEFAULT_OFFSET, EDUCATION_LEVEL_ID, GET_EDUCATION, EDUCATION_EXTRA_FIELD
from api.security.permissions import PermissionsManager
from api.models.read_models import ReadLevel, ReadLevelEducation, ReadEducationComplete, ReadEducationWithUses
from api.models.create_models import CreateEducation, CreateLevel
from api.models.update_models import UpdateEducation, UpdateLevel
from api.models.partial_update_models import PartialUpdateEducation, PartialUpdateLevel
from api.utils.functions.management_utils import endpoint_request_log
from api.utils.functions.database_utils import secure_commit, get_record_by_id, get_database_records
from api.utils.functions.models_utils import update_model
from api.models.enums.endpoints import EducationExtraField

education_route = APIRouter(prefix="/educations", tags=["educations"], dependencies=[Depends(endpoint_request_log)])

# GET METHODS #
@education_route.get("/", response_model=list[ReadEducationComplete], response_model_exclude_none=True, dependencies=[Depends(PermissionsManager.is_logged)])
async def get_educations(*,
                        session: Annotated[AsyncSession, Depends(get_session)],
                        limit: Annotated[int, LIMIT] = DEFAULT_LIMIT,
                        offset: Annotated[int, OFFSET] = DEFAULT_OFFSET) -> list[Education]:
    
    """
    Obtiene todas las formaciones con su nivel de formación y sector si lo tiene.
    Se debe estar logueado para poder acceder a este endpoint.
    
    Args:
        session (AsyncSession): La sesión de la base de datos.
        limit (int, optional): El límite de registros devueltos. Por defecto es DEFAULT_LIMIT.
        offset (int, optional): Permite omitir un número específico de registros en el conjunto de resultados. Por defecto es DEFAULT_OFFSET.
        
    Returns:
        list[Education]: La lista de formaciones.
    """

    educations = await get_database_records(session, Education, limit=limit, offset=offset)

    return educations

@education_route.get("/education-levels/", response_model=list[ReadLevel], dependencies=[Depends(PermissionsManager.is_logged)])
async def get_education_levels(*,
                            session: Annotated[AsyncSession, Depends(get_session)], 
                            limit: Annotated[int, LIMIT] = DEFAULT_LIMIT,
                            offset: Annotated[int, OFFSET] = DEFAULT_OFFSET) -> list[EducationLevel]:
    """
    Obtiene todos los niveles de formación.
    Se debe estar logueado para poder acceder a este endpoint.

    Args:
        session (AsyncSession): La sesión de la base de datos.
        limit (int, optional): El límite de registros devueltos. Defaults to DEFAULT_LIMIT.
        offset (int, optional): Permite omitir un número específico de registros en el conjunto de resultados. Defaults to DEFAULT_OFFSET.

    Returns:
        list[EducationLevel]: La lista de niveles de formación.
    """
    
    education_levels = await get_database_records(session, EducationLevel, limit=limit, offset=offset, order_by=EducationLevel.value.asc())

    return education_levels


@education_route.get("/admin/", response_model=list[ReadEducationWithUses], response_model_exclude_none=True, response_model_exclude_defaults=True, dependencies=[Depends(PermissionsManager.is_admin)])
async def get_educations_with_candidates(*,
                        session: Annotated[AsyncSession, Depends(get_session)], 
                        limit: Annotated[int, LIMIT] = DEFAULT_LIMIT,
                        offset: Annotated[int, OFFSET] = DEFAULT_OFFSET,
                        extra_fields: Annotated[set[EducationExtraField], EDUCATION_EXTRA_FIELD]) -> list[Education]:
    
    """
    Obtiene una lista de todas las educaciones con sus candidatos asociados.
    Se debe ser administrador para poder acceder a este endpoint.

    Args:
        session (AsyncSession): Sesión de base de datos.
        limit (int, optional): Límite de resultados. Defaults to DEFAULT_LIMIT.
        offset (int, optional): Desplazamiento de resultados. Defaults to DEFAULT_OFFSET.
        extra_fields (set[EducationExtraField]): Campos extra que se quieren obtener.

    Returns:
        list[Education]: Lista de educaciones con sus candidatos asociados.
    """


    educations = await get_database_records(session, Education, options=[EducationExtraField.get_field_value(field) for field in extra_fields], limit=limit, offset=offset, unique = True)

    return educations


@education_route.get("/admin/education-levels/", response_model=list[ReadLevelEducation], response_model_exclude_defaults=True, dependencies=[Depends(PermissionsManager.is_admin)])
async def get_education_levels(*,
                            session: Annotated[AsyncSession, Depends(get_session)], 
                            limit: Annotated[int, LIMIT] = DEFAULT_LIMIT,
                            offset: Annotated[int, OFFSET] = DEFAULT_OFFSET,
                            get_educations: Annotated[bool, GET_EDUCATION] = False) -> list[EducationLevel]:
    """
    Obtiene los niveles de formación. Si se especifican campos extra, se obtienen los campos de las relaciones especificadas.
    Se debe ser administrador para poder acceder a este endpoint.

    Args:
        session (AsyncSession): Sesión de base de datos.
        limit (int, optional): Límite de resultados. Defaults to DEFAULT_LIMIT.
        offset (int, optional): Desplazamiento de resultados. Defaults to DEFAULT_OFFSET.
        get_educations (bool, optional): Si se quieren obtener las educaciones asociadas. Defaults to False.

    Returns:
        list[EducationLevel]: Lista de niveles de formación.
    """
    options = joinedload(EducationLevel.education_list) if get_educations else None
    
    education_levels = await get_database_records(session, EducationLevel, limit=limit, offset=offset, options=options, order_by=EducationLevel.value.asc(), unique=True)

    return education_levels


@education_route.get("/admin/education-levels/{education_level_id}/", response_model=ReadLevelEducation, response_model_exclude_defaults=True, dependencies=[Depends(PermissionsManager.is_admin)])
async def get_education_levels(*,
                            session: Annotated[AsyncSession, Depends(get_session)], 
                            education_level_id: Annotated[UUID, EDUCATION_LEVEL_ID],
                            get_educations: Annotated[bool, GET_EDUCATION] = False) -> EducationLevel:
    """
    Obtiene un nivel de formación por su ID. Si se especifican campos extra, se obtienen los campos de las relaciones especificadas.
    Se debe ser administrador para poder acceder a este endpoint.

    Args:
        session (AsyncSession): Sesión de base de datos.
        education_level_id (UUID): ID del nivel de formación.
        get_educations (bool, optional): Si se quieren obtener las educaciones asociadas. Defaults to False.

    Returns:
        EducationLevel: Nivel de formación.
    """
    options = joinedload(EducationLevel.education_list) if get_educations else None
    
    education_level: EducationLevel = await get_record_by_id(session, EducationLevel, education_level_id, options=options)

    return education_level




@education_route.get("/education-levels/{education_level_id}/", response_model=ReadLevel, dependencies=[Depends(PermissionsManager.is_logged)])
async def get_education_levels(*,
                            session: Annotated[AsyncSession, Depends(get_session)], 
                            education_level_id: Annotated[UUID, EDUCATION_LEVEL_ID]) -> EducationLevel:
    """
    Obtiene un nivel de formación por su ID.
    Se debe estar logueado para poder acceder a este endpoint.

    Args:
        session (AsyncSession): Sesión de base de datos.
        education_level_id (UUID): ID del nivel de formación.

    Returns:
        EducationLevel: El nivel de formación solicitado.
    """
    
    education_level: EducationLevel = await get_record_by_id(session, EducationLevel, education_level_id)

    return education_level



@education_route.get("/admin/{education_id}/", response_model=ReadEducationWithUses, response_model_exclude_none=True, response_model_exclude_defaults=True, dependencies=[Depends(PermissionsManager.is_admin)])
async def get_education_with_candidates(*,
                                        session: Annotated[AsyncSession, Depends(get_session)], 
                                        education_id: Annotated[UUID, EDUCATION_ID],
                                        extra_fields: Annotated[set[EducationExtraField], EDUCATION_EXTRA_FIELD]) -> Education:
    """
    Obtiene una formación con sus candidatos por su ID.
    Se debe ser administrador para poder acceder a este endpoint.

    Args:
        session (AsyncSession): Sesión de base de datos.
        education_id (UUID): ID de la formación.
        extra_fields (set[EducationExtraField]): Campos extra que se quieren obtener.

    Returns:
        Education: Educación con sus candidatos.
    """

    education: Education = await get_record_by_id(session, Education, education_id, options=[EducationExtraField.get_field_value(field) for field in extra_fields])

    return education


@education_route.get("/{education_id}/", response_model=ReadEducationComplete, response_model_exclude_none=True, dependencies=[Depends(PermissionsManager.is_logged)])
async def get_education(*,
                        session: Annotated[AsyncSession, Depends(get_session)], 
                        education_id: Annotated[UUID, EDUCATION_ID]) -> Education:
    """
    Obtiene una formación por su ID.
    Se debe estar logueado para poder acceder a este endpoint.

    Args:
        session (AsyncSession): La sesión de base de datos.
        education_id (UUID): El ID de la formación.

    Returns:
        Education: La formación encontrada.
    """

    education: Education = await get_record_by_id(session, Education, education_id)

    return education



# POST METHODS #
@education_route.post("/", response_model=ReadEducationComplete, status_code=status.HTTP_201_CREATED, response_model_exclude_none=True, dependencies=[Depends(PermissionsManager.is_admin)])
async def create_education(*,
                            session: Annotated[AsyncSession, Depends(get_session)],
                            new_education: CreateEducation) -> Education:
    """
    Crea una nueva formación en la base de datos.'
    Se debe ser administrador para poder acceder a este endpoint.

    Args:
        session (AsyncSession): Sesión de base de datos.
        new_education (CreateEducation): Datos de la formación a crear.

    Returns:
        Education: La formación creada.
    """
    
    # obtenemos el diccionario de la formación y le añadimos un id
    education_dict = new_education.model_dump()
    education_dict["id"] = uuid4()

    # obtenemos el sector_id y lo eliminamos del diccionario
    sector_id = education_dict.pop("sector_id", None)

    new_database_education = Education(**education_dict)

    session.add(new_database_education)

    # si se ha especificado un sector, lo añadimos a la tabla relacion de sector y educacion
    if sector_id:
        new_sector_education = SectorEducation(education_id=new_database_education.id, sector_id=sector_id)
        session.add(new_sector_education)

    await secure_commit(session)

    await session.refresh(new_database_education, ["sector", "level"])

    return new_database_education
        

@education_route.post("/education-levels/", response_model=ReadLevel, status_code=status.HTTP_201_CREATED, dependencies=[Depends(PermissionsManager.is_admin)])
async def create_education_level(*,
                                session: Annotated[AsyncSession, Depends(get_session)], 
                                new_education: CreateLevel) -> EducationLevel:
    """
    Crea un nuevo nivel educativo en la base de datos.
    Se debe ser administrador para poder acceder a este endpoint.

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

@education_route.put("/education-levels/{education_level_id}/", response_model=ReadLevel, dependencies=[Depends(PermissionsManager.is_admin)])
async def update_education_level(*,
                            session: Annotated[AsyncSession, Depends(get_session)], 
                            education_level_id: Annotated[UUID, EDUCATION_LEVEL_ID],
                            education_update: UpdateLevel) -> EducationLevel:
    """
    Actualiza un nivel educativo existente en la base de datos.
    Se debe ser administrador para poder acceder a este endpoint.

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


@education_route.put("/{education_id}/", response_model=ReadEducationComplete, dependencies=[Depends(PermissionsManager.is_admin)])
async def update_education(*,
                            session: Annotated[AsyncSession, Depends(get_session)], 
                            education_id: Annotated[UUID, EDUCATION_ID],
                            education_update: UpdateEducation) -> Education:
    """
    Actualiza una formación existente en la base de datos.
    Se debe ser administrador para poder acceder a este endpoint.

    Args:
        session (AsyncSession): Sesión de base de datos.
        education_id (UUID): ID de la formación a actualizar.
        education_update (UpdateEducation): Datos de la formación actualizada.

    Returns:
        Education: La formación actualizada.
    """
    
    # obtenemos el diccionario de la formación
    update_education_dict = education_update.model_dump()
    # obtenemos el sector_id y lo eliminamos del diccionario
    sector_id = update_education_dict.pop("sector_id", None)

    # obtenemos la formación a actualizar
    education_to_update: Education = await get_record_by_id(session, Education, education_id)

    # actualizamos los campos de la formación
    update_model(education_to_update, update_education_dict)

    # si se ha especificado un sector, lo añadimos a la tabla relacion de sector y educacion
    if sector_id:
        # si la formación ya tiene un sector, actualizamos el sector_id si no, creamos una nueva relacion
        if education_to_update.sector is not None:
            education_to_update.sector.sector_id = sector_id
        else:
            new_sector_education = SectorEducation(education_id=education_to_update.id, sector_id=sector_id)
            session.add(new_sector_education)

    await secure_commit(session)

    await session.refresh(education_to_update, ["sector", "level"])

    return education_to_update



# PATCH METHODS #

@education_route.patch("/education-levels/{education_level_id}/", response_model=ReadLevel, dependencies=[Depends(PermissionsManager.is_admin)])
async def partial_update_education_level(*,
                                        session: Annotated[AsyncSession, Depends(get_session)], 
                                        education_level_id: Annotated[UUID, EDUCATION_LEVEL_ID],
                                        education_update: PartialUpdateLevel) -> EducationLevel:
    """
    Actualiza parcialmente un nivel educativo existente en la base de datos.
    Se debe ser administrador para poder acceder a este endpoint.

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


@education_route.patch("/{education_id}/", response_model=ReadEducationComplete, response_model_exclude_none=True, dependencies=[Depends(PermissionsManager.is_admin)])
async def partial_update_education(*,
                                    session: Annotated[AsyncSession, Depends(get_session)], 
                                    education_id: Annotated[UUID, EDUCATION_ID],
                                    education_update: PartialUpdateEducation) -> Education:
    """
    Actualiza parcialmente una formación existente en la base de datos.
    Se debe ser administrador para poder acceder a este endpoint.

    Args:
        session (AsyncSession): sesión de base de datos.
        education_id (UUID): id de la formación a actualizar.
        education_update (PartialUpdateEducation): objeto que contiene los campos a actualizar.

    Returns:
        Education: objeto de la formación actualizada.
    """
    
    # obtenemos el diccionario de la formación sin los campos que no se han especificado
    update_education_dict = education_update.model_dump(exclude_unset=True)

    # obtenemos el sector_id y lo eliminamos del diccionario
    sector_id = update_education_dict.pop("sector_id", None)

    # obtenemos la formación a actualizar
    education_to_update: Education = await get_record_by_id(session, Education, education_id)

    # actualizamos los campos de la formación
    update_model(education_to_update, update_education_dict)

    # si se ha especificado un sector, lo añadimos a la tabla relacion de sector y educacion
    if sector_id:
        # si la formación ya tiene un sector, actualizamos el sector_id si no, creamos una nueva relacion
        if education_to_update.sector is not None:
            education_to_update.sector.sector_id = sector_id
        else:
            new_sector_education = SectorEducation(education_id=education_to_update.id, sector_id=sector_id)
            session.add(new_sector_education)

    await secure_commit(session)

    await session.refresh(education_to_update, ["sector", "level"])

    return education_to_update



# DELETE METHODS #



@education_route.delete("/education-levels/{education_level_id}/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(PermissionsManager.is_admin)])
async def delete_education_level(*,
                                session: Annotated[AsyncSession, Depends(get_session)],
                                education_level_id: Annotated[UUID, EDUCATION_LEVEL_ID]) -> None:
    """
    Elimina un nivel educativo de la base de datos.
    Se debe ser administrador para poder acceder a este endpoint.

    Args:
        session (AsyncSession): sesión de base de datos.
        education_level_id (UUID): id del nivel educativo a eliminar.
    """

    education_level_to_delete: EducationLevel = await get_record_by_id(session, EducationLevel, education_level_id)

    await session.delete(education_level_to_delete)

    await secure_commit(session)

@education_route.delete("/{education_id}/sector/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(PermissionsManager.is_admin)])
async def delete_education_sector(*,
                                    session: Annotated[AsyncSession, Depends(get_session)], 
                                    education_id: Annotated[UUID, EDUCATION_ID]) -> None:
    """
    Elimina el sector de una formación.
    Se debe ser administrador para poder acceder a este endpoint.

    Args:
    - session (AsyncSession): sesión de base de datos.
    - education_id (UUID): id de la formación a actualizar.
    """
    
    education_sector: SectorEducation = await get_database_records(session, SectorEducation, where=SectorEducation.education_id == education_id, result_list=False)

    await session.delete(education_sector)

    await secure_commit(session)




@education_route.delete("/{education_id}/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(PermissionsManager.is_admin)])
async def delete_education(*,
                            session: Annotated[AsyncSession, Depends(get_session)], 
                            education_id: Annotated[UUID, EDUCATION_ID]) -> None:
    """
    Elimina un registro de formación de la base de datos.
    Se debe ser administrador para poder acceder a este endpoint.

    Args:
    - session (AsyncSession): sesión de base de datos.
    - education_id (UUID): id de la formación a eliminar.
    """
    education_to_delete: Education = await get_record_by_id(session, Education, education_id, options=(noload(Education.level), noload(Education.sector)))

    await session.delete(education_to_delete)

    await secure_commit(session)

