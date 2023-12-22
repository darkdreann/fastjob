from fastapi import APIRouter, status, Depends
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from api.database.database_models.models import Address
from api.database.connection import get_session
from api.utils.constants.endpoints_params import LIMIT, OFFSET, ADDRESS_ID, ADDRESS_POSTAL_CODE, ADDRESS_EXTRA_FIELD, DEFAULT_LIMIT, DEFAULT_OFFSET
from api.security.permissions import PermissionsManager
from api.models.read_models import ReadAddress, ReadAddressComplete
from api.models.create_models import CreateAddress
from api.models.update_models import UpdateAddress
from api.models.partial_update_models import PartialUpdateAddress
from api.models.enums.endpoints import AddressExtraField
from api.utils.functions.management_utils import endpoint_request_log
from api.utils.functions.database_utils import secure_commit, get_database_records, get_record_by_id
from api.utils.functions.models_utils import update_model

address_route = APIRouter(prefix="/addresses", tags=["addresses"], dependencies=[Depends(endpoint_request_log)])

@address_route.get("/", response_model=list[ReadAddress], dependencies=[Depends(PermissionsManager.is_logged)])
async def get_addresses(*,
                        session: Annotated[AsyncSession, Depends(get_session)], 
                        limit: Annotated[int, LIMIT] = DEFAULT_LIMIT,
                        offset: Annotated[int, OFFSET] = DEFAULT_OFFSET) -> list[Address]:
    """
    Obtiene todas las direcciones de la base de datos y las devuelve.
    Se debe estar logueado para poder acceder a este endpoint.
    
    Args:
    - session (AsyncSession): La sesión de la base de datos.
    - limit (int): El límite de direcciones a devolver. Por defecto es 20.
    - offset (int): El número de direcciones a omitir. Por defecto es 0.
            
    Returns:
    - list[Address]: La lista de direcciones.
    """

    addresses = await get_database_records(session, Address, limit=limit, offset=offset)

    return addresses

@address_route.get("/admin/", response_model=list[ReadAddressComplete], response_model_exclude_defaults=True, dependencies=[Depends(PermissionsManager.is_admin)])
async def get_addresses_admin(*,
                    session: Annotated[AsyncSession, Depends(get_session)], 
                    limit: Annotated[int, LIMIT] = DEFAULT_LIMIT,
                    offset: Annotated[int, OFFSET] = DEFAULT_OFFSET,
                    extra_fields: Annotated[set[AddressExtraField], ADDRESS_EXTRA_FIELD] = ()) -> Address:
    """
    Obtiene todas las direcciones de la base de datos y las devuelve. Solo para administradores. Devuelve los campos extra especificados.
    Se debe ser administrador para poder acceder a este endpoint.
    
    Args:
    - session (AsyncSession): La sesión de la base de datos.
    - limit (int): El límite de direcciones a devolver. Por defecto es 20.
    - offset (int): El número de direcciones a omitir. Por defecto es 0.
    - extra_fields (set[AddressExtraField]): Los campos extra de la dirección que se quieren obtener. Por defecto es ().
            
    Returns:
    - list[Address]: La lista de direcciones.
    """

    addresses: list[Address] = await get_database_records(session, Address, options=[AddressExtraField.get_field_value(field) for field in extra_fields], limit=limit, offset=offset, unique=True)

    return addresses

@address_route.get("/admin/{address_id}/", response_model=ReadAddressComplete, response_model_exclude_defaults=True, dependencies=[Depends(PermissionsManager.is_admin)])
async def get_address_admin(*,
                    session: Annotated[AsyncSession, Depends(get_session)], 
                    address_id: Annotated[UUID, ADDRESS_ID],
                    extra_fields: Annotated[set[AddressExtraField], ADDRESS_EXTRA_FIELD] = ()) -> Address:
    """
    Obtiene una dirección por su id y la devuelve. Si no existe devuelve un error. Solo para administradores. Devuelve los campos extra especificados.
    Se debe ser administrador para poder acceder a este endpoint.
    
    Args:
    - session (AsyncSession): La sesión de la base de datos.
    - address_id (UUID): El id de la dirección.
    - extra_fields (set[AddressExtraField]): Los campos extra de la dirección que se quieren obtener. Por defecto es ().
            
    Returns:
    - Address: La dirección.
    """

    address: Address = await get_record_by_id(session, Address, address_id, options=[AddressExtraField.get_field_value(field) for field in extra_fields])

    return address


@address_route.get("/postal-code/{address_postal_code}/", response_model=ReadAddress, dependencies=[Depends(PermissionsManager.is_logged)])
async def get_address_by_postal_code(*,
                    session: Annotated[AsyncSession, Depends(get_session)], 
                    address_postal_code: Annotated[int, ADDRESS_POSTAL_CODE]) -> Address:
    """
    Obtiene una dirección por su código postal y la devuelve.
    Se debe estar logueado para poder acceder a este endpoint.

    Args:
    - session (AsyncSession): La sesión de la base de datos.
    - postal_code (int): El código postal de la dirección.

    Returns:
    - Address: La dirección.
    """

    address: Address = await get_database_records(session, Address, where=Address.postal_code == address_postal_code, result_list=False)
    
    return address

@address_route.get("/{address_id}/", response_model=ReadAddress, dependencies=[Depends(PermissionsManager.is_logged)])
async def get_address(*,
                    session: Annotated[AsyncSession, Depends(get_session)], 
                    address_id: Annotated[UUID, ADDRESS_ID]) -> Address:
    """
    Obtiene una dirección por su id y la devuelve.
    Se debe estar logueado para poder acceder a este endpoint.
    
    Args:
    - session (AsyncSession): La sesión de la base de datos.
    - address_id (UUID): El id de la dirección.

    Returns:
    - Address: La dirección.
    """
    
    address = await get_record_by_id(session, Address, address_id)

    return address

@address_route.post("/", response_model=ReadAddress, status_code=status.HTTP_201_CREATED, dependencies=[Depends(PermissionsManager.is_admin)])
async def create_address(*,
                        session: Annotated[AsyncSession, Depends(get_session)], 
                        new_address: CreateAddress) -> Address:
    """
    Crea una nueva dirección en la base de datos.
    Se debe ser administrador para poder acceder a este endpoint.

    Args:
    - session (AsyncSession): Sesión de base de datos.
    - new_address (CreateAddress): Datos de la nueva dirección.

    Returns:
    - Address: La dirección creada.
    """
    
    address = Address(**new_address.model_dump())

    session.add(address)
    await secure_commit(session)

    return address

@address_route.put("/{address_id}/", response_model=ReadAddress, dependencies=[Depends(PermissionsManager.is_admin)])
async def update_address(*,
                        session: Annotated[AsyncSession, Depends(get_session)],
                        address_id: Annotated[UUID, ADDRESS_ID],
                        updated_address: UpdateAddress) -> Address:
    """
    Actualiza una dirección existente en la base de datos.
    Se debe ser administrador para poder acceder a este endpoint.

    Args:
    - session (AsyncSession): Sesión de base de datos.
    - address_id (UUID): ID de la dirección a actualizar.
    - updated_address (UpdateAddress): Nuevos datos de la dirección.

    Returns:
    - ReadAddress: Dirección actualizada.
    """

    address_to_update = await get_record_by_id(session, Address, address_id)

    update_model(address_to_update, updated_address.model_dump())

    await secure_commit(session)

    return address_to_update

@address_route.patch("/{address_id}/", response_model=ReadAddress, dependencies=[Depends(PermissionsManager.is_admin)])
async def partial_update_address(*,
                        session: Annotated[AsyncSession, Depends(get_session)],
                        address_id: Annotated[UUID, ADDRESS_ID],
                        updated_address: PartialUpdateAddress) -> Address:
    """
    Actualiza parcialmente una dirección existente en la base de datos.
    Se debe ser administrador para poder acceder a este endpoint.

    Args:
    - session (AsyncSession): Sesión de base de datos.
    - address_id (UUID): ID de la dirección a actualizar.
    - updated_address (PartialUpdateAddress): Datos actualizados de la dirección.

    Returns:
    - Address: La dirección actualizada.
    """
    
    address_to_update = await get_record_by_id(session, Address, address_id)
    
    update_model(address_to_update, updated_address.model_dump(exclude_unset=True))

    await secure_commit(session)

    return address_to_update

@address_route.delete("/{address_id}/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(PermissionsManager.is_admin)])
async def delete_address(*,
                        session: Annotated[AsyncSession, Depends(get_session)],
                        address_id: Annotated[UUID, ADDRESS_ID]) -> None:
    """
    Elimina una dirección de la base de datos.
    Se debe ser administrador para poder acceder a este endpoint.

    Args:
    - session (AsyncSession): Sesión de base de datos.
    - address_id (UUID): ID de la dirección a eliminar.
    """
    
    address_to_delete = await get_record_by_id(session, Address, address_id)
    
    await session.delete(address_to_delete)

    await secure_commit(session)