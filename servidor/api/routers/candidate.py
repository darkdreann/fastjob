from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, Depends, status, UploadFile
from fastapi.responses import Response
from sqlalchemy.orm import noload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from api.database.connection import get_session
from api.utils.functions.database_utils import secure_commit, get_database_records, get_record_by_id
from api.security.permissions import PermissionsManager
from api.database.database_models.models import Candidate, User, JobCandidate, Job, Address
from api.models.enums.models import UserType
from api.models.read_models import ReadCandidate, ReadCandidateComplete, ReadCandidateMinimal, ReadJobMinimal
from api.models.create_models import CreateCandidate
from api.models.update_models import UpdateCandidate
from api.models.partial_update_models import PartialUpdateCandidate
from api.utils.constants.endpoints_params import LIMIT, OFFSET, DEFAULT_LIMIT, DEFAULT_OFFSET, USER_ID, CANDIDATE_EXTRA_FIELD, CV_PARAM
from api.utils.constants.error_strings import INVALID_FILE_TYPE
from api.utils.functions.management_utils import endpoint_request_log
from api.utils.functions.models_utils import update_model, get_address_from_db
from api.utils.functions.candidate_filter import get_candidate_filter_params, CandidateExtraField
from api.utils.exceptions import RequestContentTypeError

candidate_route = APIRouter(prefix="/candidates", tags=["candidates"], dependencies=[Depends(endpoint_request_log)])

@candidate_route.get("/", response_model_exclude_defaults=True, response_model=list[ReadCandidateMinimal|ReadCandidateComplete], dependencies=[Depends(PermissionsManager.is_admin)])
async def get_candidates(
                        session: Annotated[AsyncSession, Depends(get_session)],
                        candidate_params: Annotated[dict, Depends(get_candidate_filter_params)],
                        limit: Annotated[int, LIMIT] = DEFAULT_LIMIT,
                        offset: Annotated[int, OFFSET] = DEFAULT_OFFSET) -> list[Candidate]:
    """
    Obtiene una lista de candidatos según los parámetros especificados.
    Se debe ser administrador.

    Args:
    - session (AsyncSession): Sesión de base de datos.
    - limit (int, optional): Límite de resultados a devolver. Por defecto es DEFAULT_LIMIT.
    - offset (int, optional): Desplazamiento de resultados. Por defecto es DEFAULT_OFFSET.
    - candidate_params (dict): Parámetros de búsqueda de candidatos.

    Returns:
    - list[Candidate]: Lista de candidatos encontrados.
    """
    fields = candidate_params.pop("fields")
     
    list_candidates: list[Candidate] = await get_database_records(session, *fields, **candidate_params, limit=limit, offset=offset)
    
    return list_candidates

@candidate_route.get("/applied-jobs/{candidate_id}/", response_model=list[ReadJobMinimal], dependencies=[Depends(PermissionsManager.is_candidate_resource_owner)])
async def get_candidate_applied_jobs(
                                    session: Annotated[AsyncSession, Depends(get_session)], 
                                    candidate_id: Annotated[UUID, USER_ID],
                                    limit: Annotated[int, LIMIT] = DEFAULT_LIMIT,
                                    offset: Annotated[int, OFFSET] = DEFAULT_OFFSET,) -> list[tuple]:
    """
    Obtiene los trabajos a los que un candidato ha aplicado.
    Se debe ser el propietario del recurso o un administrador.
    
    Args:
    - session: Sesión de base de datos.
    - candidate_id: ID del usuario candidato.
    - limit: Límite de resultados a devolver (opcional, valor por defecto: DEFAULT_LIMIT).
    - offset: Desplazamiento de resultados (opcional, valor por defecto: DEFAULT_OFFSET).
    
    Returns:
    - Lista de trabajos a los que el candidato ha aplicado.
    """
    
    applied_jobs: list[tuple] = await get_database_records(session, Job.id, Job.title, Job.description, Address.province, limit=limit, offset=offset, 
                                                                  joins=(
                                                                    {
                                                                        "target": JobCandidate,
                                                                        "onclause": JobCandidate.job_id == Job.id,
                                                                    },
                                                                    {
                                                                        "target": Address,
                                                                        "onclause": Address.id == Job.address_id,
                                                                    }
                                                                  ),
                                                                  where=JobCandidate.candidate_id == candidate_id, order_by=JobCandidate.inscription_date.desc(), scalar=False)
    return applied_jobs

@candidate_route.get("/{candidate_id}/", response_model=ReadCandidateComplete, response_model_exclude_defaults=True, dependencies=[Depends(PermissionsManager.is_candidate_resource_owner)])
async def get_candidate(
                        session: Annotated[AsyncSession, Depends(get_session)], 
                        candidate_id: Annotated[UUID, USER_ID],
                        extra_fields: Annotated[set[CandidateExtraField], CANDIDATE_EXTRA_FIELD] = ()) -> Candidate:
    """
    Obtiene un candidato según su id.
    Se debe ser el propietario del recurso o un administrador.
    
    Args:
    - session (AsyncSession): Sesión de base de datos.
    - candidate_id (UUID, optional): El id del usuario.
    - extra_fields (set[CandidateExtraField], optional): Campos adicionales que se quieren obtener del candidato. Por defecto es ().

    Returns:
    - Candidate: El candidato encontrado.
    """

    # anadimos los campos adicionales que se quieren obtener
    options = [CandidateExtraField.get_field_value(field) for field in extra_fields]
    # anadimos la informacion del usuario y su direccion
    options.append(joinedload(Candidate.user).joinedload(User.address))

    candidate: Candidate = await get_record_by_id(session, Candidate, candidate_id, options=options)

    return candidate


@candidate_route.post("/", status_code=status.HTTP_201_CREATED, response_model=ReadCandidate)
async def create_candidate(
                            session: Annotated[AsyncSession, Depends(get_session)],
                            new_candidate: CreateCandidate) -> Candidate:
    """
    Crea un nuevo candidato en la base de datos.
    Puede ser usado sin autenticación.

    Args:
    - session (AsyncSession): La sesión de base de datos.
    - new_candidate (CreateCandidate): Los datos del nuevo candidato.

    Returns:
    - Candidate: El candidato creado.
    """

    # obtenemos la direccion de la base de datos
    address = await get_address_from_db(session, new_candidate.user.address)

    # creamos el usuario anadiento la direccion
    user = User(**new_candidate.user.model_dump(), user_type=UserType.CANDIDATE, address=address)

    # creamos el candidato anadiendo el usuario
    candidate = Candidate(**new_candidate.model_dump(exclude="user"), user=user)

    session.add(candidate)

    await secure_commit(session)

    return candidate


@candidate_route.put("/{candidate_id}/", response_model=ReadCandidateComplete, response_model_exclude_defaults=True, dependencies=[Depends(PermissionsManager.is_candidate_resource_owner)])
async def update_candidate(
                            session: Annotated[AsyncSession, Depends(get_session)], 
                            candidate_id: Annotated[UUID, USER_ID],
                            update_candidate: UpdateCandidate) -> Candidate:
    """
    Actualiza un candidato existente en la base de datos.
    Se debe ser el propietario del recurso o un administrador.

    Args:
    - session (AsyncSession): Sesión de base de datos.
    - candidate_id (UUID): ID del usuario asociado al candidato.
    - update_candidate (UpdateCandidate): Datos actualizados del candidato.

    Returns:
    - Candidate: El candidato actualizado.
    """
    
    candidate: Candidate = await get_record_by_id(session, Candidate, candidate_id, options=joinedload(Candidate.user).joinedload(User.address))

    update_model(candidate, update_candidate.model_dump())

    # cambiamos la direccion por la nueva de la base de datos
    candidate.user.address = await get_address_from_db(session, update_candidate.user.address)

    await secure_commit(session)

    return candidate


@candidate_route.patch("/{candidate_id}/", response_model=ReadCandidateComplete, response_model_exclude_defaults=True, dependencies=[Depends(PermissionsManager.is_candidate_resource_owner)])
async def update_candidate(
                            session: Annotated[AsyncSession, Depends(get_session)], 
                            candidate_id: Annotated[UUID, USER_ID],
                            update_candidate: PartialUpdateCandidate) -> Candidate:
    """
    Actualiza un candidato existente en la base de datos.
    Se debe ser el propietario del recurso o un administrador.

    Args:
    - session (AsyncSession): Sesión de base de datos.
    - candidate_id (UUID): ID del usuario asociado al candidato.
    - update_candidate (UpdateCandidate): Datos actualizados del candidato.

    Returns:
    - Candidate: El candidato actualizado.
    """
    
    candidate: Candidate = await get_record_by_id(session, Candidate, candidate_id, options=joinedload(Candidate.user).joinedload(User.address))

    update_model(candidate, update_candidate.model_dump(exclude_unset=True))

    # si se ha especificado la direccion, la cambiamos por la nueva de la base de datos
    if update_candidate.user and update_candidate.user.address:
        candidate.user.address = await get_address_from_db(session, update_candidate.user.address)

    await secure_commit(session)

    return candidate

@candidate_route.delete("/{candidate_id}/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(PermissionsManager.is_candidate_resource_owner)])
async def delete_candidate(
                            session: Annotated[AsyncSession, Depends(get_session)], 
                            candidate_id: Annotated[UUID, USER_ID]) -> None:
    """
    Elimina un candidato de la base de datos.
    Se debe ser el propietario del recurso o un administrador.

    Args:
    - session: Sesión de base de datos.
    - candidate_id: ID del usuario candidato a eliminar.
    """
    
    candidate: Candidate = await get_record_by_id(session, Candidate, candidate_id, options=joinedload(Candidate.user))

    await session.delete(candidate.user)

    await secure_commit(session)

# CURRICULUM #

@candidate_route.get("/{candidate_id}/curriculum/", status_code=status.HTTP_200_OK, response_class=Response, dependencies=[Depends(PermissionsManager.is_candidate_resource_owner)])
async def get_candidate_curriculum(
                                    session: Annotated[AsyncSession, Depends(get_session)], 
                                    candidate_id: Annotated[UUID, USER_ID]) -> Response:
    """
    Obtiene el currículum de un candidato de la base de datos.
    Se debe ser el propietario del recurso o un administrador.

    Args:
    - session: Sesión de base de datos.
    - candidate_id: ID del usuario candidato.

    Returns:
    - Response: Currículum del candidato.
    """

    cv_candidate = await get_database_records(session, Candidate.curriculum, where=Candidate.user_id == candidate_id, result_list=False, dependencies=[Depends(PermissionsManager.is_candidate_resource_owner)])

    return Response(cv_candidate, media_type='application/pdf')

@candidate_route.post("/{candidate_id}/curriculum/", status_code=status.HTTP_204_NO_CONTENT)
async def upload_candidate_curriculum(
                                    session: Annotated[AsyncSession, Depends(get_session)], 
                                    candidate_id: Annotated[UUID, USER_ID],
                                    curriculum: Annotated[UploadFile, CV_PARAM]) -> None:
    """
    Sube el currículum de un candidato a la base de datos.
    Se debe ser el propietario del recurso o un administrador.

    Args:
    - session: Sesión de base de datos.
    - candidate_id: ID del usuario candidato.
    - curriculum: Currículum del candidato.

    Raise:
    - RequestContentTypeError: Si el tipo de archivo no es pdf.
    """

    if curriculum.content_type != "application/pdf":
        raise RequestContentTypeError(INVALID_FILE_TYPE)
    
    candidate: Candidate = await get_record_by_id(session, Candidate, candidate_id)

    candidate.curriculum = await curriculum.read()

    await secure_commit(session)

@candidate_route.delete("/{candidate_id}/curriculum/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(PermissionsManager.is_candidate_resource_owner)])
async def delete_candidate_curriculum(
                                    session: Annotated[AsyncSession, Depends(get_session)], 
                                    candidate_id: Annotated[UUID, USER_ID]) -> None:
    """
    Elimina el currículum de un candidato de la base de datos.
    Se debe ser el propietario del recurso o un administrador.

    Args:
    - session: Sesión de base de datos.
    - candidate_id: ID del usuario candidato.
    """
    
    candidate: Candidate = await get_record_by_id(session, Candidate, candidate_id)

    candidate.curriculum = None

    await secure_commit(session)