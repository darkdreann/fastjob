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
from api.models.read_models import ReadCandidateRelationJob, ReadCandidateComplete
from api.utils.constants.endpoints_params import LIMIT, OFFSET, USER_ID, DEFAULT_LIMIT, DEFAULT_OFFSET, JOB_ID, CANDIDATE_EXTRA_FIELD
from api.utils.functions.candidate_filter import get_candidate_applied, JobCandidateExtraField


job_candidate_route = APIRouter(prefix="/jobs/candidates", tags=["jobs"], dependencies=[Depends(endpoint_request_log)])

# GET #

@job_candidate_route.get("/{job_id}/", response_model_exclude_defaults=True, response_model=list[ReadCandidateComplete], dependencies=[Depends(PermissionsManager.is_job_resource_owner_noload)])
async def get_job_candidates(
                            session: Annotated[AsyncSession, Depends(get_session)],
                            candidate_params: Annotated[dict, Depends(get_candidate_applied)],
                            limit: Annotated[int, LIMIT] = DEFAULT_LIMIT,
                            offset: Annotated[int, OFFSET] = DEFAULT_OFFSET) -> list[Candidate]:
    """
    Obtiene los candidatos que aplicaron a un trabajo específico.

    Args:
    - session (AsyncSession): Sesión de base de datos.
    - candidate_params (dict): Parámetros de filtrado de candidatos.
    - limit (int): Cantidad de registros a obtener.
    - offset (int): Registro desde el cual se empieza a obtener.

    Returns:
    - list[JobCandidate]: Lista de objetos que representan la relación entre el trabajo y el candidato.
    """

    job_candidates = await get_database_records(session, Candidate, limit=limit, offset=offset, **candidate_params, unique=True)

    return job_candidates

@job_candidate_route.get("/{job_id}/{candidate_id}/", response_model_exclude_defaults=True, response_model=ReadCandidateComplete, dependencies=[Depends(PermissionsManager.is_job_resource_owner)])
async def get_job_candidate(
                            session: Annotated[AsyncSession, Depends(get_session)],
                            job: Annotated[Job, Depends(GetJob())], 
                            candidate_id: Annotated[UUID, USER_ID],
                            extra_fields: Annotated[set[JobCandidateExtraField], CANDIDATE_EXTRA_FIELD] = ()) -> Candidate:
    """
    Obtiene la relación entre un trabajo y un candidato específico.

    Args:
    - session (AsyncSession): Sesión de base de datos.
    - job (Job): Oferta de trabajo al que se desea aplicar.
    - candidate_id (UUID): ID del candidato que aplica al trabajo.

    Returns:
    - JobCandidate: Objeto que representa la relación entre el trabajo y el candidato.
    """

    options = [JobCandidateExtraField.get_field_value(field) for field in extra_fields]
    options.append(joinedload(Candidate.user).joinedload(User.address))

    where= (JobCandidate.job_id == job.id, Candidate.user_id == candidate_id)

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
    Obtiene la cantidad de veces que un candidato ha aplicado a un trabajo específico.

    Args:
    - session (AsyncSession): Sesión de base de datos.
    - job (Job): Oferta de trabajo al que se desea aplicar.
    - candidate_id (UUID): ID del candidato que aplica al trabajo.

    Returns:
    - int: Cantidad de veces que el candidato ha aplicado al trabajo.
    """

    joins = {
        "target": JobCandidate,
        "onclause": JobCandidate.candidate_id == Candidate.user_id,
    }

    where = (
        Candidate.user_id == candidate_id,
        JobCandidate.job_id == job.id
    )

    candidate_cv = await get_database_records(session, Candidate.curriculum, joins=joins, where=where, result_list=False)

    return Response(candidate_cv, media_type='application/pdf')


# POST #

@job_candidate_route.post("/{job_id}/apply/{candidate_id}", status_code=status.HTTP_201_CREATED, response_model=ReadCandidateRelationJob, dependencies=[Depends(PermissionsManager.is_candidate_resource_owner)])
async def apply_to_job(
                        session: Annotated[AsyncSession, Depends(get_session)],
                        job_id: Annotated[UUID, JOB_ID], 
                        candidate_id: Annotated[UUID, USER_ID]) -> JobCandidate:
    """
    Aplica a un trabajo específico.

    Args:
    - session (AsyncSession): Sesión de base de datos.
    - job_id (UUID): ID del trabajo al que se desea aplicar.
    - candidate_id (UUID): ID del candidato que aplica al trabajo.

    Returns:
    - JobCandidate: Objeto que representa la relación entre el trabajo y el candidato.
    """
    
    job_candidate = JobCandidate(job_id=job_id, candidate_id=candidate_id)

    session.add(job_candidate)

    await secure_commit(session)

    await session.refresh(job_candidate, ["job"])

    return job_candidate

# DELETE #

@job_candidate_route.delete("/{job_id}/remove/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(PermissionsManager.is_candidate_resource_owner)])
async def remove_job_application(
                                session: Annotated[AsyncSession, Depends(get_session)],
                                job_id: Annotated[UUID, JOB_ID], 
                                candidate_id: Annotated[UUID, USER_ID]) -> None:
    """
    Elimina la aplicación de un candidato a un trabajo específico.

    Args:
    - session (AsyncSession): Sesión de base de datos.
    - job_id (UUID): ID del trabajo al que se desea aplicar.
    - candidate_id (UUID): ID del candidato que aplica al trabajo.
    """

    options = (noload(JobCandidate.candidate), noload(JobCandidate.job))

    where = (JobCandidate.job_id == job_id, JobCandidate.candidate_id == candidate_id)

    job_candidate = await get_database_records(session, JobCandidate, options=options, where=where, result_list=False)

    await session.delete(job_candidate)

    await secure_commit(session)