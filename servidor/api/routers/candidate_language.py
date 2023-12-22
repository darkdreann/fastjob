from fastapi import APIRouter, Depends, status
from typing import Annotated
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from api.database.connection import get_session
from api.utils.functions.database_utils import secure_commit, get_database_records
from api.security.permissions import PermissionsManager
from api.database.database_models.models import CandidateLanguage
from api.models.read_models import ReadCandidateRelationLanguage
from api.utils.constants.endpoints_params import LIMIT, OFFSET, DEFAULT_LIMIT, DEFAULT_OFFSET, USER_ID, LANGUAGE_ID, LANGUAGE_ID_BODY, LANGUAGE_LEVEL_ID_BODY
from api.utils.functions.management_utils import endpoint_request_log

candidate_language_route = APIRouter(prefix="/candidates/languages", tags=["candidates", "languages"], dependencies=[Depends(endpoint_request_log), Depends(PermissionsManager.is_candidate_resource_owner)])

@candidate_language_route.get("/{candidate_id}/", response_model=list[ReadCandidateRelationLanguage])
async def get_candidate_languages(
                                    session: Annotated[AsyncSession, Depends(get_session)],
                                    candidate_id: Annotated[UUID, USER_ID],
                                    limit: Annotated[int, LIMIT] = DEFAULT_LIMIT,
                                    offset: Annotated[int, OFFSET] = DEFAULT_OFFSET) -> list[CandidateLanguage]:
    """
    Obtiene una lista de lenguajes de un candidato.
    Se debe ser el propietario del recurso o un administrador.

    Args:
    - session: Sesión de base de datos.
    - candidate_id: ID del usuario candidato.
    - limit: Límite de resultados a devolver (opcional, valor por defecto: DEFAULT_LIMIT).
    - offset: Desplazamiento de resultados (opcional, valor por defecto: DEFAULT_OFFSET).

    Returns:
    - list[CandidateLanguage]: Lista de lenguajes del candidato.
    """

    candidate_languages: list[CandidateLanguage] = await get_database_records(session, CandidateLanguage, limit=limit, offset=offset, where=CandidateLanguage.candidate_id == candidate_id)

    return candidate_languages

@candidate_language_route.get("/{candidate_id}/{language_id}/", response_model=ReadCandidateRelationLanguage)
async def get_candidate_language(
                                    session: Annotated[AsyncSession, Depends(get_session)],
                                    candidate_id: Annotated[UUID, USER_ID],
                                    language_id: Annotated[UUID, LANGUAGE_ID]) -> CandidateLanguage:
    """
    Obtiene un lenguaje de un candidato.
    Se debe ser el propietario del recurso o un administrador.

    Args:
    - session: Sesión de base de datos.
    - candidate_id: ID del usuario candidato.
    - language_id: ID del lenguaje.

    Returns:
    - CandidateLanguage: Lenguaje del candidato.
    """

    candidate_language: CandidateLanguage = await get_database_records(session, CandidateLanguage, where=(CandidateLanguage.candidate_id == candidate_id, CandidateLanguage.language_id == language_id), result_list=False)

    return candidate_language


@candidate_language_route.post("/{candidate_id}/", response_model=ReadCandidateRelationLanguage, status_code=status.HTTP_201_CREATED)
async def create_candidate_language(
                                    session: Annotated[AsyncSession, Depends(get_session)],
                                    candidate_id: Annotated[UUID, USER_ID],
                                    language_id: Annotated[UUID, LANGUAGE_ID_BODY],
                                    level_id: Annotated[UUID, LANGUAGE_LEVEL_ID_BODY]) -> CandidateLanguage:
    """
    Crea una experiencia de un candidato.
    Se debe ser el propietario del recurso o un administrador.
    
    Args:
    - session: Sesión de base de datos.
    - candidate_id: ID del usuario candidato.
    - language_id: ID del lenguaje.
    - level_id: ID del nivel del lenguaje.
    
    Returns:
    - CandidateLanguage: Lenguaje del candidato.
    """
    
    new_candidate_language = CandidateLanguage(candidate_id=candidate_id, language_id=language_id, language_level_id=level_id)

    session.add(new_candidate_language)

    await secure_commit(session)

    await session.refresh(new_candidate_language, ["language", "language_level"])

    return new_candidate_language


@candidate_language_route.put("/{candidate_id}/{language_id}/", response_model=ReadCandidateRelationLanguage)
async def update_candidate_language(
                                    session: Annotated[AsyncSession, Depends(get_session)],
                                    candidate_id: Annotated[UUID, USER_ID],
                                    language_id: Annotated[UUID, LANGUAGE_ID],
                                    level_id: Annotated[UUID, LANGUAGE_LEVEL_ID_BODY]) -> CandidateLanguage:
    """
    Permite actualizar el nivel de un lenguaje de un candidato.
    Se debe ser el propietario del recurso o un administrador.

    Args:
    - session: Sesión de base de datos.
    - candidate_id: ID del usuario candidato.
    - language_id: ID del lenguaje.
    - level_id: ID del nivel del lenguaje.

    Returns:
    - CandidateLanguage: Lenguaje del candidato.
    """

    candidate_language: CandidateLanguage = await get_database_records(session, CandidateLanguage, where=(CandidateLanguage.candidate_id == candidate_id, CandidateLanguage.language_id == language_id), result_list=False)

    candidate_language.language_level_id = level_id

    await secure_commit(session)

    await session.refresh(candidate_language, ["language_level"])

    return candidate_language


@candidate_language_route.delete("/{candidate_id}/{language_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_candidate_language(
                                    session: Annotated[AsyncSession, Depends(get_session)],
                                    candidate_id: Annotated[UUID, USER_ID],
                                    language_id: Annotated[UUID, LANGUAGE_ID]) -> None:
    """
    Permite borrar un lenguaje de un candidato.
    Se debe ser el propietario del recurso o un administrador.

    Args:
    - session: Sesión de base de datos.
    - candidate_id: ID del usuario candidato.
    - language_id: ID del lenguaje.
    """

    candidate_language: CandidateLanguage = await get_database_records(session, CandidateLanguage, where=(CandidateLanguage.candidate_id == candidate_id, CandidateLanguage.language_id == language_id), result_list=False)

    await session.delete(candidate_language)

    await secure_commit(session)
