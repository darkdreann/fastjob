import pytest, random
from httpx import AsyncClient
from uuid import uuid4
from sqlalchemy import select
from api.tests.test_utils.db_manage_test import get_database_record, save_database_record
from api.models.enums.models import UserType
from api.database.database_models.models import User, Address
from api.tests.test_utils.result_tests import check_request_data_saved, check_request_with_response
from api.security.security import generate_token
from api.tests.test_utils.db_manage_test import DATA

@pytest.fixture(scope="module")
async def test_consts() -> dict:
    """Devuelve las constantes de prueba."""

    ENDPOINT = "/addresses/"

    # se obtiene el primer usuario administrador de la información de prueba
    admin = DATA["User"][UserType.ADMIN.value][0]
    # se obtiene el token de autenticación de un usuario administrador
    admin_token = generate_token(User(**admin)).access_token

    # se obtiene una dirección aleatoria de la información de prueba
    address = random.choice(DATA["Address"])

    # se crea una dirección para eliminar y se guarda en la base de datos para evitar que tenga relaciones
    delete_address = {
        "id": uuid4(),
        "postal_code": 10000,
        "street": "calle delete",
        "city": "delete",
        "province": "delete"
    }
    await save_database_record(Address(**delete_address))

    # se crea un diccionario con las constantes de prueba y se devuelve
    consts = {
        "admin_token": admin_token,
        "all_address": DATA["Address"],
        "address": address,
        "delete_address": delete_address,
        "endpoint": ENDPOINT
    }
    return consts

@pytest.mark.anyio
async def test_get_addresses(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la funcionalidad de obtener todas las direcciones a través del endpoint.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # se obtienen todos los usuarios de las constantes de prueba
    addresses = test_consts["all_address"]

    # se realiza la petición HTTP
    response = await client.get(ENDPOINT, headers=headers)

    # se obtiene el contenido de la respuesta
    response_json: list = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200

    # se recorren las direcciones de la respuesta y se comprueba que los datos son correctos
    for address in addresses:
        address_from_response = next(filter(lambda u: u["id"] == address["id"], response_json))
        check_request_with_response(address, address_from_response)


@pytest.mark.anyio
async def test_get_address(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la funcionalidad de obtener una dirección mediante una petición GET al endpoint.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Diccionario con las constantes de prueba.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}
    # se obtiene la dirección de las constantes de prueba
    address = test_consts["address"]
    # se obtiene el id de la dirección de las constantes de prueba
    address_id = address["id"]

    # se realiza la petición HTTP
    response = await client.get(f"{ENDPOINT}{address_id}/", headers=headers)

    # se obtiene el contenido de la respuesta
    response_json = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200
    check_request_with_response(address, response_json)


@pytest.mark.anyio
async def test_create_address(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la creación de una nueva dirección mediante una petición HTTP POST al endpoint especificado.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar la petición.
    - test_consts (dict): Constantes de prueba que contienen la URL del endpoint y el token de autenticación.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # se crea un diccionario con los datos de la nueva dirección
    new_address = {
        "postal_code": 19999,
        "street": "calle falsa",
        "city": "vigo",
        "province": "pontevedra"
    }

    # se realiza la petición HTTP
    response = await client.post(ENDPOINT, headers=headers, json=new_address)

    # se obtiene el contenido de la respuesta
    response_json = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 201
    check_request_with_response(new_address, response_json)
    # se obtiene la dirección de la base de datos y se comprueba que los datos son correctos
    database_address = await get_database_record(select(Address).where(Address.postal_code == new_address["postal_code"]), only_one=True)
    check_request_data_saved(new_address, record=database_address)

@pytest.mark.anyio
async def test_update_address(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la funcionalidad de actualización de una dirección en el endpoint correspondiente.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Diccionario con las constantes de prueba.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # se obtiene la dirección de las constantes de prueba y su id
    address: dict = test_consts["address"]
    address_id = address["id"]

    # se crea un diccionario con los datos de la dirección actualizados
    updated_address = {
        "postal_code": 18123,
        "street": "calle falsa",
        "city": "vigo",
        "province": "pontevedra"
    }

    address.update(updated_address)

    # se realiza la petición HTTP
    response = await client.put(f"{ENDPOINT}{address_id}/", headers=headers, json=updated_address)

    # se obtiene el contenido de la respuesta
    response_json = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200
    check_request_with_response(address, response_json)
    # se obtiene la dirección de la base de datos y se comprueba que los datos son correctos
    database_address = await get_database_record(select(Address).where(Address.id == address_id), only_one=True)
    check_request_data_saved(address, record=database_address)


@pytest.mark.anyio
async def test_partial_update_address(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la actualización parcial de una dirección.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # se obtiene la dirección de las constantes de prueba y su id
    address: dict = test_consts["address"]
    address_id = address["id"]

    # se crea un diccionario con los datos de la dirección actualizados
    updated_address = {
        "street": "calle falsa",
        "city": "vigo"
    }

    address.update(updated_address)

    # se realiza la petición HTTP
    response = await client.patch(f"{ENDPOINT}{address_id}/", headers=headers, json=updated_address)

    # se obtiene el contenido de la respuesta
    response_json = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200
    check_request_with_response(address, response_json)
    # se obtiene la dirección de la base de datos y se comprueba que los datos son correctos
    database_address = await get_database_record(select(Address).where(Address.id == address_id), only_one=True)
    check_request_data_saved(address, record=database_address)


@pytest.mark.anyio
async def test_delete_address(client: AsyncClient, test_consts: dict):
    """
    Prueba la funcionalidad de eliminación de una dirección en el endpoint correspondiente.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # se obtiene la direccion para eliminar de las constantes de prueba y su id
    address: dict = test_consts["delete_address"]
    address_id = address["id"]

    # se realiza la petición HTTP
    response = await client.delete(f"{ENDPOINT}{address_id}/", headers=headers)

    # se comprueba que la respuesta es correcta
    assert response.status_code == 204

    # se obtiene la dirección de la base de datos y se comprueba que no existe
    user = await get_database_record(select(Address).where(Address.id == address_id), only_one=True)
    assert user is None