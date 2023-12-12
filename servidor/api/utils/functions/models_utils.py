from pydantic import BaseModel
from uuid import UUID
from typing import Annotated, Self
from fastapi import Depends
from sqlalchemy.orm import noload
from sqlalchemy.ext.asyncio import AsyncSession
from api.models.create_models import CreateAddress
from api.utils.functions.database_utils import get_database_records
from api.utils.exceptions import ResourceNotFoundException
from api.database.database_models.models import Base, Address, Job
from api.database.connection import get_session
from api.utils.functions.database_utils import get_record_by_id
from api.utils.constants.endpoints_params import JOB_ID


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


class GetJob:
    def __init__(self, joined_required = True) -> Self:
        """
        Inicializa una instancia de la clase.

        Args:
        - joined_required (bool): Indica si se requiere la unión de datos o no. Por defecto es True.
        Return:
        - Una instancia de la clase.
        """
        self.options = None
        if not joined_required:
            self.options = (noload(Job.address), noload(Job.language_list), noload(Job.sector), noload(Job.required_education))

    async def __call__(self, session: Annotated[AsyncSession, Depends(get_session)], job_id: Annotated[UUID, JOB_ID]) -> Job:
        """
        Ejecuta la función __call__ para obtener un trabajo por su ID.

        Args:
        - session: Sesión de base de datos.
        - job_id: ID del trabajo a obtener.

        Return:
        - El trabajo correspondiente al ID proporcionado.
        """
        job: Job = await get_record_by_id(session, Job, job_id, options=self.options)
        return job