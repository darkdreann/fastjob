from fastapi import APIRouter, Depends, status
from typing import Annotated
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from api.database.connection import get_session
from api.utils.functions.database_utils import secure_commit, get_database_records
from api.security.permissions import PermissionsManager
from api.database.database_models.models import Experience
from api.models.read_models import ReadExperience
from api.models.create_models import CreateExperience
from api.models.update_models import UpdateExperience
from api.models.partial_update_models import PartialUpdateExperience
from api.utils.constants.endpoints_params import LIMIT, OFFSET, DEFAULT_LIMIT, DEFAULT_OFFSET, USER_ID, EXPERIENCE_ID
from api.utils.functions.management_utils import endpoint_request_log
from api.utils.functions.models_utils import update_model

candidate_experience_route = APIRouter(prefix="/candidates/experiences", tags=["candidates", "experiences"], dependencies=[Depends(endpoint_request_log), Depends(PermissionsManager.is_candidate_resource_owner)])

@candidate_experience_route.get("/{candidate_id}/", response_model=list[ReadExperience], response_model_exclude_none=True)
async def get_candidate_experiences(
                                    session: Annotated[AsyncSession, Depends(get_session)],
                                    candidate_id: Annotated[UUID, USER_ID],
                                    limit: Annotated[int, LIMIT] = DEFAULT_LIMIT,
                                    offset: Annotated[int, OFFSET] = DEFAULT_OFFSET) -> list[Experience]:
    """
    Obtiene una lista de experiencias de un candidato.
    Se debe ser el propietario del recurso o un administrador.
    
    Args:
    - session: Sesión de base de datos.
    - candidate_id: ID del usuario candidato.
    - limit: Límite de resultados a devolver (opcional, valor por defecto: DEFAULT_LIMIT).
    - offset: Desplazamiento de resultados (opcional, valor por defecto: DEFAULT_OFFSET).
    
    Returns:
    - list[Experience]: Lista de experiencias del candidato.
    """
    
    experiences: list[Experience] = await get_database_records(session, Experience, limit=limit, offset=offset, where=Experience.candidate_id == candidate_id, order=(Experience.start_date.asc(), Experience.end_date.asc()))

    return experiences


@candidate_experience_route.get("/{candidate_id}/{experience_id}/", response_model=ReadExperience, response_model_exclude_none=True)
async def get_candidate_experience(
                                    session: Annotated[AsyncSession, Depends(get_session)],
                                    candidate_id: Annotated[UUID, USER_ID],
                                    experience_id: Annotated[UUID, EXPERIENCE_ID]) -> Experience:
    """
    Obtiene una experiencia de un candidato.
    Se debe ser el propietario del recurso o un administrador.
    
    Args:
    - session: Sesión de base de datos.
    - candidate_id: ID del usuario candidato.
    - experience_id: ID de la experiencia.
    
    Returns:
    - Experience: Experiencia del candidato.
    """
    
    experiences: Experience = await get_database_records(session, Experience, where=(Experience.candidate_id == candidate_id, Experience.id == experience_id), result_list=False)

    return experiences


@candidate_experience_route.post("/{candidate_id}/", response_model=ReadExperience, status_code=status.HTTP_201_CREATED, response_model_exclude_none=True)
async def create_candidate_experience(
                                        session: Annotated[AsyncSession, Depends(get_session)],
                                        candidate_id: Annotated[UUID, USER_ID],
                                        new_experience: CreateExperience) -> Experience:
    """
    Crea una experiencia para un candidato.
    Se debe ser el propietario del recurso o un administrador.
    
    Args:
    - session: Sesión de base de datos.
    - candidate_id: ID del usuario candidato.
    - new_experience: Datos de la experiencia.
    
    Returns:
    - Experience: Experiencia creada.
    """
    
    db_experience = Experience(**new_experience.model_dump(), candidate_id=candidate_id)

    session.add(db_experience)
    
    await secure_commit(session)
    
    return db_experience


@candidate_experience_route.put("/{candidate_id}/{experience_id}/", response_model=ReadExperience, response_model_exclude_none=True)
async def update_candidate_experience(
                                        session: Annotated[AsyncSession, Depends(get_session)],
                                        candidate_id: Annotated[UUID, USER_ID],
                                        experience_id: Annotated[UUID, EXPERIENCE_ID],
                                        update_experience: UpdateExperience) -> Experience:
    """
    Actualiza una experiencia de un candidato.
    Se debe ser el propietario del recurso o un administrador.
    
    Args:
    - session: Sesión de base de datos.
    - candidate_id: ID del usuario candidato.
    - experience_id: ID de la experiencia.
    - update_experience: Datos de la experiencia.
    
    Returns:
    - Experience: Experiencia actualizada.
    """
    
    db_experience: Experience = await get_database_records(session, Experience, where=(Experience.candidate_id == candidate_id, Experience.id == experience_id), result_list=False)
    
    update_model(db_experience, update_experience.model_dump())

    await secure_commit(session)
    
    return db_experience


@candidate_experience_route.patch("/{candidate_id}/{experience_id}/", response_model=ReadExperience, response_model_exclude_none=True)
async def partial_update_candidate_experience(
                                        session: Annotated[AsyncSession, Depends(get_session)],
                                        candidate_id: Annotated[UUID, USER_ID],
                                        experience_id: Annotated[UUID, EXPERIENCE_ID],
                                        update_experience: PartialUpdateExperience) -> Experience:
    """
    Actualiza una experiencia de un candidato de forma parcial.
    Se debe ser el propietario del recurso o un administrador.
    
    Args:
    - session: Sesión de base de datos.
    - candidate_id: ID del usuario candidato.
    - experience_id: ID de la experiencia.
    - update_experience: Datos de la experiencia.
    
    Returns:
    - Experience: Experiencia actualizada.
    """
    
    db_experience: Experience = await get_database_records(session, Experience, where=(Experience.candidate_id == candidate_id, Experience.id == experience_id), result_list=False)
    
    update_model(db_experience, update_experience.model_dump(exclude_unset=True))

    await secure_commit(session)
    
    return db_experience


@candidate_experience_route.delete("/{candidate_id}/{experience_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_candidate_experience(
                                        session: Annotated[AsyncSession, Depends(get_session)],
                                        candidate_id: Annotated[UUID, USER_ID],
                                        experience_id: Annotated[UUID, EXPERIENCE_ID]) -> None:
    """
    Elimina una experiencia de un candidato.
    Se debe ser el propietario del recurso o un administrador.
    
    Args:
    - session: Sesión de base de datos.
    - candidate_id: ID del usuario candidato.
    - experience_id: ID de la experiencia.
    """
    
    db_experience: Experience = await get_database_records(session, Experience, where=(Experience.candidate_id == candidate_id, Experience.id == experience_id), result_list=False)
    
    await session.delete(db_experience)
    
    await secure_commit(session)