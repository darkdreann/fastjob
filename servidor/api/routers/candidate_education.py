from fastapi import APIRouter, Depends, status, Body
from typing import Annotated
from uuid import UUID
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from api.database.connection import get_session
from api.utils.functions.database_utils import secure_commit, get_database_records
from api.security.permissions import PermissionsManager
from api.database.database_models.models import CandidateEducation
from api.models.read_models import ReadCandidateRelationEducation
from api.utils.constants.endpoints_params import LIMIT, OFFSET, DEFAULT_LIMIT, DEFAULT_OFFSET, USER_ID, EDUCATION_ID
from api.utils.functions.management_utils import endpoint_request_log

candidate_education_route = APIRouter(prefix="/candidates/educations", tags=["candidates", "educations"], dependencies=[Depends(endpoint_request_log), Depends(PermissionsManager.is_candidate_resource_owner)])

@candidate_education_route.get("/{candidate_id}/", response_model=list[ReadCandidateRelationEducation])
async def get_candidate_educations(
                                    session: Annotated[AsyncSession, Depends(get_session)],
                                    candidate_id: Annotated[UUID, USER_ID],
                                    limit: Annotated[int, LIMIT] = DEFAULT_LIMIT,
                                    offset: Annotated[int, OFFSET] = DEFAULT_OFFSET) -> list[CandidateEducation]:
    """
    Obtiene una lista de educaciones de un candidato.

    Args:
    - session: Sesión de base de datos.
    - candidate_id: ID del usuario candidato.
    - limit: Límite de resultados a devolver (opcional, valor por defecto: DEFAULT_LIMIT).
    - offset: Desplazamiento de resultados (opcional, valor por defecto: DEFAULT_OFFSET).

    Returns:
    - list[CandidateEducation]: Lista de educaciones del candidato.
    """

    candidate_educations: list[CandidateEducation] = await get_database_records(session, CandidateEducation, limit=limit, offset=offset, where=CandidateEducation.candidate_id == candidate_id)

    return candidate_educations

@candidate_education_route.get("/{candidate_id}/{education_id}/", response_model=ReadCandidateRelationEducation)
async def get_candidate_education(
                                    session: Annotated[AsyncSession, Depends(get_session)],
                                    candidate_id: Annotated[UUID, USER_ID],
                                    education_id: Annotated[UUID, EDUCATION_ID]) -> CandidateEducation:
    """
    Obtiene una educación de un candidato.

    Args:
    - session: Sesión de base de datos.
    - candidate_id: ID del usuario candidato.
    - education_id: ID de la educación.

    Returns:
    - CandidateEducation: educación del candidato.
    """

    candidate_education: CandidateEducation = await get_database_records(session, CandidateEducation, where=(CandidateEducation.candidate_id == candidate_id, CandidateEducation.education_id == education_id), result_list=False)

    return candidate_education

@candidate_education_route.post("/{candidate_id}/", response_model=ReadCandidateRelationEducation, status_code=status.HTTP_201_CREATED)
async def create_candidate_education(
                                        session: Annotated[AsyncSession, Depends(get_session)],
                                        candidate_id: Annotated[UUID, USER_ID],
                                        education_id: Annotated[UUID, Body()],
                                        completion_date: Annotated[date, Body()]) -> CandidateEducation:
    """
    Crea una educación para un candidato.

    Args:
    - session: Sesión de base de datos.
    - candidate_id: ID del usuario candidato.
    - candidate_education: Datos de la educación del candidato.

    Returns:
    - CandidateEducation: Educación del candidato creada.
    """

    candidate_education = CandidateEducation(candidate_id=candidate_id, education_id=education_id, completion_date=completion_date)

    session.add(candidate_education)

    await secure_commit(session)

    await session.refresh(candidate_education, ["education"])

    return candidate_education


@candidate_education_route.put("/{candidate_id}/{education_id}/", response_model=ReadCandidateRelationEducation)
async def update_candidate_education(
                                    session: Annotated[AsyncSession, Depends(get_session)],
                                    candidate_id: Annotated[UUID, USER_ID],
                                    education_id: Annotated[UUID, EDUCATION_ID],
                                    completion_date: Annotated[date, Body()]) -> CandidateEducation:
    """
    Actualiza la fecha de finalización de una educación de un candidato.

    Args:
    - session: Sesión de base de datos.
    - candidate_id: ID del usuario candidato.
    - education_id: ID de la educación.
    - completion_date: Fecha de finalización de la educación.

    Returns:
    - CandidateEducation: Educación del candidato actualizada.
    """

    candidate_education: CandidateEducation = await get_database_records(session, CandidateEducation, where=(CandidateEducation.candidate_id == candidate_id, CandidateEducation.education_id == education_id), result_list=False)

    candidate_education.completion_date = completion_date

    await secure_commit(session)

    await session.refresh(candidate_education, ["education"])

    return candidate_education


@candidate_education_route.delete("/{candidate_id}/{education_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_candidate_education(
                                    session: Annotated[AsyncSession, Depends(get_session)],
                                    candidate_id: Annotated[UUID, USER_ID],
                                    education_id: Annotated[UUID, EDUCATION_ID]) -> None:
    """
    Elimina una educación de un candidato.

    Args:
    - session: Sesión de base de datos.
    - candidate_id: ID del usuario candidato.
    - education_id: ID de la educación.

    Returns:
    - None
    """

    candidate_education: CandidateEducation = await get_database_records(session, CandidateEducation, where=(CandidateEducation.candidate_id == candidate_id, CandidateEducation.education_id == education_id), result_list=False)

    await session.delete(candidate_education)

    await secure_commit(session)

    return None