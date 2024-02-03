from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Annotated
from api.database.database_models.models import Language, LanguageLevel
from api.database.connection import get_session
from api.utils.constants.endpoints_params import LIMIT, OFFSET, DEFAULT_LIMIT, DEFAULT_OFFSET, LANGUAGE_ID, LANGUAGE_LEVEL_ID, LANGUAGE_EXTRA_FIELD, LANGUAGE_LEVEL_EXTRA_FIELD, LANGUAGE_NAME_KEYWORD, LANGUAGE_LEVEL_NAME_KEYWORD, LANGUAGE_NAME_KEYWORD_QUERY
from api.security.permissions import PermissionsManager
from api.models.read_models import ReadLevel, ReadLevelLanguage, ReadLanguage, ReadLanguageComplete
from api.models.create_models import CreateLanguage, CreateLevel
from api.models.update_models import UpdateLanguage, UpdateLevel
from api.models.partial_update_models import PartialUpdateLevel
from api.utils.functions.management_utils import endpoint_request_log
from api.utils.functions.database_utils import secure_commit, get_record_by_id, get_database_records
from api.utils.functions.models_utils import update_model
from api.models.enums.endpoints import LanguageExtraField, LanguageLevelExtraField

language_route = APIRouter(prefix="/languages", tags=["languages"], dependencies=[Depends(endpoint_request_log)])

# GET METHODS #
@language_route.get("/", response_model=list[ReadLanguage], dependencies=[Depends(PermissionsManager.is_logged)])
async def get_languages(*,
                        session: AsyncSession = Depends(get_session),
                        name_keyword: Annotated[str, LANGUAGE_NAME_KEYWORD_QUERY] = None,
                        limit: Annotated[int, LIMIT] = DEFAULT_LIMIT,
                        offset: Annotated[int, OFFSET] = DEFAULT_OFFSET) -> list[Language]:
    
    """
    Obtener todos los idiomas.
    Solo para usuarios logueados.

    Args:
    - session (AsyncSession, optional): Conexion a la base de datos. Defaults to Depends(get_session).
    - name_keyword (str, optional): Palabras clave para buscar en el nombre del idioma. Defaults to None.
    - limit (int, optional): Numero de registros a mostrar. Defaults to DEFAULT_LIMIT.
    - offset (int, optional): Numero de registros a saltar. Defaults to DEFAULT_OFFSET.

    Returns:
    - list[Language]: Lista de idiomas
    """

    where = None
    if name_keyword:
        where = Language.name.startswith(name_keyword)

    languages: list[Language] = await get_database_records(session, Language, limit=limit, offset=offset, where=where)

    return languages

@language_route.get("/language-name/{name_keyword}/", response_model=list[str])
async def get_languages(*,
                        session: AsyncSession = Depends(get_session),
                        name_keyword: Annotated[str, LANGUAGE_NAME_KEYWORD],
                        limit: Annotated[int, LIMIT] = DEFAULT_LIMIT,
                        offset: Annotated[int, OFFSET] = DEFAULT_OFFSET) -> list[str]:
    
    """
    Obtener todos los nombres de los idiomas que contengan las palabras clave.

    Args:
    - session (AsyncSession, optional): Conexion a la base de datos. Defaults to Depends(get_session).
    - name_keyword (str): Palabras clave para buscar en el nombre del idioma.
    - limit (int, optional): Numero de registros a mostrar. Defaults to DEFAULT_LIMIT.
    - offset (int, optional): Numero de registros a saltar. Defaults to DEFAULT_OFFSET.

    Returns:
    - list[Language]: Lista de idiomas
    """

    languages: list[str] = await get_database_records(session, Language.name, limit=limit, offset=offset, where=Language.name.startswith(name_keyword), order_by=Language.name.desc())
    return languages

@language_route.get("/language-levels/", response_model=list[ReadLevel])
async def get_language_levels(*,
                                session: AsyncSession = Depends(get_session),
                                language_level_keyword: Annotated[str, LANGUAGE_LEVEL_NAME_KEYWORD] = None,
                                limit: Annotated[int, LIMIT] = DEFAULT_LIMIT,
                                offset: Annotated[int, OFFSET] = DEFAULT_OFFSET) -> list[LanguageLevel]:
        
    """
    Obtener todos los niveles de idiomas

    Args:
    - session (AsyncSession, optional): Conexion a la base de datos. Defaults to Depends(get_session).
    - language_level_keyword (str, optional): Palabras clave para buscar en el nombre del nivel de idioma. Defaults to None.
    - limit (int, optional): Numero de registros a mostrar. Defaults to DEFAULT_LIMIT.
    - offset (int, optional): Numero de registros a saltar. Defaults to DEFAULT_OFFSET.

    Returns:
    - list[LanguageLevel]: Lista de niveles de idiomas
    """

    where = None
    if language_level_keyword:
        where = LanguageLevel.name.startswith(language_level_keyword)

    levels: list[LanguageLevel] = await get_database_records(session, LanguageLevel, where=where, limit=limit, offset=offset, order_by=LanguageLevel.value)

    return levels


@language_route.get("/admin/", response_model=list[ReadLanguageComplete], response_model_exclude_defaults=True, dependencies=[Depends(PermissionsManager.is_admin)])
async def get_languages_complete(*,
                                session: AsyncSession = Depends(get_session),
                                limit: Annotated[int, LIMIT] = DEFAULT_LIMIT,
                                offset: Annotated[int, OFFSET] = DEFAULT_OFFSET,
                                extra_fields: Annotated[set[LanguageExtraField], LANGUAGE_EXTRA_FIELD] = ()) -> list[Language]:
    
    """
    Obtener todos los idiomas con sus relaciones. 
    Solo para administradores

    Args:
    - session (AsyncSession, optional): Conexion a la base de datos. Defaults to Depends(get_session).
    - limit (int, optional): Numero de registros a mostrar. Defaults to DEFAULT_LIMIT.
    - offset (int, optional): Numero de registros a saltar. Defaults to DEFAULT_OFFSET.

    Returns:
    - list[Language]: Lista de idiomas
    """

    languages: list[Language] = await get_database_records(session, Language, limit=limit, offset=offset, options=[LanguageExtraField.get_field_value(field) for field in extra_fields], unique=True)
    return languages

@language_route.get("/admin/language-levels/", response_model=list[ReadLevelLanguage], response_model_exclude_defaults=True, dependencies=[Depends(PermissionsManager.is_admin)])
async def get_language_levels_complete(*,
                                        session: AsyncSession = Depends(get_session),
                                        limit: Annotated[int, LIMIT] = DEFAULT_LIMIT,
                                        offset: Annotated[int, OFFSET] = DEFAULT_OFFSET,
                                        extra_fields: Annotated[set[LanguageLevelExtraField], LANGUAGE_LEVEL_EXTRA_FIELD] = ()) -> list[LanguageLevel]:
    """
    Obtener todos los niveles de idiomas con sus relaciones. 
    Solo para administradores.

    Args:
    - session (AsyncSession, optional): Conexión a la base de datos. Defaults to Depends(get_session).
    - limit (int, optional): Número de registros a mostrar. Defaults to DEFAULT_LIMIT.
    - offset (int, optional): Número de registros a saltar. Defaults to DEFAULT_OFFSET.
    - extra_fields (Annotated[LanguageLevelExtraField, LANGUAGE_LEVEL_EXTRA_FIELD]): Campos extra de las relaciones de la tabla language level que se quieren obtener. Se pueden especificar varios.

    Returns:
    - list[LanguageLevel]: Lista de niveles de idiomas.
    """

    levels: list[LanguageLevel] = await get_database_records(session, LanguageLevel, limit=limit, offset=offset, options=[LanguageLevelExtraField.get_field_value(field) for field in extra_fields], order_by=LanguageLevel.value, unique=True)

    return levels



@language_route.get("/admin/{language_id}/", response_model=ReadLanguageComplete, response_model_exclude_defaults=True, dependencies=[Depends(PermissionsManager.is_admin)])
async def get_language_complete(*,
                                session: AsyncSession = Depends(get_session),
                                language_id: Annotated[UUID, LANGUAGE_ID],
                                extra_fields: Annotated[set[LanguageExtraField], LANGUAGE_EXTRA_FIELD] = ()) -> Language:
    
    """
    Obtener un idioma por su id con sus relaciones. 
    Solo para administradores.

    Args:
    - session (AsyncSession, optional): Conexión a la base de datos. Defaults to Depends(get_session).
    - language_id (UUID): Id del idioma.
    - extra_fields (Annotated[LanguageExtraField, LANGUAGE_EXTRA_FIELD]): Campos extra de las relaciones de la tabla language que se quieren obtener. Se pueden especificar varios.

    Returns:
    - Language: Idioma.
    """

    language: Language = await get_record_by_id(session, Language, language_id, options=[LanguageExtraField.get_field_value(field) for field in extra_fields])

    return language

@language_route.get("/admin/language-levels/{language_level_id}/", response_model=ReadLevelLanguage, response_model_exclude_defaults=True, dependencies=[Depends(PermissionsManager.is_admin)])
async def get_language_level_complete(*,
                                    session: AsyncSession = Depends(get_session),
                                    language_level_id: Annotated[UUID, LANGUAGE_LEVEL_ID],
                                    extra_fields: Annotated[set[LanguageLevelExtraField], LANGUAGE_LEVEL_EXTRA_FIELD] = ()) -> LanguageLevel:
        
    """
    Obtener un nivel de idioma por su id con sus relaciones. 
    Solo para administradores.

    Args:
    - session (AsyncSession, optional): Conexión a la base de datos. Defaults to Depends(get_session).
    - language_level_id (UUID): Id del nivel de idioma.
    - extra_fields (Annotated[LanguageLevelExtraField, LANGUAGE_LEVEL_EXTRA_FIELD]): Campos extra de las relaciones de la tabla language level que se quieren obtener. Se pueden especificar varios.

    Returns:
    - LanguageLevel: Nivel de idioma.
    """
    
    level: LanguageLevel = await get_record_by_id(session, LanguageLevel, language_level_id, options=[LanguageLevelExtraField.get_field_value(field) for field in extra_fields])

    return level



@language_route.get("/language-levels/{language_level_id}/", response_model=ReadLevel, dependencies=[Depends(PermissionsManager.is_logged)])
async def get_language_level(*,
                            session: AsyncSession = Depends(get_session),
                            language_level_id: Annotated[UUID, LANGUAGE_LEVEL_ID]) -> LanguageLevel:
        
    """
    Obtener un nivel de idioma por su id.
    Solo para usuarios logueados.

    Args:
    - session (AsyncSession, optional): Conexión a la base de datos. Defaults to Depends(get_session).
    - language_level_id (UUID): Id del nivel de idioma.

    Returns:
    - LanguageLevel: Nivel de idioma.
    """

    level: LanguageLevel = await get_record_by_id(session, LanguageLevel, language_level_id)

    return level

@language_route.get("/{language_id}/", response_model=ReadLanguage, dependencies=[Depends(PermissionsManager.is_logged)])
async def get_language(*,
                        session: AsyncSession = Depends(get_session),
                        language_id: Annotated[UUID, LANGUAGE_ID]) -> Language:
    
    """
    Obtener un idioma por su id.
    Solo para usuarios logueados.

    Args:
    - session (AsyncSession, optional): Conexión a la base de datos. Defaults to Depends(get_session).
    - language_id (UUID): Id del idioma.

    Returns:
    - Language: Idioma.
    """

    language: Language = await get_record_by_id(session, Language, language_id)

    return language


# POST METHODS #

@language_route.post("/", response_model=ReadLanguage, status_code=status.HTTP_201_CREATED, dependencies=[Depends(PermissionsManager.is_admin)])
async def create_language(*,
                        session: AsyncSession = Depends(get_session),
                        new_language: CreateLanguage) -> Language:
        
    """
    Crear un idioma.
    Solo para administradores.

    Args:
    - session (AsyncSession, optional): Conexión a la base de datos. Defaults to Depends(get_session).
    - language (CreateLanguage): Modelo para crear un idioma.

    Returns:
    - Language: Idioma creado.
    """

    new_db_language = Language(**new_language.model_dump())

    session.add(new_db_language)

    await secure_commit(session)

    return new_db_language

@language_route.post("/language-levels/", response_model=ReadLevel, status_code=status.HTTP_201_CREATED, dependencies=[Depends(PermissionsManager.is_admin)])
async def create_language_level(*,
                                session: AsyncSession = Depends(get_session),
                                new_language_level: CreateLevel) -> LanguageLevel:
        
    """Crear un nivel de idioma.

    Args:
        session (AsyncSession, optional): Conexión a la base de datos. Defaults to Depends(get_session).
        language_level (CreateLevel): Modelo para crear un nivel de idioma.

    Returns:
        LanguageLevel: Nivel de idioma creado.
    """

    new_db_language_level = LanguageLevel(**new_language_level.model_dump())

    session.add(new_db_language_level)

    await secure_commit(session)

    return new_db_language_level

# PUT METHODS #

@language_route.put("/language-levels/{language_level_id}/", response_model=ReadLevel, dependencies=[Depends(PermissionsManager.is_admin)])
async def update_language_level(*,
                                session: AsyncSession = Depends(get_session),
                                language_level_id: Annotated[UUID, LANGUAGE_LEVEL_ID],
                                language_level: UpdateLevel) -> LanguageLevel:
    
    """
    Actualizar un nivel de idioma.
    Solo para administradores.

    Args:
    - session (AsyncSession, optional): Conexión a la base de datos. Defaults to Depends(get_session).
    - language_level_id (UUID): Id del nivel de idioma.
    - language_level (UpdateLevel): Modelo para actualizar un nivel de idioma.

    Returns:
    - LanguageLevel: Nivel de idioma actualizado.
    """

    db_language_level = await get_record_by_id(session, LanguageLevel, language_level_id)

    update_model(db_language_level, language_level.model_dump())

    await secure_commit(session)

    return db_language_level



@language_route.put("/{language_id}/", response_model=ReadLanguage, dependencies=[Depends(PermissionsManager.is_admin)])
async def update_language(*,
                            session: AsyncSession = Depends(get_session),
                            language_id: Annotated[UUID, LANGUAGE_ID],
                            language: UpdateLanguage) -> Language:
        
    """
    Actualizar un idioma.
    Solo para administradores.

    Args:
    - session (AsyncSession, optional): Conexión a la base de datos. Defaults to Depends(get_session).
    - language_id (UUID): Id del idioma.
    - language (UpdateLanguage): Modelo para actualizar un idioma.

    Returns:
    - Language: Idioma actualizado.
    """

    db_language = await get_record_by_id(session, Language, language_id)

    update_model(db_language, language.model_dump())

    await secure_commit(session)

    return db_language

# PATCH METHODS #


@language_route.patch("/language-levels/{language_level_id}/", response_model=ReadLevel, dependencies=[Depends(PermissionsManager.is_admin)])
async def partial_update_language_level(*,
                                session: AsyncSession = Depends(get_session),
                                language_level_id: Annotated[UUID, LANGUAGE_LEVEL_ID],
                                language_level: PartialUpdateLevel) -> LanguageLevel:
    
    """
    Actualizar un nivel de idioma parcialmente. Solo se actualizarán los campos que se pasen en el modelo.
    Solo para administradores.

    Args:
    - session (AsyncSession, optional): Conexión a la base de datos. Defaults to Depends(get_session).
    - language_level_id (UUID): Id del nivel de idioma.
    - language_level (PartialUpdateLevel): Modelo para actualizar parcialmente un nivel de idioma.

    Returns:
    - LanguageLevel: Nivel de idioma actualizado.
    """

    db_language_level = await get_record_by_id(session, LanguageLevel, language_level_id)

    update_model(db_language_level, language_level.model_dump(exclude_unset=True))

    await secure_commit(session)

    return db_language_level

# DELETE METHODS #

@language_route.delete("/language-levels/{language_level_id}/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(PermissionsManager.is_admin)])
async def delete_language_level(*,
                                session: AsyncSession = Depends(get_session),
                                language_level_id: Annotated[UUID, LANGUAGE_LEVEL_ID]) -> None:
    
    """
    Eliminar un nivel de idioma.
    Solo para administradores.

    Args:
    - session (AsyncSession, optional): Conexión a la base de datos. Defaults to Depends(get_session).
    - language_level_id (UUID): Id del nivel de idioma.
    """

    db_language_level: LanguageLevel = await get_record_by_id(session, LanguageLevel, language_level_id)

    await session.delete(db_language_level)

    await secure_commit(session)


@language_route.delete("/{language_id}/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(PermissionsManager.is_admin)])
async def partial_update_language(*,
                            session: AsyncSession = Depends(get_session),
                            language_id: Annotated[UUID, LANGUAGE_ID]) -> None:
    
    """
    Eliminar un idioma.
    Solo para administradores.

    Args:
    - session (AsyncSession, optional): Conexión a la base de datos. Defaults to Depends(get_session).
    - language_id (UUID): Id del idioma.
    """

    db_language: Language = await get_record_by_id(session, Language, language_id)

    await session.delete(db_language)

    await secure_commit(session)
