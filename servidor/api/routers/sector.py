from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from uuid import UUID
from api.database.database_models.models import Sector
from api.database.connection import get_session
from api.utils.constants.endpoints_params import LIMIT, OFFSET, SECTOR_EXTRA_FIELD, SECTOR_ID, DEFAULT_LIMIT, DEFAULT_OFFSET, SECTOR_CATEGORY, SECTOR_SUBCATEGORY_KEYWORD, SECTOR_CATEGORY_KEYWORD
from api.security.permissions import PermissionsManager
from api.models.read_models import ReadSector, ReadSectorComplete, ReadSectorNoCategory
from api.models.create_models import CreateSector
from api.models.update_models import UpdateSector
from api.models.partial_update_models import PartialUpdateSector
from api.utils.functions.management_utils import endpoint_request_log
from api.utils.functions.database_utils import secure_commit, get_database_records, get_record_by_id
from api.utils.functions.models_utils import update_model
from api.models.enums.endpoints import SectorExtraField


sector_route = APIRouter(prefix="/sectors", tags=["sectors"], dependencies=[Depends(endpoint_request_log)])

@sector_route.get("/", response_model=list[ReadSector], response_model_exclude_unset=True, dependencies=[Depends(PermissionsManager.is_logged)])
async def get_sectors(
        session: Annotated[AsyncSession, Depends(get_session)],
        limit: Annotated[int, LIMIT] = DEFAULT_LIMIT,
        offset: Annotated[int, OFFSET] = DEFAULT_OFFSET) -> list[Sector]:
    """
    Devuelve todos los sectores.
    Se debe estar logueado para acceder a este endpoint.

    Args:
    - session (AsyncSession): La sesión de base de datos. Defaults to Depends(get_session).
    - limit (int, optional): Límite de registros devueltos. Defaults to 20.
    - offset (int, optional): Permite omitir un número específico de registros en el conjunto de resultados. Defaults to 0.

    Returns:
    - list[Sector]: La lista de sectores o subcategorías.
    """

    sectors = await get_database_records(session, Sector, limit=limit, offset=offset)
    return sectors

@sector_route.get("/categories/{category_keyword}/", response_model=list[str])
async def get_sector_categories(        
        session: Annotated[AsyncSession, Depends(get_session)],
        category_keyword: Annotated[str, SECTOR_CATEGORY_KEYWORD],
        limit: Annotated[int, LIMIT] = DEFAULT_LIMIT,
        offset: Annotated[int, OFFSET] = DEFAULT_OFFSET) -> list[str]:
    """
    Recibe una palabra y devuelve las categorías de sectores que empiezan por esa palabra.

    Args:
    - session (AsyncSession): La sesión de base de datos. Defaults to Depends(get_session).
    - category_keyword (str): La palabra clave para buscar en la categoría del sector.
    - limit (int, optional): Límite de registros devueltos. Defaults to 20.
    - offset (int, optional): Permite omitir un número específico de registros en el conjunto de resultados. Defaults to 0.

    Returns:
    - list[str]: La lista de categorías de sectores.
    """

    categories = await get_database_records(session, Sector.category.distinct(), where=Sector.category.startswith(category_keyword), limit=limit, offset=offset, order_by=Sector.category.desc())
    return categories

@sector_route.get("/{category}/subcategories/{subcategory_keyword}/", response_model=list[ReadSectorNoCategory])
async def get_sector_subcategories(        
        session: Annotated[AsyncSession, Depends(get_session)],
        category: Annotated[str, SECTOR_CATEGORY],
        subcategory_keyword: Annotated[str, SECTOR_SUBCATEGORY_KEYWORD],
        limit: Annotated[int, LIMIT] = DEFAULT_LIMIT,
        offset: Annotated[int, OFFSET] = DEFAULT_OFFSET) -> list[ReadSectorNoCategory]:
    """
    Recibe una palabra y devuelve las categorías de sectores que empiezan por esa palabra.

    Args:
    - session (AsyncSession): La sesión de base de datos. Defaults to Depends(get_session).
    - category (str): La categoría del sector.
    - subcategory_keyword (str): La palabra clave para buscar en la subcategoría del sector.
    - limit (int, optional): Límite de registros devueltos. Defaults to 20.
    - offset (int, optional): Permite omitir un número específico de registros en el conjunto de resultados. Defaults to 0.

    Returns:
    - list[str]: La lista de categorías de sectores.
    """

    subcategories = await get_database_records(session, Sector, where=(Sector.subcategory.startswith(subcategory_keyword), 
                                                                    Sector.category == category), limit=limit, offset=offset, order_by=Sector.subcategory.desc())
    return subcategories

@sector_route.get("/admin/", response_model=list[ReadSectorComplete], response_model_exclude_defaults=True, dependencies=[Depends(PermissionsManager.is_admin)])
async def get_sectors_complete(
        session: Annotated[AsyncSession, Depends(get_session)],
        limit: Annotated[int, LIMIT] = DEFAULT_LIMIT,
        offset: Annotated[int, OFFSET] = DEFAULT_OFFSET,
        extra_fields: Annotated[set[SectorExtraField], SECTOR_EXTRA_FIELD] = ()) -> list[Sector]:
    """
    Devuelve todos los sectores con todos sus campos. Solo accesible por administradores. Se pueden especificar los campos extra que se quieren obtener de las tablas relacionadas.
    Se debe ser administrador para acceder a este endpoint.

    Args:
    - session (AsyncSession): La sesión de base de datos. Defaults to Depends(get_session).
    - limit (int, optional): Límite de registros devueltos. Defaults to 20.
    - offset (int, optional): Permite omitir un número específico de registros en el conjunto de resultados. Defaults to 0.
    - extra_fields (set[SectorExtraField], optional): Los campos extra que se quieren obtener de las tablas relacionadas. Defaults to ().

    Returns:
    - list[Sector]: La lista de sectores con todos sus campos.
    """
    sectors = await get_database_records(session, Sector, options=[SectorExtraField.get_field_value(field) for field in extra_fields], limit=limit, offset=offset, unique=True)

    return sectors


@sector_route.get("/admin/{sector_id}/", response_model=ReadSectorComplete, response_model_exclude_defaults=True, dependencies=[Depends(PermissionsManager.is_admin)])
async def get_sector_complete(
        session: Annotated[AsyncSession, Depends(get_session)],
        sector_id: Annotated[UUID, SECTOR_ID],
        extra_fields: Annotated[set[SectorExtraField], SECTOR_EXTRA_FIELD] = ()) -> Sector:
    """
    Devuelve un sector en específico pasándole el id del sector. Solo accesible por administradores. Se pueden especificar los campos extra que se quieren obtener de las tablas relacionadas.
    Se debe ser administrador para acceder a este endpoint.

    Args:
    - session (AsyncSession): La sesión de base de datos. Defaults to Depends(get_session).
    - sector_id (int): El id del sector.
    - extra_fields (set[SectorExtraField], optional): Los campos extra que se quieren obtener de las tablas relacionadas. Defaults to ().

    Returns:
    - Sector: El sector completo.
    """
    sector = await get_record_by_id(session, Sector, sector_id, options=[SectorExtraField.get_field_value(field) for field in extra_fields])

    return sector


@sector_route.get("/{sector_id}/", response_model=ReadSector, dependencies=[Depends(PermissionsManager.is_logged)])
async def get_sector(*,
                     session: Annotated[AsyncSession, Depends(get_session)],
                     sector_id: Annotated[UUID, SECTOR_ID]) -> Sector:
    """
    Devuelve un sector en específico pasándole el id del sector.
    Se debe estar logueado para acceder a este endpoint.

    Args:
    - session (AsyncSession): La sesión de base de datos. Defaults to Depends(get_session).
    - sector_id (int): El id del sector.

    Returns:
    - Sector: El sector.
    """
    sector: Sector = await get_record_by_id(session, Sector, sector_id)

    return sector


@sector_route.post("/", status_code=status.HTTP_201_CREATED, response_model=ReadSector, dependencies=[Depends(PermissionsManager.is_admin)])
async def create_sector(
        session: Annotated[AsyncSession, Depends(get_session)],
        new_sector: CreateSector) -> Sector:
    """
    Crea un nuevo sector.
    Se debe ser administrador para acceder a este endpoint.

    Args:
    - session (AsyncSession): La sesión de base de datos. Defaults to Depends(get_session).
    - new_sector (CreateSector): El sector a crear.

    Returns:
    - Sector: El sector creado.
    """
    db_new_sector = Sector(**new_sector.model_dump())

    session.add(db_new_sector)

    await secure_commit(session)

    return db_new_sector


@sector_route.put("/{sector_id}/", response_model=ReadSector, dependencies=[Depends(PermissionsManager.is_admin)])
async def update_sector(
        session: Annotated[AsyncSession, Depends(get_session)],
        sector_id: Annotated[UUID, SECTOR_ID],
        updated_sector: UpdateSector) -> Sector:
    """
    Actualiza un sector en específico pasándole el id del sector. Se debe ser administrador para acceder a este endpoint.

    Args:
    - session (AsyncSession): La sesión de base de datos. Defaults to Depends(get_session).
    - sector_id (int): El id del sector.
    - updated_sector (UpdateSector): El sector con los datos actualizados.

    Returns:
    - Sector: El sector actualizado.
    """
    sector_to_update = await get_record_by_id(session, Sector, sector_id)

    update_model(sector_to_update, updated_sector.model_dump())

    await secure_commit(session)

    return sector_to_update


@sector_route.patch("/{sector_id}/", response_model=ReadSector, dependencies=[Depends(PermissionsManager.is_admin)])
async def partial_update_sector(
        session: Annotated[AsyncSession, Depends(get_session)],
        sector_id: Annotated[UUID, SECTOR_ID],
        updated_sector: PartialUpdateSector) -> Sector:
    """
    Actualiza parcialmente un sector en específico pasándole el id del sector. Permite actualizar solo algunos campos del sector.
    Se debe ser administrador para acceder a este endpoint.

    Args:
    - session (AsyncSession): La sesión de base de datos. Defaults to Depends(get_session).
    - sector_id (int): El id del sector.
    - updated_sector (PartialUpdateSector): El sector con los datos actualizados.

    Returns:
    - Sector: El sector actualizado.
    """
    sector_to_update = await get_record_by_id(session, Sector, sector_id)

    update_model(sector_to_update, updated_sector.model_dump(exclude_unset=True))

    await secure_commit(session)

    return sector_to_update


@sector_route.delete("/{sector_id}/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(PermissionsManager.is_admin)])
async def delete_sector(
        session: Annotated[AsyncSession, Depends(get_session)],
        sector_id: Annotated[UUID, SECTOR_ID]) -> None:
    """
    Elimina un sector en específico pasándole el id del sector.
    Se debe ser administrador para acceder a este endpoint.

    Args:
    - session (AsyncSession): La sesión de base de datos. Defaults to Depends(get_session).
    - sector_id (int): El id del sector.
    """
    sector_to_delete = await get_record_by_id(session, Sector, sector_id)

    await session.delete(sector_to_delete)
    await secure_commit(session)