from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import RequestValidationError
from typing import Annotated
from uuid import UUID
from api.database.database_models.models import Sector
from api.database.connection import get_session
from api.utils.constants.endpoints_params import LIMIT, OFFSET, SECTOR_CATEGORY, ONLY_CATEGORY, SECTOR_EXTRA_FIELD, SECTOR_ID, DEFAULT_LIMIT, DEFAULT_OFFSET
from api.security.permissions import PermissionsManager
from api.models.read_models import ReadSector, ReadSectorComplete
from api.models.create_models import CreateSector
from api.models.update_models import UpdateSector
from api.models.partial_update_models import PartialUpdateSector
from api.utils.constants.error_strings import SECTOR_GET_PARAMS
from api.utils.functions.management_utils import endpoint_request_log
from api.utils.functions.database_utils import secure_commit, get_database_records, get_record_by_id
from api.utils.functions.models_utils import update_model
from api.models.enums.endpoints import SectorExtraField


sector_route = APIRouter(prefix="/sectors", tags=["sectors"], dependencies=[Depends(endpoint_request_log)])


async def _get_sector_params(only_categories: Annotated[bool | None, ONLY_CATEGORY] = False,
                             category_name: Annotated[str | None, SECTOR_CATEGORY] = None) -> dict:
    """Función que valida los parámetros de la ruta /sectors. Si se especifica el parámetro 'only_category' se devolverán solo las categorías de los sectores.	
        Si se especifica el parámetro 'category' se devolverán las subcategorías de ese sector. No se pueden usar ambos parámetros a la vez.

        Args:
            request (Request): La request.
            only_categories (bool, optional): Si se quiere obtener solo la categoría del sector. Defaults to False.
            category_name (str, optional): La categoría del sector. Para obtener todas sus subcategorías. Defaults to None.
        
        Raises:
            RequestValidationError: Si se especifican ambos parámetros a la vez.

        Returns:
            dict: Los parámetros de la ruta."""
            
    if category_name and only_categories:
        raise RequestValidationError([SECTOR_GET_PARAMS])
    
    if category_name:
        return {"category_name": category_name}
    return {"only_categories": only_categories}


@sector_route.get("/", response_model=list[ReadSector], response_model_exclude_unset=True, dependencies=[Depends(PermissionsManager.is_logged)])
async def get_sectors(*, 
                    session: Annotated[AsyncSession, Depends(get_session)], 
                    limit: Annotated[int, LIMIT] = DEFAULT_LIMIT,
                    offset: Annotated[int, OFFSET] = DEFAULT_OFFSET,
                    extra_params: dict = Depends(_get_sector_params)) -> list[Sector]:
    """Devuelve todos los sectores o las subcategorías de un sector en específico. Si se especifica el parámetro 'only_category' se devolverán solo las categorías de los sectores.
        Si se especifica el parámetro 'category' se devolverán las subcategorías de ese sector. No se pueden usar ambos parámetros a la vez.
        
        Args:
            session (AsyncSession): La sesión de base de datos. Defaults to Depends(get_session).
            limit (int, optional): Limite de registros devueltos. Defaults to 20.
            offset (int, optional): Permite omitir un número específico de registros en el conjunto de resultados. Defaults to 0.
            only_categories (bool, optional): Si se quiere obtener solo la categoría del sector. Defaults to False.
            category_name (str, optional): La categoría del sector. Para obtener todas sus subcategorías. Defaults to None."""

    args = [session]
    kwargs = {
        "limit": limit,
        "offset": offset,
        "scalar": False,
    }
    
    if extra_params.get("category_name"):
        args.extend((Sector.id, Sector.subcategory))
        kwargs["where"] = Sector.category == extra_params["category_name"]
        
    elif extra_params.get("only_categories"):
        args.append(Sector.category.distinct().label("category"))

    else:
        args.append(Sector)
        kwargs["scalar"] = True

    sectors = await get_database_records(*args, **kwargs)



    return sectors


@sector_route.get("/admin/", response_model=list[ReadSectorComplete], response_model_exclude_defaults=True, dependencies=[Depends(PermissionsManager.is_admin)])
async def get_sectors_complete(*,
                                session: Annotated[AsyncSession, Depends(get_session)], 
                                limit: Annotated[int, LIMIT] = DEFAULT_LIMIT,
                                offset: Annotated[int, OFFSET] = DEFAULT_OFFSET,
                                extra_fields: Annotated[set[SectorExtraField], SECTOR_EXTRA_FIELD] = ()) -> list[Sector]:
    """Devuelve todos los sectores con todos sus campos. Solo accesible por administradores. Se pueden especificar los campos extra que se quieren obtener de las tablas relacionadas.

        Args:
            session (AsyncSession): La sesión de base de datos. Defaults to Depends(get_session).
            limit (int, optional): Limite de registros devueltos. Defaults to 20.
            offset (int, optional): Permite omitir un número específico de registros en el conjunto de resultados. Defaults to 0.
            extra_fields (set[SectorExtraField], optional): Los campos extra que se quieren obtener de las tablas relacionadas. Defaults to ().

        Returns:
            list[Sector]: La lista de sectores con todos sus campos.
        """

    sectors = await get_database_records(session, Sector, options=[SectorExtraField.get_field_value(field) for field in extra_fields], limit=limit, offset=offset, unique=True)

    return sectors


@sector_route.get("/admin/{sector_id}/", response_model=ReadSectorComplete, response_model_exclude_defaults=True, dependencies=[Depends(PermissionsManager.is_admin)])
async def get_sector_complete(*,
                    session: Annotated[AsyncSession, Depends(get_session)], 
                    sector_id: Annotated[UUID, SECTOR_ID], 
                    extra_fields: Annotated[set[SectorExtraField], SECTOR_EXTRA_FIELD] = ()) -> Sector:
    
    """Devuelve un sector en específico pasandole el id del sector. Solo accesible por administradores. Se pueden especificar los campos extra que se quieren obtener de las tablas relacionadas.

        Args:
            session (AsyncSession): La sesión de base de datos. Defaults to Depends(get_session).
            sector_id (int): El id del sector.
            extra_fields (set[SectorExtraField], optional): Los campos extra que se quieren obtener de las tablas relacionadas. Defaults to ()."""
    
    sector = await get_record_by_id(session, Sector, sector_id, options=[SectorExtraField.get_field_value(field) for field in extra_fields])

    return sector


@sector_route.get("/{sector_id}/", response_model=ReadSector, dependencies=[Depends(PermissionsManager.is_logged)])
async def get_sector(*,
                    session: Annotated[AsyncSession, Depends(get_session)], 
                    sector_id: Annotated[UUID, SECTOR_ID]) -> Sector:
    
    """Devuelve un sector en específico pasandole el id del sector.

        Args:
            session (AsyncSession): La sesión de base de datos. Defaults to Depends(get_session).
            sector_id (int): El id del sector."""
    
    sector: Sector = await get_record_by_id(session, Sector, sector_id)

    return sector



@sector_route.post("/", status_code=status.HTTP_201_CREATED, response_model=ReadSector, dependencies=[Depends(PermissionsManager.is_admin)])
async def create_sector(*,
                        session: Annotated[AsyncSession, Depends(get_session)], 
                        new_sector: CreateSector) -> Sector:
    
    """Crea un nuevo sector.

        Args:
            session (AsyncSession): La sesión de base de datos. Defaults to Depends(get_session).
            sector (CreateSector): El sector a crear."""
    
    db_new_sector = Sector(**new_sector.model_dump())
    
    session.add(db_new_sector)

    await secure_commit(session)

    return db_new_sector


@sector_route.put("/{sector_id}/", response_model=ReadSector, dependencies=[Depends(PermissionsManager.is_admin)])
async def update_sector(*,
                    session: Annotated[AsyncSession, Depends(get_session)], 
                    sector_id: Annotated[UUID, SECTOR_ID],
                    updated_sector: UpdateSector) -> Sector:
    """Actualiza un sector en específico pasandole el id del sector. Si el sector no existe lanza una excepción.
        
        Args:
            session (AsyncSession): La sesión de base de datos. Defaults to Depends(get_session).
            sector_to_update (Sector): El sector a actualizar.
            updated_sector (UpdateSector): El sector con los datos actualizados.
            
        Raises:
            HTTPException: Si el sector no existe."""
    
    sector_to_update = await get_record_by_id(session, Sector, sector_id)

    update_model(sector_to_update, updated_sector.model_dump())

    await secure_commit(session)

    return sector_to_update

@sector_route.patch("/{sector_id}/", response_model=ReadSector, dependencies=[Depends(PermissionsManager.is_admin)])
async def partial_update_sector(*,
                        session: Annotated[AsyncSession, Depends(get_session)], 
                        sector_id: Annotated[UUID, SECTOR_ID],
                        updated_sector: PartialUpdateSector) -> Sector:
    """Actualiza un parcialmente sector en específico pasandole el id del sector. Si el sector no existe lanza una excepción.
        Permite actualizar solo algunos campos del sector.

        Args:
            session (AsyncSession): La sesión de base de datos. Defaults to Depends(get_session).
            sector_to_update (Sector): El sector a actualizar.
            updated_sector (PartialUpdateSector): El sector con los datos actualizados.
        Raises:
            HTTPException: Si el sector no existe."""
    
    sector_to_update = await get_record_by_id(session, Sector, sector_id)
    
    update_model(sector_to_update, updated_sector.model_dump(exclude_unset=True))

    await secure_commit(session)

    return sector_to_update


@sector_route.delete("/{sector_id}/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(PermissionsManager.is_admin)])
async def delete_sector(*,
                        session: Annotated[AsyncSession, Depends(get_session)], 
                        sector_id: Annotated[UUID, SECTOR_ID]) -> None:
    
    """Elimina un sector en específico pasandole el id del sector. Si el sector no existe lanza una excepción.	

        Args:
            session (AsyncSession): La sesión de base de datos. Defaults to Depends(get_session).
            sector_to_delete (Sector): El sector a eliminar.
        Raises:
            HTTPException: Si el sector no existe."""
    
    sector_to_delete = await get_record_by_id(session, Sector, sector_id)
    
    await session.delete(sector_to_delete)
    await secure_commit(session)