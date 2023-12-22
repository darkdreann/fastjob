import pytest, random
from httpx import AsyncClient
from uuid import uuid4
from sqlalchemy import select
from api.tests.test_utils.db_manage_test import get_database_record, save_database_record
from api.models.enums.models import UserType
from api.database.database_models.models import User, Sector
from api.tests.test_utils.result_tests import check_request_data_saved, check_request_with_response
from api.security.security import generate_token
from api.tests.test_utils.db_manage_test import DATA


@pytest.fixture(scope="module")
async def test_consts() -> dict:
    """Devuelve las constantes de prueba."""

    ENDPOINT = "/sectors/"

    # se obtiene el primer usuario administrador de la lista de prueba
    admin = DATA["User"][UserType.ADMIN.value][0]
    # se obtiene el token de autenticación de un usuario administrador
    admin_token = generate_token(User(**admin)).access_token

    # se obtienen todos los sectores de la lista de prueba
    all_sector = DATA["Sector"]

    # se obtiene un sector aleatorio de la lista de prueba
    sector = random.choice(DATA["Sector"])

    delete_sector = {
        "id": uuid4(),
        "category": "IT",
        "subcategory": "ciberseguridad"
    }

    await save_database_record(Sector(**delete_sector))

    # se crea un diccionario con las constantes de prueba y se devuelve
    consts = {
        "admin_token": admin_token,
        "all_sector": all_sector,
        "sector": sector,
        "delete_sector": delete_sector,
        "endpoint": ENDPOINT
    }
    return consts

@pytest.mark.anyio
async def test_get_sector(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la funcionalidad de obtener todos los sectores a través del endpoint.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # se obtienen todos los sectores de las constantes de prueba
    all_sector = test_consts["all_sector"]

    # se realiza la petición HTTP
    response = await client.get(ENDPOINT, headers=headers)

    # se obtiene el contenido de la respuesta
    response_json: list = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200

    # se recorren los sectores de la respuesta y se comprueba que los datos son correctos
    for sector in all_sector:
        sector_response = next(filter(lambda u: u["id"] == sector["id"], response_json))
        check_request_with_response(sector, sector_response)

@pytest.mark.anyio
async def test_get_sector(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la funcionalidad de obtener un sector mediante el endpoint correspondiente.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # se obtiene el sector de las constantes de prueba y su id
    sector = test_consts["sector"]
    sector_id = sector["id"]

    # se realiza la petición HTTP
    response = await client.get(f"{ENDPOINT}{sector_id}/", headers=headers)

    # se obtiene el contenido de la respuesta
    response_json: list = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200
    check_request_with_response(sector, response_json)

@pytest.mark.anyio
async def test_create_sector(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la creación de un sector mediante una solicitud HTTP POST al endpoint correspondiente.
    
    Args:
    - client (AsyncClient): Cliente HTTP para realizar la solicitud.
    - test_consts (dict): Constantes de prueba que contienen la URL del endpoint y el token de administrador.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # se crea un diccionario con los datos del nuevo sector
    new_sector = {
        "category": "prueba",
        "subcategory": "prueba"
    }

    # se realiza la petición HTTP
    response = await client.post(ENDPOINT, headers=headers, json=new_sector)

    # se obtiene el contenido de la respuesta
    response_json = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 201
    check_request_with_response(new_sector, response_json)
    # se obtiene el id del sector creado
    new_sector_id = response_json["id"]
    # se obtiene el sector de la base de datos y se comprueba que los datos son correctos
    sector_db = await get_database_record(select(Sector).where(Sector.id == new_sector_id), only_one=True)
    check_request_data_saved(new_sector, record=sector_db)


@pytest.mark.anyio
async def test_update_sector(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la actualización de un sector mediante una solicitud HTTP PUT al endpoint correspondiente.
    
    Args:
    - client (AsyncClient): Cliente HTTP para realizar la solicitud.
    - test_consts (dict): Constantes de prueba que contienen la URL del endpoint y el token de administrador.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # se obtiene el sector de las constantes de prueba y su id
    sector: dict = test_consts["sector"]
    sector_id = sector["id"]

    # se crea un diccionario con los datos del nuevo sector
    update_sector = {
        "category": "update",
        "subcategory": "update"
    }

    
    # se realiza la petición HTTP
    response = await client.put(f"{ENDPOINT}{sector_id}/", headers=headers, json=update_sector)

    # se actualizan los datos del sector
    sector.update(update_sector)

    # se obtiene el contenido de la respuesta
    response_json = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200
    check_request_with_response(sector, response_json)
    # se obtiene el sector de la base de datos y se comprueba que los datos son correctos
    sector_db = await get_database_record(select(Sector).where(Sector.id == sector_id), only_one=True)
    check_request_data_saved(sector, record=sector_db)


@pytest.mark.anyio
async def test_partial_update_education(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la actualización parcial de una sector mediante una solicitud HTTP PATCH al endpoint correspondiente.
    
    Args:
    - client (AsyncClient): Cliente HTTP para realizar la solicitud.
    - test_consts (dict): Constantes de prueba que contienen la URL del endpoint y el token de administrador.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # se obtiene el sector de las constantes de prueba y su id
    sector: dict = test_consts["sector"]
    sector_id = sector["id"]

    # se crea un diccionario con los datos del nuevo sector
    update_sector = {
        "category": "update2",
    }

    # se realiza la petición HTTP
    response = await client.patch(f"{ENDPOINT}{sector_id}/", headers=headers, json=update_sector)

    # se actualizan los datos de la sector
    sector.update(update_sector)

    # se obtiene el contenido de la respuesta
    response_json = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200
    check_request_with_response(sector, response_json)
    # se obtiene la sector de la base de datos y se comprueba que los datos son correctos
    sector_db = await get_database_record(select(Sector).where(Sector.id == sector_id), only_one=True)
    check_request_data_saved(sector, record=sector_db)

@pytest.mark.anyio
async def test_delete_sector(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la eliminación de un sector mediante una solicitud HTTP DELETE al endpoint correspondiente.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # se obtiene el sector de las constantes de prueba y su id
    sector: dict = test_consts["delete_sector"]
    sector_id = sector["id"]

    # se realiza la petición HTTP
    response = await client.delete(f"{ENDPOINT}{sector_id}/", headers=headers)

    # se comprueba que la respuesta es correcta
    assert response.status_code == 204

    # se obtiene el sector de la base de datos y se comprueba que no existe
    sector_db = await get_database_record(select(Sector).where(Sector.id == sector_id), only_one=True)
    assert sector_db is None
