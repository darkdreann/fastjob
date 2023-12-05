from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import noload, joinedload
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
from api.utils.constants.endpoints_params import LIMIT, OFFSET, DEFAULT_LIMIT, DEFAULT_OFFSET, USER_ID, COMPANIES_GET_JOBS
from api.utils.functions.management_utils import endpoint_request_log
from api.utils.functions.models_utils import update_model, get_address_from_db

company_route = APIRouter(prefix="/companies", tags=["companies"], dependencies=[Depends(endpoint_request_log)])

@company_route.get("/", response_model=list[ReadCompanyComplete], response_model_exclude_defaults=True, dependencies=[Depends(PermissionsManager.is_admin)])
async def get_companies(
                        session: Annotated[AsyncSession, Depends(get_session)], 
                        limit: Annotated[int, DEFAULT_LIMIT]=DEFAULT_LIMIT,
                        offset: Annotated[int, DEFAULT_OFFSET]=DEFAULT_OFFSET,
                        get_jobs: Annotated[bool, COMPANIES_GET_JOBS]=False) -> list[Company]:
    """
    Obtiene una lista de empresas.

    Args:
    - session: Sesión de base de datos (AsyncSession).
    - limit: Límite de resultados a devolver (int, opcional).
    - offset: Desplazamiento de resultados (int, opcional).
    - get_jobs: Indica si se deben incluir los trabajos asociados a las empresas (bool, opcional).

    Return:
    - Lista de empresas (list[Company]).
    """
    options = [joinedload(Company.user).joinedload(User.address)]
    
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

    Args:
    - session: Sesión de base de datos (AsyncSession).
    - company_id: Id de la empresa (UUID).
    - get_jobs: Indica si se deben incluir los trabajos asociados a las empresas (bool, opcional).

    Return:
    - Datos de la empresa (Company).
    """

    options = [joinedload(Company.user).joinedload(User.address)]
    
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

    Args:
    - session: Sesión de base de datos (AsyncSession).
    - company: Datos de la empresa a crear (CreateCompany).

    Returns:
    - Datos de la empresa creada (Company).
    """

    address = await get_address_from_db(session, new_company.user.address)

    user = User(**new_company.user.model_dump(), user_type=UserType.COMPANY, address=address)

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

    Args:
    - session: Sesión de base de datos (AsyncSession).
    - company_id: Id de la empresa (UUID).
    - company: Datos de la empresa a actualizar (CreateCompany).

    Returns:
    - Datos de la empresa actualizada (Company).
    """

    company: Company = await get_record_by_id(session, Company, company_id, options=joinedload(Company.user).joinedload(User.address))

    update_model(company, update_company.model_dump())

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

    Args:
    - session: Sesión de base de datos (AsyncSession).
    - company_id: Id de la empresa (UUID).
    - company: Datos de la empresa a actualizar (CreateCompany).

    Returns:
    - Datos de la empresa actualizada (Company).
    """

    company: Company = await get_record_by_id(session, Company, company_id, options=joinedload(Company.user).joinedload(User.address))

    update_model(company, update_company.model_dump(exclude_unset=True))

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

    Args:
    - session: Sesión de base de datos (AsyncSession).
    - company_id: Id de la empresa (UUID).
    """

    company: Company = await get_record_by_id(session, Company, company_id, options=joinedload(Company.user))

    await session.delete(company.user)

    await secure_commit(session)