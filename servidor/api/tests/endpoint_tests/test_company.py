import pytest, random
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.orm import contains_eager
from api.tests.test_utils.db_manage_test import get_database_record
from api.models.enums.models import UserType
from api.database.database_models.models import User, Address, Company
from api.tests.test_utils.result_tests import check_request_data_saved, check_request_with_response
from api.security.security import generate_token
from api.tests.test_utils.db_manage_test import DATA


@pytest.fixture(scope="module")
async def test_consts() -> dict:
    """Devuelve las constantes de prueba."""

    ENDPOINT = "/companies/"

    # se obtiene el primer usuario administrador de la información de prueba
    admin = DATA["User"][UserType.ADMIN.value][0]
    # se obtiene el token de autenticación de un usuario administrador
    admin_token = generate_token(User(**admin)).access_token

    # se obtiene un empresa aleatorio de la información de prueba para eliminar y se elimina de la lista de usuarios empresas
    delete_company_user = DATA["User"][UserType.COMPANY.value].pop(random.randrange(len(DATA["User"][UserType.COMPANY.value])))
    # se obtiene los datos del empresa a eliminar
    delete_company = next(filter(lambda c: c["user_id"] == delete_company_user["id"], DATA["Company"]))
    # se elimina el empresa de la lista de empresas
    DATA["Company"].remove(delete_company)
    # se junta la información de usuario y empresa
    delete_company["user"] = delete_company_user

    # se obtienen todos los usuarios empresas de la información de prueba
    all_company_user = DATA["User"][UserType.COMPANY.value]
    all_company = DATA["Company"]

    # se juntan los datos de usuario y empresa
    for comp in all_company:
        comp["user"] = next(filter(lambda u: u["id"] == comp["user_id"], all_company_user))

    # se obtiene un empresa aleatorio de la información de prueba
    company = random.choice(DATA["Company"])

    # se crea un diccionario con las constantes de prueba y se devuelve
    consts = {
        "admin_token": admin_token,
        "all_company": all_company,
        "company": company,
        "delete_company": delete_company,
        "endpoint": ENDPOINT
    }
    return consts

@pytest.mark.anyio
async def test_get_companies(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la funcionalidad de obtener todos los empresas a través del endpoint.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # se obtienen todos los usuarios de las constantes de prueba
    companies = test_consts["all_company"]

    # se realiza la petición HTTP
    response = await client.get(ENDPOINT, headers=headers)

    # se obtiene el contenido de la respuesta
    response_json: list = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200

    # se recorren las empresas de la respuesta y se comprueba que los datos son correctos
    for company in companies:
        company_from_response = next(filter(lambda u: u["user"]["id"] == company["user_id"], response_json))
        check_request_with_response(company, company_from_response)

@pytest.mark.anyio
async def test_get_company(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la funcionalidad de obtener una empresa mediante el endpoint correspondiente.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # se obtiene la empresa de las constantes de prueba y su id
    company = test_consts["company"]
    company_id = company["user_id"]

    # se realiza la petición HTTP
    response = await client.get(f"{ENDPOINT}{company_id}/", headers=headers)

    # se obtiene el contenido de la respuesta
    response_json: list = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200
    check_request_with_response(company, response_json)

@pytest.mark.anyio
async def test_create_company(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la creación de una empresa mediante una solicitud HTTP POST al endpoint correspondiente.
    
    Args:
    - client (AsyncClient): Cliente HTTP para realizar la solicitud.
    - test_consts (dict): Constantes de prueba que contienen la URL del endpoint y el token de administrador.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # se crea un diccionario con los datos de la nueva empresa
    new_company = {
    "tin": "K84465930",
    "company_name": "Meta",
    "user": {
        "username": "meta1",
        "email": "meta1@example.com",
        "name": "raul",
        "surname": "rodriguez",
        "phone_numbers": [
            613985123
        ],
        "password": "Password12!",
        "address": {
                "postal_code": 16000,
                "street": "prueba",
                "city": "prueba",
                "province": "prueba"
            }
        }
    }

    # se realiza la petición HTTP
    response = await client.post(ENDPOINT, headers=headers, json=new_company)

    # se obtiene el contenido de la respuesta
    response_json = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 201
    check_request_with_response(new_company, response_json)
    # se obtiene la empresa de la base de datos y se comprueba que los datos son correctos
    company_db = await get_database_record(select(Company).where(User.username == new_company["user"]["username"])
                                                .join(
                                                    target=User,
                                                onclause=User.id == Company.user_id
                                                )
                                                .join(
                                                    target=Address,
                                                    onclause=Address.id == User.address_id
                                                )
                                                .options(contains_eager(Company.user).contains_eager(User.address)), only_one=True)
    check_request_data_saved(new_company, record=company_db, user_type=UserType.COMPANY)



@pytest.mark.anyio
async def test_update_company(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la actualización de una empresa mediante una solicitud HTTP PUT al endpoint correspondiente.
    
    Args:
    - client (AsyncClient): Cliente HTTP para realizar la solicitud.
    - test_consts (dict): Constantes de prueba que contienen la URL del endpoint y el token de administrador.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # obtenemos los datos de la empresa a actualizar y su id
    company: dict = test_consts["company"]
    company_id = company["user_id"]

    # se crea un diccionario con los datos de la nueva empresa
    update_company = {
    "tin": "T12465930",
    "company_name": "NEW_Meta",
    "user": {
        "username": "new_meta",
        "email": "new_meta@example.com",
        "name": "new_meta",
        "surname": "new_meta",
        "phone_numbers": [
            613985123
        ],
        "password": "Password12!",
        "address": {
                "postal_code": 16000,
                "street": "prueba",
                "city": "prueba",
                "province": "prueba"
            }
        }
    }

    # se realiza la petición HTTP
    response = await client.put(f"{ENDPOINT}{company_id}/", headers=headers, json=update_company)

    # se actualizan los datos de la empresa
    company.update(update_company)

    # se obtiene el contenido de la respuesta
    response_json = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200
    check_request_with_response(company, response_json)
    # se obtiene la empresa de la base de datos y se comprueba que los datos son correctos
    company_db = await get_database_record(select(Company).where(User.username == update_company["user"]["username"])
                                                .join(
                                                    target=User,
                                                onclause=User.id == Company.user_id
                                                )
                                                .join(
                                                    target=Address,
                                                    onclause=Address.id == User.address_id
                                                )
                                                .options(contains_eager(Company.user).contains_eager(User.address)), only_one=True)
    check_request_data_saved(company, record=company_db, user_type=UserType.COMPANY)


@pytest.mark.anyio
async def test_partial_update_company(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la actualización parcial de una empresa mediante una solicitud HTTP PATCH al endpoint correspondiente.
    
    Args:
    - client (AsyncClient): Cliente HTTP para realizar la solicitud.
    - test_consts (dict): Constantes de prueba que contienen la URL del endpoint y el token de administrador.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # obtenemos los datos de la empresa a actualizar y su id
    company: dict = test_consts["company"]
    company_id = company["user_id"]

    # se crea un diccionario con los datos de la nueva empresa
    update_company = {
        "user": {
            "username": "new_meta2",
            "email": "new_meta2@example.com",
            "password": "actualizadO12!",
        }
    }

    # se realiza la petición HTTP
    response = await client.patch(f"{ENDPOINT}{company_id}/", headers=headers, json=update_company)

    # se actualizan los datos de la empresa
    company.update(update_company)

    # se obtiene el contenido de la respuesta
    response_json = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200
    check_request_with_response(company, response_json)
    # se obtiene la empresa de la base de datos y se comprueba que los datos son correctos
    company_db = await get_database_record(select(Company).where(User.username == update_company["user"]["username"])
                                                .join(
                                                    target=User,
                                                onclause=User.id == Company.user_id
                                                )
                                                .join(
                                                    target=Address,
                                                    onclause=Address.id == User.address_id
                                                )
                                                .options(contains_eager(Company.user).contains_eager(User.address)), only_one=True)
    check_request_data_saved(company, record=company_db, user_type=UserType.COMPANY)

@pytest.mark.anyio
async def test_delete_company(client: AsyncClient, test_consts: dict):
    """
    Prueba la eliminación de una empresa mediante una solicitud HTTP DELETE al endpoint correspondiente.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # obtenemos los datos de la empresa a actualizar y su id
    company: dict = test_consts["delete_company"]
    company_id = company["user_id"]

    # se realiza la petición HTTP
    response = await client.delete(f"{ENDPOINT}{company_id}/", headers=headers)

    # se comprueba que la respuesta es correcta
    assert response.status_code == 204

    # se obtiene la empresa de la base de datos y se comprueba que no existe
    user = await get_database_record(select(Company).where(Company.user_id == company_id), only_one=True)
    assert user is None
