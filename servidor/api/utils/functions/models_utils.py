from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from api.models.create_models import CreateAddress
from api.utils.functions.database_utils import get_database_records
from api.utils.exceptions import ResourceNotFoundException
from api.database.database_models.models import Base, Address, User
from api.models.enums.models import UserType

def update_model(model_to_update: Base, new_data: dict | BaseModel) -> None:
    """Actualiza los atributos de un modelo con los datos de un diccionario.
    
        Args:
            model_to_update (BaseModel): Modelo a actualizar.
            new_data (dict): Diccionario con los datos a actualizar."""

    for atribute, value in new_data.items():
        if isinstance(value, dict):
            update_model(getattr(model_to_update, atribute), value)
        else:
            setattr(model_to_update, atribute, value)


async def get_address_from_db(session: AsyncSession, address: CreateAddress) -> Address:
    """Obtiene una direccion de la base de datos a partir de una dirección. Si no existe devuelve la dirección pasada por parametro.
    
        Args:
            session (AsyncSession): Sesión abierta con la base de datos.
            address (CreateAddress): Dirección a buscar en la base de datos.
            
        Returns:
            Address: Dirección encontrada en la base de datos o la dirección pasada por parametro."""
    
    try:
        address_from_db = await get_database_records(session, Address, where=Address.postal_code == address.postal_code, result_list=False)
    except ResourceNotFoundException:
        return Address(**address.model_dump())

    return address_from_db