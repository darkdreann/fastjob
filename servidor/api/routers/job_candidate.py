from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from api.utils.functions.models_utils import GetJob
from sqlalchemy.orm import joinedload, noload
from api.database.connection import get_session
from api.utils.functions.management_utils import endpoint_request_log
from api.utils.functions.database_utils import secure_commit, get_database_records
from api.security.permissions import PermissionsManager
from api.database.database_models.models import Job, JobCandidate, Candidate, User
from api.models.read_models import ReadCandidateRelationJob, ReadCandidateComplete, ReadCandidateMinimal
from api.utils.exceptions import DatabaseException
from api.utils.constants.endpoints_params import LIMIT, OFFSET, USER_ID, DEFAULT_LIMIT, DEFAULT_OFFSET, JOB_ID, CANDIDATE_EXTRA_FIELD
from api.utils.functions.candidate_filter import get_candidate_applied, JobCandidateExtraField


job_candidate_route = APIRouter(prefix="/jobs/candidates", tags=["jobs"], dependencies=[Depends(endpoint_request_log)])

# GET #

@job_candidate_route.get("/{job_id}/", response_model_exclude_defaults=True, response_model=list[ReadCandidateMinimal|ReadCandidateComplete], dependencies=[Depends(PermissionsManager.is_job_resource_owner_noload)])
async def get_job_candidates(
                            session: Annotated[AsyncSession, Depends(get_session)],
                            candidate_params: Annotated[dict, Depends(get_candidate_applied)],
                            limit: Annotated[int, LIMIT] = DEFAULT_LIMIT,
                            offset: Annotated[int, OFFSET] = DEFAULT_OFFSET) -> list[Candidate]:
    """
    Obtiene los candidatos que aplicaron a una oferta específica.
    Se debe ser el propietario del recurso o un administrador.

    Args:
    - session (AsyncSession): Sesión de base de datos.
    - candidate_params (dict): Parámetros de filtrado de candidatos.
    - limit (int): Cantidad de registros a obtener.
    - offset (int): Registro desde el cual se empieza a obtener.

    Returns:
    - list[JobCandidate]: Lista de objetos que representan la relación entre la oferta y el candidato.
    """
    fields = candidate_params.pop("fields")

    job_candidates = await get_database_records(session, *fields, **candidate_params, limit=limit, offset=offset)

    return job_candidates

@job_candidate_route.get("/{job_id}/{candidate_id}/", response_model_exclude_defaults=True, response_model=ReadCandidateComplete, dependencies=[Depends(PermissionsManager.is_job_resource_owner)])
async def get_job_candidate(
                            session: Annotated[AsyncSession, Depends(get_session)],
                            job: Annotated[Job, Depends(GetJob())], 
                            candidate_id: Annotated[UUID, USER_ID],
                            extra_fields: Annotated[set[JobCandidateExtraField], CANDIDATE_EXTRA_FIELD] = ()) -> Candidate:
    """
    Obtiene la relación entre una oferta y un candidato específico.
    Se debe ser el propietario del recurso o un administrador.

    Args:
    - session (AsyncSession): Sesión de base de datos.
    - job (Job): Oferta de la oferta a la que se desea aplicar.
    - candidate_id (UUID): ID del candidato que aplica a la oferta.
    - extra_fields (set[JobCandidateExtraField]): Campos extra que se desean obtener del candidato.

    Returns:
    - JobCandidate: Objeto que representa la relación entre la oferta y el candidato.
    """

    # obtener los campos extra que se desean obtener del candidato
    options = [JobCandidateExtraField.get_field_value(field) for field in extra_fields]

    # añadir para que se obtenga el usuario y su dirección
    options.append(joinedload(Candidate.user).joinedload(User.address))

    # añadimos un filtro para que solo se obtengan los registros que coincidan con la oferta y el candidato
    where = (JobCandidate.job_id == job.id, Candidate.user_id == candidate_id)

    # hacemos join a la tabla de JobCandidate para poder filtrar por la oferta y el candidato
    joins = {
        "target": JobCandidate,
        "onclause": JobCandidate.candidate_id == Candidate.user_id,
    }

    job_candidate = await get_database_records(session, Candidate, joins=joins, options=options, where=where, result_list=False, unique=True)

    return job_candidate

@job_candidate_route.get("/{job_id}/{candidate_id}/curriculum/", response_class=Response, dependencies=[Depends(PermissionsManager.is_job_resource_owner_noload)])
async def get_job_candidate_cv(
                            session: Annotated[AsyncSession, Depends(get_session)],
                            job: Annotated[Job, Depends(GetJob(False))], 
                            candidate_id: Annotated[UUID, USER_ID]) -> Response:
    """
    Obtiene el currículum de un candidato que ha aplicado a una oferta específica.
    Se debe ser el propietario del recurso o un administrador.

    Args:
    - session (AsyncSession): Sesión de base de datos.
    - job (Job): Oferta de la oferta a la que se desea aplicar.
    - candidate_id (UUID): ID del candidato que aplica a la oferta.

    Returns:
    - int: Cantidad de veces que el candidato ha aplicado a la oferta.
    """

    # hacemos join a la tabla de JobCandidate para poder filtrar por la oferta y el candidato
    joins = {
        "target": JobCandidate,
        "onclause": JobCandidate.candidate_id == Candidate.user_id,
    }

    # añadimos un filtro para que solo se obtengan los registros que coincidan con la oferta y el candidato
    where = (
        Candidate.user_id == candidate_id,
        JobCandidate.job_id == job.id
    )

    candidate_cv = await get_database_records(session, Candidate.curriculum, joins=joins, where=where, result_list=False)

    return Response(candidate_cv, media_type='application/pdf')



@job_candidate_route.get("/{job_id}/is-applied/{candidate_id}/", dependencies=[Depends(PermissionsManager.is_candidate_resource_owner)])
async def is_candidate_applied(
                            session: Annotated[AsyncSession, Depends(get_session)],
                            job_id: Annotated[UUID, JOB_ID], 
                            candidate_id: Annotated[UUID, USER_ID]) -> bool:
    """
    Verifica si un candidato ha aplicado a un trabajo específico.

    Args:
    - session: Sesión de base de datos.
    - job_id: ID del trabajo.
    - candidate_id: ID del candidato.

    Returns:
    - bool: True si el candidato ha aplicado a la oferta, False en caso contrario.
    """

    where = (JobCandidate.job_id == job_id, JobCandidate.candidate_id == candidate_id)
    try:
        job_candidate = await get_database_records(session, JobCandidate.candidate_id, where=where, result_list=False)
    except DatabaseException:
        job_candidate = None

    return job_candidate is not None

  
# POST #

@job_candidate_route.post("/{job_id}/apply/{candidate_id}/", status_code=status.HTTP_201_CREATED, response_model=ReadCandidateRelationJob, dependencies=[Depends(PermissionsManager.is_candidate_resource_owner)])
async def apply_to_job(
                        session: Annotated[AsyncSession, Depends(get_session)],
                        job_id: Annotated[UUID, JOB_ID], 
                        candidate_id: Annotated[UUID, USER_ID]) -> JobCandidate:
    """
    Aplica un candidato a una oferta de empleo.
    Se debe ser el propietario del recurso o un administrador.

    Args:
    - session (AsyncSession): Sesión de base de datos.
    - job_id (UUID): ID de la oferta a la que se desea aplicar.
    - candidate_id (UUID): ID del candidato que aplica a la oferta.

    Returns:
    - JobCandidate: Objeto que representa la relación entre la oferta y el candidato.
    """
    
    job_candidate = JobCandidate(job_id=job_id, candidate_id=candidate_id)

    session.add(job_candidate)

    await secure_commit(session)

    await session.refresh(job_candidate, ["job"])

    return job_candidate

# DELETE #

@job_candidate_route.delete("/{job_id}/remove/{candidate_id}/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(PermissionsManager.is_candidate_resource_owner)])
async def remove_job_application(
                                session: Annotated[AsyncSession, Depends(get_session)],
                                job_id: Annotated[UUID, JOB_ID], 
                                candidate_id: Annotated[UUID, USER_ID]) -> None:
    """
    Elimina la aplicación de un candidato a una oferta específica.

    Args:
    - session (AsyncSession): Sesión de base de datos.
    - job_id (UUID): ID de la oferta a la que se desea aplicar.
    - candidate_id (UUID): ID del candidato que aplica a la oferta.
    """

    options = (noload(JobCandidate.candidate), noload(JobCandidate.job))

    where = (JobCandidate.job_id == job_id, JobCandidate.candidate_id == candidate_id)

    job_candidate = await get_database_records(session, JobCandidate, options=options, where=where, result_list=False)

    await session.delete(job_candidate)

    await secure_commit(session)