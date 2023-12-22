import pytest, random
from httpx import AsyncClient
from uuid import uuid4
from sqlalchemy import select
from api.tests.test_utils.db_manage_test import get_database_record, save_database_record
from api.models.enums.models import UserType
from api.database.database_models.models import User, Language
from api.tests.test_utils.result_tests import check_request_data_saved, check_request_with_response
from api.security.security import generate_token
from api.tests.test_utils.db_manage_test import DATA


@pytest.fixture(scope="module")
async def test_consts() -> dict:
    """Devuelve las constantes de prueba."""

    ENDPOINT = "/languages/"

    # se obtiene el primer usuario administrador de la lista de prueba
    admin = DATA["User"][UserType.ADMIN.value][0]
    # se obtiene el token de autenticación de un usuario administrador
    admin_token = generate_token(User(**admin)).access_token

    # se obtienen todos los idiomas de la lista de prueba
    all_languages = DATA["Language"]

    # se obtiene un idioma aleatorio de la lista de prueba
    language = random.choice(DATA["Language"])

    delete_language = {
        "id": uuid4(),
        "name": "frances"
    }

    await save_database_record(Language(**delete_language))

    # se crea un diccionario con las constantes de prueba y se devuelve
    consts = {
        "admin_token": admin_token,
        "all_languages": all_languages,
        "language": language,
        "delete_language": delete_language,
        "endpoint": ENDPOINT
    }
    return consts

@pytest.mark.anyio
async def test_get_languages(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la funcionalidad de obtener todos los idiomas a través del endpoint.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # se obtienen todos los idiomas de las constantes de prueba
    languages = test_consts["all_languages"]

    # se realiza la petición HTTP
    response = await client.get(ENDPOINT, headers=headers)

    # se obtiene el contenido de la respuesta
    response_json: list = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200

    # se recorren los idiomas de la respuesta y se comprueba que los datos son correctos
    for language in languages:
        language_response = next(filter(lambda u: u["id"] == language["id"], response_json))
        check_request_with_response(language, language_response)

@pytest.mark.anyio
async def test_get_language(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la funcionalidad de obtener un idioma mediante el endpoint correspondiente.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # se obtiene el idioma de las constantes de prueba y su id
    language = test_consts["language"]
    language_id = language["id"]

    # se realiza la petición HTTP
    response = await client.get(f"{ENDPOINT}{language_id}/", headers=headers)

    # se obtiene el contenido de la respuesta
    response_json: list = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200
    check_request_with_response(language, response_json)

@pytest.mark.anyio
async def test_create_language(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la creación de un idioma mediante una solicitud HTTP POST al endpoint correspondiente.
    
    Args:
    - client (AsyncClient): Cliente HTTP para realizar la solicitud.
    - test_consts (dict): Constantes de prueba que contienen la URL del endpoint y el token de administrador.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # se crea un diccionario con los datos del nuevo idioma
    new_language = {
        "name": "aleman"
    }

    # se realiza la petición HTTP
    response = await client.post(ENDPOINT, headers=headers, json=new_language)

    # se obtiene el contenido de la respuesta
    response_json = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 201
    check_request_with_response(new_language, response_json)
    # se obtiene el id del idioma creado
    new_language_id = response_json["id"]
    # se obtiene el idioma de la base de datos y se comprueba que los datos son correctos
    language_db = await get_database_record(select(Language).where(Language.id == new_language_id), only_one=True)
    check_request_data_saved(new_language, record=language_db)


@pytest.mark.anyio
async def test_update_language(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la actualización de un idioma mediante una solicitud HTTP PUT al endpoint correspondiente.
    
    Args:
    - client (AsyncClient): Cliente HTTP para realizar la solicitud.
    - test_consts (dict): Constantes de prueba que contienen la URL del endpoint y el token de administrador.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # se obtiene el idioma de las constantes de prueba y su id
    language: dict = test_consts["language"]
    language_id = language["id"]

    # se crea un diccionario con los datos del nuevo idioma
    update_language = {
        "name": "italiano"
    }
    
    # se realiza la petición HTTP
    response = await client.put(f"{ENDPOINT}{language_id}/", headers=headers, json=update_language)

    # se actualizan los datos del idioma
    language.update(update_language)

    # se obtiene el contenido de la respuesta
    response_json = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200
    check_request_with_response(language, response_json)
    # se obtiene el idioma de la base de datos y se comprueba que los datos son correctos
    language_db = await get_database_record(select(Language).where(Language.id == language_id), only_one=True)
    check_request_data_saved(language, record=language_db)


@pytest.mark.anyio
async def test_delete_language(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la eliminación de un idioma mediante una solicitud HTTP DELETE al endpoint correspondiente.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # se obtiene el idioma a eliminar de las constantes de prueba y su id
    language: dict = test_consts["delete_language"]
    language_id = language["id"]

    # se realiza la petición HTTP
    response = await client.delete(f"{ENDPOINT}{language_id}/", headers=headers)

    # se comprueba que la respuesta es correcta
    assert response.status_code == 204

    # se obtiene el idioma de la base de datos y se comprueba que no existe
    language_db = await get_database_record(select(Language).where(Language.id == language_id), only_one=True)
    assert language_db is None
