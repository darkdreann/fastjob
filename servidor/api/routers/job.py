from fastapi import APIRouter, Depends, status
from typing import Annotated
from uuid import UUID, uuid4
from sqlalchemy.orm import noload
from sqlalchemy.ext.asyncio import AsyncSession
from api.database.connection import get_session
from api.utils.functions.database_utils import secure_commit, get_database_records
from api.utils.functions.models_utils import update_model, get_address_from_db
from api.security.permissions import PermissionsManager
from api.database.database_models.models import Job, JobEducation, JobLanguage, Address, Education
from api.models.read_models import ReadJobComplete, ReadJobRelationLanguage, ReadJobCompleteWithUsers, ReadJobMinimal, ReadEducation
from api.models.create_models import CreateJob, CreateJobLanguage
from api.models.update_models import UpdateJob
from api.models.partial_update_models import PartialUpdateJob
from api.utils.constants.endpoints_params import LIMIT, OFFSET, DEFAULT_LIMIT, DEFAULT_OFFSET, JOB_EXTRA_FIELD, LANGUAGE_ID, LANGUAGE_LEVEL_ID_BODY, JOB_KEYWORD, JOB_ID
from api.utils.functions.management_utils import endpoint_request_log
from api.utils.functions.models_utils import GetJob
from api.models.enums.endpoints import JobExtraField
from api.utils.functions.job_filter import get_job_filter_params
from api.database.database_models.view_models import JobKeywordModel

job_route = APIRouter(prefix="/jobs", tags=["jobs"], dependencies=[Depends(endpoint_request_log)])

# GET #

@job_route.get("/", response_model=list[ReadJobComplete|ReadJobMinimal], response_model_exclude_none=True)
async def get_jobs(
                session: Annotated[AsyncSession, Depends(get_session)],
                job_params: Annotated[dict, Depends(get_job_filter_params)],
                limit: Annotated[int, LIMIT] = DEFAULT_LIMIT, 
                offset: Annotated[int, OFFSET] = DEFAULT_OFFSET) -> list[Job]:
    """
    Obtiene todas las ofertas de trabajo.
    Se puede usar sin autenticación.

    Args:
    - session: Sesión de base de datos.
    - job_params: Parámetros de filtrado de las ofertas de trabajo.
    - limit: Cantidad de registros a obtener.
    - offset: Cantidad de registros a saltar.

    Return:
    - Lista de ofertas de trabajo.
    """
    fields = job_params.pop("fields")

    jobs: list[Job] = await get_database_records(session, *fields, **job_params, limit=limit, offset=offset, order_by=Job.publication_date.desc())

    return jobs

@job_route.get("/admin/", response_model=list[ReadJobCompleteWithUsers], response_model_exclude_defaults=True, dependencies=[Depends(PermissionsManager.is_admin)])
async def get_jobs_admin(
                session: Annotated[AsyncSession, Depends(get_session)], 
                limit: Annotated[int, LIMIT] = DEFAULT_LIMIT, 
                offset: Annotated[int, OFFSET] = DEFAULT_OFFSET,
                extra_fields: Annotated[set[JobExtraField], JOB_EXTRA_FIELD] = ()) -> list[Job]:
    """
    Obtiene todas las ofertas de trabajo para administradores.
    Se debe ser administrador.

    Args:
    - session: Sesión de base de datos.
    - limit: Cantidad de registros a obtener.
    - offset: Cantidad de registros a saltar.
    - extra_fields: Campos adicionales de la oferta de trabajo.

    Return:
    - Lista de ofertas de trabajo.
    """

    jobs: list[Job] = await get_database_records(session, Job, options=[JobExtraField.get_field_value(field) for field in extra_fields], unique=True, limit=limit, offset=offset, order_by=Job.publication_date.desc())

    return jobs

@job_route.get("/{job_id}/", response_model=ReadJobComplete, response_model_exclude_defaults=True)
async def get_job_by_id(
                    job: Annotated[Job, Depends(GetJob())]) -> Job:
    """
    Obtiene una oferta de trabajo por su ID.
    Se puede usar sin autenticación.

    Args:
    - job: Oferta de trabajo a obtener.

    Return:
    - La oferta de trabajo.
    """

    return job

@job_route.get("/{job_id}/education/", response_model=ReadEducation, response_model_exclude_defaults=True)
async def get_job_education_by_id(
                    session: Annotated[AsyncSession, Depends(get_session)], 
                    job_id: Annotated[UUID, JOB_ID]) -> Education:
    """
    Obtiene la formación requerida para una oferta de trabajo por su ID.
    Se puede usar sin autenticación.

    Args:
    - session: Sesión de base de datos.
    - job_id: ID de la oferta de trabajo.

    Return:
    - La formación requerida.
    """

    education: Education = await get_database_records(session, Education, 
                                                                  joins=(
                                                                    {
                                                                        "target": JobEducation,
                                                                        "onclause": JobEducation.education_id == Education.id,
                                                                    },
                                                                    {
                                                                        "target": Job,
                                                                        "onclause": Job.id == JobEducation.job_id,
                                                                    }
                                                                  ),
                                                                  where=Job.id == job_id, result_list=False)
    return education

@job_route.get("/{job_id}/languages/", response_model=list[ReadJobRelationLanguage], response_model_exclude_defaults=True)
async def get_job_languages_by_id(
                    session: Annotated[AsyncSession, Depends(get_session)], 
                    job_id: Annotated[UUID, JOB_ID],
                    limit: Annotated[int, LIMIT] = DEFAULT_LIMIT, 
                    offset: Annotated[int, OFFSET] = DEFAULT_OFFSET) -> list[JobLanguage]:
    """
    Obtiene los idiomas requeridos para una oferta de trabajo por su ID.
    Se puede usar sin autenticación.

    Args:
    - session: Sesión de base de datos.
    - job_id: ID de la oferta de trabajo.
    - limit: Cantidad de registros a obtener.
    - offset: Cantidad de registros a saltar.

    Return:
    - Los idiomas requeridos.
    """

    job_languages: list[JobLanguage] = await get_database_records(session, JobLanguage, limit=limit, offset=offset, where=JobLanguage.job_id == job_id, unique=True)
    return job_languages

@job_route.get("/{job_id}/languages/{language_id}/", response_model=ReadJobRelationLanguage, response_model_exclude_defaults=True)
async def get_job_languages_by_id(
                    session: Annotated[AsyncSession, Depends(get_session)], 
                    job_id: Annotated[UUID, JOB_ID],
                    language_id: Annotated[UUID, LANGUAGE_ID]) -> JobLanguage:
    """
    Obtiene un idioma requerido para una oferta de trabajo por su ID.
    Se puede usar sin autenticación.

    Args:
    - session: Sesión de base de datos.
    - job_id: ID de la oferta de trabajo.
    - language_id: ID del idioma requerido.

    Return:
    - El idioma requerido.
    """

    job_language: JobLanguage = await get_database_records(session, JobLanguage, where=(JobLanguage.job_id == job_id, JobLanguage.language_id == language_id), result_list=False, unique=True)
    return job_language

@job_route.get("/keywords/{keyword}/", response_model=list[str])
async def get_jobs_keywords(
                            session: Annotated[AsyncSession, Depends(get_session)],
                            keyword: Annotated[str, JOB_KEYWORD],
                            limit: Annotated[int, LIMIT] = DEFAULT_LIMIT,
                            offset: Annotated[int, OFFSET] = DEFAULT_OFFSET) -> list[str]:
    """
    Obtiene una lista de palabras clave relacionadas con ofertas de trabajo que comienzan con la palabra clave dada.
    
    Args:
    - session: Sesión de base de datos.
    - keyword: Palabra clave para buscar trabajos relacionados.
    - limit: Límite de resultados a devolver (opcional, valor predeterminado: DEFAULT_LIMIT).
    - offset: Desplazamiento de resultados (opcional, valor predeterminado: DEFAULT_OFFSET).
    
    Return:
    - Lista de palabras clave relacionadas con trabajos.
    """
    
    view_table = JobKeywordModel.get_view()

    keywords = await get_database_records(session, view_table.c.word, where=view_table.c.word.startswith(keyword), order_by=view_table.c.count.desc(), limit=limit, offset=offset)

    return keywords

# POST #

@job_route.post("/", response_model=ReadJobComplete, response_model_exclude_defaults=True, status_code=status.HTTP_201_CREATED, dependencies=[Depends(PermissionsManager.is_new_job_resource_owner)])
async def create_job(
                    session: Annotated[AsyncSession, Depends(get_session)],
                    job: CreateJob,
                    job_languages: list[CreateJobLanguage] = None) -> Job:
    """
    Crea una oferta de trabajo.
    Se debe ser el propietario del recurso o un administrador.

    Args:
    - session: Sesión de base de datos.
    - job: Datos de la oferta de trabajo a crear.
    - job_languages: Idiomas requeridos para la oferta de trabajo.

    Return:
    - La oferta de trabajo creada.
    """

    # obtenemos la dirección de la base de datos
    address: Address = await get_address_from_db(session, job.address)
    # creamos la oferta de trabajo
    job_db = Job(**job.model_dump(exclude={"address", "required_education", "required_language_list"}), id=uuid4(), address=address)

    # si se especificó una formación requerida, la anadimos
    if job.required_education:
        job_education = JobEducation(job_id=job_db.id, education_id=job.required_education)
        session.add(job_education)

    # si se especificaron idiomas requeridos, los anadimos
    if job_languages:
        for language in job_languages:
            job_language = JobLanguage(job_id=job_db.id, language_id=language.language_id, level_id=language.level_id)
            session.add(job_language)

    session.add(job_db)

    await secure_commit(session)

    await session.refresh(job_db, ["address", "required_education", "language_list", "sector"])

    return job_db

@job_route.post("/{job_id}/", response_model=ReadJobRelationLanguage, status_code=status.HTTP_201_CREATED, dependencies=[Depends(PermissionsManager.is_job_resource_owner)])
async def create_job_language(
                    session: Annotated[AsyncSession, Depends(get_session)],
                    job: Annotated[Job, Depends(GetJob())],
                    job_language: CreateJobLanguage) -> JobLanguage:
    """
    Crea un idioma requerido para una oferta de trabajo.
    Se debe ser el propietario del recurso o un administrador.

    Args:
    - session: Sesión de base de datos.
    - job: Oferta de trabajo a la que se le añadirá el idioma requerido.
    - job_language: Datos del idioma requerido.

    Return:
    - El idioma requerido creado.
    """

    job_language_db = JobLanguage(job_id=job.id, **job_language.model_dump())

    session.add(job_language_db)

    await secure_commit(session)

    await session.refresh(job_language_db, ["language", "language_level"])

    return job_language_db

# PUT #

@job_route.put("/{job_id}/", response_model=ReadJobComplete, response_model_exclude_defaults=True, dependencies=[Depends(PermissionsManager.is_job_resource_owner)])
async def update_job(
                    session: Annotated[AsyncSession, Depends(get_session)],
                    job: Annotated[Job, Depends(GetJob())],
                    update_job: UpdateJob) -> Job:
    """
    Actualiza una oferta de trabajo.

    Args:
    - session: Sesión de base de datos.
    - job: Oferta de trabajo a actualizar.
    - update_job: Datos de la oferta de trabajo actualizada.

    Return:
    - La oferta de trabajo actualizada.
    """

    # actualizamos la oferta de trabajo con los datos recibidos excepto la direccion y la formacion requerida
    update_model(job, update_job.model_dump(exclude={"address", "required_education"}))

    # si se especifico una direccion, la actualizamos buscandola en la base de datos
    if update_job.address:
        address: Address = await get_address_from_db(session, update_job.address)
        job.address = address

    # si se especifico una formacion requerida, la actualizamos
    if update_job.required_education:
        # si la oferta ya tenia una formacion requerida, actualizamos su ID, si no, la creamos
        if job.required_education is not None:
            job.required_education.education_id = update_job.required_education
        else:
            job_education = JobEducation(job_id=job.id, education_id=update_job.required_education)
            session.add(job_education)

    await secure_commit(session)

    await session.refresh(job, ["address", "required_education", "language_list", "sector"])

    return job

@job_route.put("/{job_id}/languages/{language_id}/", response_model=ReadJobRelationLanguage, response_model_exclude_none=True, dependencies=[Depends(PermissionsManager.is_job_resource_owner)])
async def update_job_language(
                            session: Annotated[AsyncSession, Depends(get_session)],
                            job: Annotated[Job, Depends(GetJob())],
                            language_id: Annotated[UUID, LANGUAGE_ID],
                            language_level_id: Annotated[UUID, LANGUAGE_LEVEL_ID_BODY]) -> JobLanguage:
    """
    Actualiza un idioma requerido para una oferta de trabajo.
    Se debe ser el propietario del recurso o un administrador.

    Args:
    - session: Sesión de base de datos.
    - job: Oferta de trabajo a la que se le actualizará el idioma requerido.
    - language_id: ID del idioma requerido.
    - language_level: Nivel del idioma requerido.

    Return:
    - El idioma requerido actualizado.
    """

    job_language_db: JobLanguage = await get_database_records(session, JobLanguage, where=(JobLanguage.job_id == job.id, JobLanguage.language_id == language_id), result_list=False, unique=True)

    job_language_db.level_id = language_level_id

    await secure_commit(session)

    await session.refresh(job_language_db, ["language", "language_level"])

    return job_language_db

# PATCH #

@job_route.patch("/{job_id}/", response_model=ReadJobComplete, response_model_exclude_none=True, dependencies=[Depends(PermissionsManager.is_job_resource_owner)])
async def partial_update_job(
                        session: Annotated[AsyncSession, Depends(get_session)],
                        job: Annotated[Job, Depends(GetJob())],
                        update_job: PartialUpdateJob) -> Job:
    """
    Actualiza parcialmente una oferta de trabajo.
    Se debe ser el propietario del recurso o un administrador.

    Args:
    - session: Sesión de base de datos.
    - job: Oferta de trabajo a actualizar.
    - update_job: Datos de la oferta de trabajo actualizada.

    Return:
    - La oferta de trabajo actualizada.
    """

    # actualizamos la oferta de trabajo con los datos recibidos excepto la direccion, la formacion requerida y los campos no especificados
    update_model(job, update_job.model_dump(exclude={"address", "required_education"}, exclude_unset=True))

    # si se especifico una direccion, la actualizamos buscandola en la base de datos
    if update_job.address:
        address: Address = await get_address_from_db(session, update_job.address)
        job.address = address

    # si se especifico una formacion requerida, la actualizamos
    if update_job.required_education:
        # si la oferta ya tenia una formacion requerida, actualizamos su ID, si no, la creamos
        if job.required_education is not None:
            job.required_education.education_id = update_job.required_education
        else:
            job_education = JobEducation(job_id=job.id, education_id=update_job.required_education)
            session.add(job_education)

    await secure_commit(session)

    await session.refresh(job, ["address", "required_education", "language_list", "sector"])

    return job

# DELETE #

@job_route.delete("/{job_id}/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(PermissionsManager.is_job_resource_owner_noload)])
async def delete_job(
                    session: Annotated[AsyncSession, Depends(get_session)],
                    job: Annotated[Job, Depends(GetJob(False))]) -> None:
    """
    Elimina una oferta de trabajo.
    Se debe ser el propietario del recurso o un administrador.

    Args:
    - session: Sesión de base de datos.
    - job: Oferta de trabajo a eliminar.
    """

    await session.delete(job)

    await secure_commit(session)

@job_route.delete("/{job_id}/languages/{language_id}/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(PermissionsManager.is_job_resource_owner_noload)])
async def delete_job_language(
                            session: Annotated[AsyncSession, Depends(get_session)],
                            job: Annotated[Job, Depends(GetJob(False))],
                            language_id: Annotated[UUID, LANGUAGE_ID]) -> None:
    """
    Elimina un idioma requerido para una oferta de trabajo.
    Se debe ser el propietario del recurso o un administrador.

    Args:
    - session: Sesión de base de datos.
    - job: Oferta de trabajo a la que pertenece el idioma requerido.
    - language_id: ID del idioma requerido.
    """

    # anadimos las opciones para que no se carguen las relaciones
    options = (noload(JobLanguage.language), noload(JobLanguage.language_level), noload(JobLanguage.job))

    # filtramos por el id de la oferta de trabajo y el id del idioma
    where = (JobLanguage.job_id == job.id, JobLanguage.language_id == language_id)

    job_language_db: JobLanguage = await get_database_records(session, JobLanguage, options=options, where=where, result_list=False)

    await session.delete(job_language_db)

    await secure_commit(session)

@job_route.delete("/{job_id}/education/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(PermissionsManager.is_job_resource_owner_noload)])
async def delete_job_education(
                            session: Annotated[AsyncSession, Depends(get_session)],
                            job: Annotated[Job, Depends(GetJob(False))]) -> None:
    """
    Elimina una formación requerida para una oferta de trabajo.
    Se debe ser el propietario del recurso o un administrador.

    Args:
    - session: Sesión de base de datos.
    - job: Oferta de trabajo a la que pertenece la formación requerida.
    """

    # anadimos las opciones para que no se carguen las relaciones
    options = (noload(JobEducation.education), noload(JobEducation.job))

    # filtramos por el id de la oferta de trabajo
    where = JobEducation.job_id == job.id

    job_education_db: JobEducation = await get_database_records(session, JobEducation, options=options, where=where, result_list=False)

    await session.delete(job_education_db)

    await secure_commit(session)