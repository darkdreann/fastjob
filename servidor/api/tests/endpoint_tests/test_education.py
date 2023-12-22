import pytest, random
from httpx import AsyncClient
from uuid import uuid4
from sqlalchemy import select
from api.tests.test_utils.db_manage_test import get_database_record, save_database_record
from api.models.enums.models import UserType
from api.database.database_models.models import User, Education
from api.tests.test_utils.result_tests import check_request_data_saved, check_request_with_response
from api.security.security import generate_token
from api.tests.test_utils.db_manage_test import DATA


@pytest.fixture(scope="module")
async def test_consts() -> dict:
    """Devuelve las constantes de prueba."""

    ENDPOINT = "/educations/"

    # se obtiene el primer usuario administrador de la información de prueba
    admin = DATA["User"][UserType.ADMIN.value][0]
    # se obtiene el token de autenticación de un usuario administrador
    admin_token = generate_token(User(**admin)).access_token

    # se obtienen todos los usuarios formaciones de la información de prueba
    all_education = DATA["Education"]

    # se obtiene un formación aleatorio de la información de prueba
    education = random.choice(DATA["Education"])

    # se obtiene el id de un nivel de formación y un sector aleatorio de la información de prueba
    education_level_id = random.choice(DATA["EducationLevel"])["id"]
    sector_id = random.choice(DATA["Sector"])["id"]

    delete_education = {
        "id": uuid4(),
        "qualification": "DELETE",
        "level_id": education_level_id
    }

    await save_database_record(Education(**delete_education))

    # se crea un diccionario con las constantes de prueba y se devuelve
    consts = {
        "admin_token": admin_token,
        "all_education": all_education,
        "education": education,
        "delete_education": delete_education,
        "education_level_id": education_level_id,
        "sector_id": sector_id,
        "endpoint": ENDPOINT
    }
    return consts

@pytest.mark.anyio
async def test_get_educations(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la funcionalidad de obtener todos los formaciones a través del endpoint.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # se obtienen todos los usuarios de las constantes de prueba
    educations = test_consts["all_education"]

    # se realiza la petición HTTP
    response = await client.get(ENDPOINT, headers=headers)

    # se obtiene el contenido de la respuesta
    response_json: list = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200

    # se recorren las formaciones de la respuesta y se comprueba que los datos son correctos
    for education in educations:
        education_response = next(filter(lambda u: u["id"] == education["id"], response_json))
        check_request_with_response(education, education_response)

@pytest.mark.anyio
async def test_get_education(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la funcionalidad de obtener una formación mediante el endpoint correspondiente.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # se obtiene la formación de las constantes de prueba y su id
    education = test_consts["education"]
    education_id = education["id"]

    # se realiza la petición HTTP
    response = await client.get(f"{ENDPOINT}{education_id}/", headers=headers)

    # se obtiene el contenido de la respuesta
    response_json: list = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200
    check_request_with_response(education, response_json)

@pytest.mark.anyio
async def test_create_education(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la creación de una formación mediante una solicitud HTTP POST al endpoint correspondiente.
    
    Args:
    - client (AsyncClient): Cliente HTTP para realizar la solicitud.
    - test_consts (dict): Constantes de prueba que contienen la URL del endpoint y el token de administrador.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # se crea un diccionario con los datos de la nueva formación
    new_education = {
        "qualification": "Prueba de formación",
        "level_id": test_consts['education_level_id'],
        "sector_id": test_consts['sector_id']
    }

    

    # se realiza la petición HTTP
    response = await client.post(ENDPOINT, headers=headers, json=new_education)

    # se quita el sector_id del diccionario de la formación
    del new_education["sector_id"]

    # se obtiene el contenido de la respuesta
    response_json = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 201
    check_request_with_response(new_education, response_json)
    # se obtiene el id de la formación creada
    new_education_id = response_json["id"]
    # se obtiene la formación de la base de datos y se comprueba que los datos son correctos
    education_db = await get_database_record(select(Education).where(Education.id == new_education_id), only_one=True)
    check_request_data_saved(new_education, record=education_db)


@pytest.mark.anyio
async def test_update_job(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la actualización de una formación mediante una solicitud HTTP PUT al endpoint correspondiente.
    
    Args:
    - client (AsyncClient): Cliente HTTP para realizar la solicitud.
    - test_consts (dict): Constantes de prueba que contienen la URL del endpoint y el token de administrador.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # obtenemos los datos de la formación a actualizar y su id
    education: dict = test_consts["education"]
    education_id = education["id"]

    # se crea un diccionario con los datos de la nueva formación
    update_education = {
        "qualification": "Prueba de formación update",
        "level_id": test_consts['education_level_id'],
        "sector_id": test_consts['sector_id']
    }
    
    # se realiza la petición HTTP
    response = await client.put(f"{ENDPOINT}{education_id}/", headers=headers, json=update_education)

    # se quita el sector_id del diccionario de la formación
    del update_education["sector_id"]

    # se actualizan los datos de la formación
    education.update(update_education)

    # se obtiene el contenido de la respuesta
    response_json = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200
    check_request_with_response(education, response_json)
    # se obtiene la formación de la base de datos y se comprueba que los datos son correctos
    education_db = await get_database_record(select(Education).where(Education.id == education_id), only_one=True)
    check_request_data_saved(education, record=education_db)


@pytest.mark.anyio
async def test_partial_update_education(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la actualización parcial de una formación mediante una solicitud HTTP PATCH al endpoint correspondiente.
    
    Args:
    - client (AsyncClient): Cliente HTTP para realizar la solicitud.
    - test_consts (dict): Constantes de prueba que contienen la URL del endpoint y el token de administrador.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # obtenemos los datos de la formación a actualizar y su id
    education: dict = test_consts["education"]
    education_id = education["id"]

    # se crea un diccionario con los datos de la nueva formación
    update_education = {
        "qualification": "Prueba de formación update 2",
    }

    # se realiza la petición HTTP
    response = await client.patch(f"{ENDPOINT}{education_id}/", headers=headers, json=update_education)

    # se actualizan los datos de la formación
    education.update(update_education)

    # se obtiene el contenido de la respuesta
    response_json = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200
    check_request_with_response(education, response_json)
    # se obtiene la formación de la base de datos y se comprueba que los datos son correctos
    education_db = await get_database_record(select(Education).where(Education.id == education_id), only_one=True)
    check_request_data_saved(education, record=education_db)

@pytest.mark.anyio
async def test_delete_education(client: AsyncClient, test_consts: dict):
    """
    Prueba la eliminación de una formación mediante una solicitud HTTP DELETE al endpoint correspondiente.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # obtenemos los datos de la formación a actualizar y su id
    education: dict = test_consts["delete_education"]
    education_id = education["id"]

    # se realiza la petición HTTP
    response = await client.delete(f"{ENDPOINT}{education_id}/", headers=headers)

    # se comprueba que la respuesta es correcta
    assert response.status_code == 204

    # se obtiene la formación de la base de datos y se comprueba que no existe
    education_db = await get_database_record(select(Education).where(Education.id == education_id), only_one=True)
    assert education_db is None
