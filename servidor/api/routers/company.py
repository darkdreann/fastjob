from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from api.database.connection import get_session
from api.utils.functions.database_utils import secure_commit, get_database_records, get_record_by_id
from api.security.permissions import PermissionsManager
from api.database.database_models.models import Company, User
from api.models.enums.models import UserType
from api.models.read_models import ReadCompany, ReadCompanyComplete
from api.models.create_models import CreateCompany
from api.models.update_models import UpdateCompany
from api.models.partial_update_models import PartialUpdateCompany
from api.utils.constants.endpoints_params import DEFAULT_LIMIT, DEFAULT_OFFSET, USER_ID, COMPANIES_GET_JOBS
from api.utils.functions.management_utils import endpoint_request_log
from api.utils.functions.models_utils import update_model, get_address_from_db

company_route = APIRouter(prefix="/companies", tags=["companies"], dependencies=[Depends(endpoint_request_log)])

@company_route.get("/", response_model=list[ReadCompanyComplete], response_model_exclude_defaults=True, dependencies=[Depends(PermissionsManager.is_admin)])
async def get_companies(
                        session: Annotated[AsyncSession, Depends(get_session)], 
                        limit: Annotated[int, DEFAULT_LIMIT] = DEFAULT_LIMIT,
                        offset: Annotated[int, DEFAULT_OFFSET] = DEFAULT_OFFSET,
                        get_jobs: Annotated[bool, COMPANIES_GET_JOBS] = False) -> list[Company]:
    """
    Obtiene una lista de empresas.
    Se debe ser administrador para poder acceder a este endpoint.

    Args:
    - session: Sesión de base de datos (AsyncSession).
    - limit: Límite de resultados a devolver (int, opcional).
    - offset: Desplazamiento de resultados (int, opcional).
    - get_jobs: Indica si se deben incluir los trabajos asociados a las empresas (bool, opcional).

    Returns:
    - Lista de empresas (list[Company]).
    """

    # anadimos la informacion de usuario y direccion
    options = [joinedload(Company.user).joinedload(User.address)]
    
    # si se quiere obtener la lista de ofertas de trabajo asociadas a las empresas anadimos la relacion
    if get_jobs:
        options.append(joinedload(Company.job_list))
    
    companies: list[Company] = await get_database_records(session, Company, limit=limit, offset=offset, unique=True, options=options)

    return companies

@company_route.get("/{company_id}/", response_model=ReadCompanyComplete, response_model_exclude_defaults=True, dependencies=[Depends(PermissionsManager.is_company_resource_owner)])
async def get_company(
                        session: Annotated[AsyncSession, Depends(get_session)], 
                        company_id: Annotated[UUID, USER_ID],
                        get_jobs: Annotated[bool, COMPANIES_GET_JOBS]=False) -> Company:
    """
    Obtiene una empresa.
    Se debe ser el propietario del recurso o un administrador.

    Args:
    - session: Sesión de base de datos (AsyncSession).
    - company_id: Id de la empresa (UUID).
    - get_jobs: Indica si se deben incluir los trabajos asociados a las empresas (bool, opcional).

    Return:
    - Datos de la empresa (Company).
    """

    # anadimos la informacion de usuario y direccion
    options = [joinedload(Company.user).joinedload(User.address)]
    
    # si se quiere obtener la lista de ofertas de trabajo asociadas a las empresas anadimos la relacion
    if get_jobs:
        options.append(joinedload(Company.job_list))
    
    companies: Company = await get_record_by_id(session, Company, company_id, options=options)

    return companies

@company_route.post("/", response_model=ReadCompany, status_code=status.HTTP_201_CREATED)
async def create_company(
                        session: Annotated[AsyncSession, Depends(get_session)], 
                        new_company: CreateCompany) -> Company:
    """
    Crea una empresa.
    Se puede acceder a este endpoint sin autenticación.

    Args:
    - session: Sesión de base de datos (AsyncSession).
    - new_company: Datos de la empresa a crear (CreateCompany).

    Returns:
    - Datos de la empresa creada (Company).
    """

    # obtenemos la direccion de la base de datos
    address = await get_address_from_db(session, new_company.user.address)

    # creamos el usuario anadiendo la direccion
    user = User(**new_company.user.model_dump(), user_type=UserType.COMPANY, address=address)

    # creamos la empresa anadiendo el usuario
    company_db = Company(**new_company.model_dump(exclude="user"), user=user)

    session.add(company_db)

    await secure_commit(session)

    return company_db

@company_route.put("/{company_id}/", response_model=ReadCompany, dependencies=[Depends(PermissionsManager.is_company_resource_owner)])
async def update_company(
                        session: Annotated[AsyncSession, Depends(get_session)],
                        company_id: Annotated[UUID, USER_ID],
                        update_company: UpdateCompany) -> Company:
    
    """
    Actualiza una empresa.
    Se debe ser el propietario del recurso o un administrador.

    Args:
    - session: Sesión de base de datos (AsyncSession).
    - company_id: Id de la empresa (UUID).
    - update_company: Datos de la empresa a actualizar (UpdateCompany).

    Returns:
    - Datos de la empresa actualizada (Company).
    """

    company: Company = await get_record_by_id(session, Company, company_id, options=joinedload(Company.user).joinedload(User.address))

    update_model(company, update_company.model_dump())

    # cambiamos la direccion obteniendo la direccion de la base de datos
    company.user.address = await get_address_from_db(session, update_company.user.address)

    await secure_commit(session)

    return company

@company_route.patch("/{company_id}/", response_model=ReadCompany, dependencies=[Depends(PermissionsManager.is_company_resource_owner)])
async def partial_update_company(
                        session: Annotated[AsyncSession, Depends(get_session)],
                        company_id: Annotated[UUID, USER_ID],
                        update_company: PartialUpdateCompany) -> Company:
    
    """
    Actualiza una empresa. Solo actualiza los campos que se le pasen.
    Se debe ser el propietario del recurso o un administrador.

    Args:
    - session: Sesión de base de datos (AsyncSession).
    - company_id: Id de la empresa (UUID).
    - update_company: Datos de la empresa a actualizar (PartialUpdateCompany).

    Returns:
    - Datos de la empresa actualizada (Company).
    """

    company: Company = await get_record_by_id(session, Company, company_id, options=joinedload(Company.user).joinedload(User.address))

    update_model(company, update_company.model_dump(exclude_unset=True))

    # si se especificado  la direccion la cambiamos obteniendo la direccion de la base de datos
    if update_company.user and update_company.user.address:
        company.user.address = await get_address_from_db(session, update_company.user.address)

    await secure_commit(session)

    return company

@company_route.delete("/{company_id}/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(PermissionsManager.is_company_resource_owner)])
async def delete_company(
                        session: Annotated[AsyncSession, Depends(get_session)],
                        company_id: Annotated[UUID, USER_ID]) -> None:
    """
    Elimina una empresa.
    Se debe ser el propietario del recurso o un administrador.

    Args:
    - session: Sesión de base de datos (AsyncSession).
    - company_id: Id de la empresa (UUID).
    """

    company: Company = await get_record_by_id(session, Company, company_id, options=joinedload(Company.user))

    await session.delete(company.user)

    await secure_commit(session)