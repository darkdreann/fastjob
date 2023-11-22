from fastapi import APIRouter, status, Depends
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from api.database.database_models.models import Adress
from api.database.connection import get_session
from api.utils.constants.endpoints_params import LIMIT, OFFSET, ADRESS_ID, ADRESS_POSTAL_CODE, ADRESS_EXTRA_FIELD, DEFAULT_LIMIT, DEFAULT_OFFSET
from api.security.permissions import PermissionsManager
from api.models.read_models import ReadAdress, ReadAdressComplete
from api.models.create_models import CreateAdress
from api.models.update_models import UpdateAdress
from api.models.partial_update_models import PartialUpdateAdress
from api.models.enums.endpoints import AdressExtraField
from api.utils.functions.management_utils import endpoint_request_log
from api.utils.functions.database_utils import update_model, secure_commit, get_database_records, get_record_by_id

adressRoute = APIRouter(prefix="/addresses", tags=["addresses"], dependencies=[Depends(endpoint_request_log)])

@adressRoute.get("/", response_model=list[ReadAdress], dependencies=[Depends(PermissionsManager.is_logged)])
async def get_addresses(*,
                        session: Annotated[AsyncSession, Depends(get_session)], 
                        limit: Annotated[int | None, LIMIT] = DEFAULT_LIMIT,
                        offset: Annotated[int | None, OFFSET] = DEFAULT_OFFSET) -> list[Adress]:
    """Obtiene todas las direcciones de la base de datos y las devuelve.
    
        Args:
            session (AsyncSession): La sesión de la base de datos.
            limit (int, optional): El límite de direcciones a devolver. Defaults to 20.
            offset (int, optional): El número de direcciones a omitir. Defaults to 0.
            
        Returns:
            list[Adress]: La lista de direcciones."""

    adresses = await get_database_records(session, Adress, limit=limit, offset=offset)

    return adresses

@adressRoute.get("/admin/", response_model=list[ReadAdressComplete], response_model_exclude_defaults=True, dependencies=[Depends(PermissionsManager.is_admin)])
async def get_adress(*,
                    session: Annotated[AsyncSession, Depends(get_session)], 
                    limit: Annotated[int | None, LIMIT] = DEFAULT_LIMIT,
                    offset: Annotated[int | None, OFFSET] = DEFAULT_OFFSET,
                    extra_fields: Annotated[set[AdressExtraField], ADRESS_EXTRA_FIELD] = ()) -> Adress:
    """Obtiene todas las direcciones de la base de datos y las devuelve. Solo para administradores. Devuelve los campos extra especificados.
    
        Args:
            session (AsyncSession): La sesión de la base de datos.
            limit (int, optional): El límite de direcciones a devolver. Defaults to 20.
            offset (int, optional): El número de direcciones a omitir. Defaults to 0.
            extra_fields (set[AdressExtraField], optional): Los campos extra de la dirección que se quieren obtener. Defaults to ().
            
        Returns:
            list[Adress]: La lista de direcciones.
        
        """

    adresses: list[Adress] = await get_database_records(session, Adress, options=[AdressExtraField.get_field_value(field) for field in extra_fields], limit=limit, offset=offset, unique=True)

    print(adresses[0].users_list)

    return adresses

@adressRoute.get("/admin/{adress_id}/", response_model=ReadAdressComplete, response_model_exclude_defaults=True, dependencies=[Depends(PermissionsManager.is_admin)])
async def get_adress(*,
                    session: Annotated[AsyncSession, Depends(get_session)], 
                    adress_id: Annotated[UUID, ADRESS_ID],
                    extra_fields: Annotated[set[AdressExtraField], ADRESS_EXTRA_FIELD] = ()) -> Adress:
    """Obtiene una dirección por su id y la devuelve. Si no existe devuelve un error. Solo para administradores. Devuelve los campos extra especificados.
    
        Args:
            session (AsyncSession): La sesión de la base de datos.
            adress_id (UUID): El id de la dirección.
            extra_fields (set[AdressExtraField], optional): Los campos extra de la dirección que se quieren obtener. Defaults to ().
            
        Returns:
            Adress: La dirección.
            
        Raises:
            HTTPException: Si no se encuentra la dirección."""

    adress: Adress = await get_record_by_id(session, Adress, adress_id, options=[AdressExtraField.get_field_value(field) for field in extra_fields])

    return adress



@adressRoute.get("/postal-code/{adress_postal_code}/", response_model=ReadAdress, dependencies=[Depends(PermissionsManager.is_logged)])
async def get_adress_by_postal_code(*,
                    session: Annotated[AsyncSession, Depends(get_session)], 
                    adress_postal_code: Annotated[int, ADRESS_POSTAL_CODE]) -> Adress:
    """Obtiene una dirección por su código postal y la devuelve. Si no existe devuelve un error.

        Args:
            session (AsyncSession): La sesión de la base de datos.
            postal_code (int): El código postal de la dirección.
        
        Returns:
            Adress: La dirección.

        Raises:
            HTTPException: Si no se encuentra la dirección."""

    adress: Adress = await get_database_records(session, Adress, where=Adress.postal_code == adress_postal_code, result_list=False)
    
    return adress

@adressRoute.get("/{adress_id}/", response_model=ReadAdress, dependencies=[Depends(PermissionsManager.is_logged)])
async def get_adress(*,
                    session: Annotated[AsyncSession, Depends(get_session)], 
                    adress_id: Annotated[UUID, ADRESS_ID]) -> Adress:
    """Obtiene una dirección por su id y la devuelve. Si no existe devuelve un error.
    
        Args:
            session (AsyncSession): La sesión de la base de datos.
            adress (Adress): La dirección.
            
        Returns:
            Adress: La dirección.
            
        Raises:
            HTTPException: Si no se encuentra la dirección."""
    
    adress = await get_record_by_id(session, Adress, adress_id)


    return adress

@adressRoute.post("/", response_model=ReadAdress, status_code=status.HTTP_201_CREATED, dependencies=[Depends(PermissionsManager.is_admin)])
async def create_adress(*,
                        session: Annotated[AsyncSession, Depends(get_session)], 
                        new_adress: CreateAdress) -> Adress:
    """
    Crea una nueva dirección en la base de datos.

    Args:
        session (AsyncSession): Sesión de base de datos.
        new_adress (CreateAdress): Datos de la nueva dirección.

    Returns:
        Adress: La dirección creada.
    """
    
    adress = Adress(**new_adress.model_dump())

    session.add(adress)
    await secure_commit(session)

    return adress

@adressRoute.put("/{adress_id}/", response_model=ReadAdress, dependencies=[Depends(PermissionsManager.is_admin)])
async def update_adress(*,
                        session: Annotated[AsyncSession, Depends(get_session)],
                        adress_id: Annotated[UUID, ADRESS_ID],
                        updated_adress: UpdateAdress) -> Adress:
    """
    Actualiza una dirección existente en la base de datos.

    Args:
        session (AsyncSession): Sesión de base de datos.
        adress_to_update (Adress): Dirección a actualizar.
        updated_adress (UpdateAdress): Nuevos datos de la dirección.

    Returns:
        ReadAdress: Dirección actualizada.
    """

    adress_to_update = await get_record_by_id(session, Adress, adress_id)

    update_model(adress_to_update, updated_adress.model_dump())

    await secure_commit(session)


    return adress_to_update

@adressRoute.patch("/{adress_id}/", response_model=ReadAdress, dependencies=[Depends(PermissionsManager.is_admin)])
async def partial_update_adress(*,
                        session: Annotated[AsyncSession, Depends(get_session)],
                        adress_id: Annotated[UUID, ADRESS_ID],
                        updated_adress: PartialUpdateAdress) -> Adress:
    """
    Actualiza parcialmente una dirección existente en la base de datos.

    Args:
        session (AsyncSession): Sesión de base de datos.
        adress_id (UUID): ID de la dirección a actualizar.
        updated_adress (PartialUpdateAdress): Datos actualizados de la dirección.

    Returns:
        Adress: La dirección actualizada.
    """
    
    adress_to_update = await get_record_by_id(session, Adress, adress_id)
    
    update_model(adress_to_update, updated_adress.model_dump(exclude_unset=True))

    await secure_commit(session)

    return adress_to_update

@adressRoute.delete("/{adress_id}/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(PermissionsManager.is_admin)])
async def delete_adress(*,
                        session: Annotated[AsyncSession, Depends(get_session)],
                        adress_id: Annotated[UUID, ADRESS_ID]) -> None:
    """
    Elimina una dirección de la base de datos.

    Args:
        session (AsyncSession): Sesión de base de datos.
        adress_id (UUID): ID de la dirección a eliminar.

    Returns:
        None
    """
    
    adress_to_delete = await get_record_by_id(session, Adress, adress_id)
    
    await session.delete(adress_to_delete)

    await secure_commit(session)