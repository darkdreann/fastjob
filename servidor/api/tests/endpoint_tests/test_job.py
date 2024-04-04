import pytest, random
from httpx import AsyncClient
from sqlalchemy import select
from api.tests.test_utils.db_manage_test import get_database_record
from api.models.enums.models import UserType
from api.database.database_models.models import User, Job
from api.tests.test_utils.result_tests import check_request_data_saved, check_request_with_response
from api.security.security import generate_token
from api.tests.test_utils.db_manage_test import DATA


@pytest.fixture(scope="module")
async def test_consts() -> dict:
    """Devuelve las constantes de prueba."""

    ENDPOINT = "/jobs/"

    # se obtiene el primer usuario administrador de la información de prueba
    admin = DATA["User"][UserType.ADMIN.value][0]
    # se obtiene el token de autenticación de un usuario administrador
    admin_token = generate_token(User(**admin)).access_token

    # se obtiene una oferta de trabajo aleatoria de la información de prueba para eliminar
    delete_job = DATA["Job"].pop(random.randrange(len(DATA["Job"])))

    # se obtienen todos los usuarios ofertas de trabajo de la información de prueba
    all_jobs = DATA["Job"]

    # se obtiene un oferta de trabajo aleatorio de la información de prueba
    db_job = random.choice(DATA["Job"])

    # se obtiene el id de un sector, una empresa, una educación y un idioma aleatorios de la información de prueba
    sector_id = random.choice(DATA["Sector"])["id"]
    company_id = random.choice(DATA["Company"])["user_id"]
    education_id = random.choice(DATA["Education"])["id"]
    language_id = random.choice(DATA["Language"])["id"]
    level_language_id = random.choice(DATA["LanguageLevel"])["id"]

    # se obtiene el código postal de la dirección de la oferta de trabajo para las pruebas de actualización mantener la misma dirección y no tener que obtenerla el id de la nueva
    address = next(filter(lambda a: a["id"] == db_job["address_id"], DATA["Address"]))

    # se crea un diccionario con las constantes de prueba y se devuelve
    consts = {
        "admin_token": admin_token,
        "all_jobs": all_jobs,
        "job": db_job,
        "delete_job": delete_job,
        "endpoint": ENDPOINT,
        "sector_id": sector_id,
        "company_id": company_id,
        "education_id": education_id,
        "language_id": language_id,
        "level_id": level_language_id,
        "address": address
    }
    return consts

@pytest.mark.anyio
async def test_get_jobs(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la funcionalidad de obtener todos los ofertas de trabajo a través del endpoint.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # se obtienen todos los usuarios de las constantes de prueba
    jobs = test_consts["all_jobs"]

    # se realiza la petición HTTP
    response = await client.get(ENDPOINT, headers=headers)

    # se obtiene el contenido de la respuesta
    response_json: list = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200

    # se recorren las ofertas de trabajo de la respuesta y se comprueba que los datos son correctos
    for job in jobs:
        job_response = next(filter(lambda u: u["id"] == job["id"], response_json))
        check_request_with_response(job, job_response)

@pytest.mark.anyio
async def test_get_job(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la funcionalidad de obtener una oferta de trabajo mediante el endpoint correspondiente.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # se obtiene la oferta de trabajo de las constantes de prueba y su id
    job = test_consts["job"]
    job_id = job["id"]

    # se realiza la petición HTTP
    response = await client.get(f"{ENDPOINT}{job_id}/", headers=headers)

    # se obtiene el contenido de la respuesta
    response_json: list = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200
    check_request_with_response(job, response_json)

@pytest.mark.anyio
async def test_create_job(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la creación de una oferta de trabajo mediante una solicitud HTTP POST al endpoint correspondiente.
    
    Args:
    - client (AsyncClient): Cliente HTTP para realizar la solicitud.
    - test_consts (dict): Constantes de prueba que contienen la URL del endpoint y el token de administrador.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # se crea un diccionario con los datos de la nueva oferta de trabajo
    new_job = {
        "job": {
            "title": "prueba",
            "description": "prueba",
            "skills": [
                "prueba"
            ],
            "work_schedule": "FULL-TIME",
            "required_experience": 12,
            "active": True,
            "address": {
                "postal_code": 25000,
                "street": "prueba",
                "city": "prueba",
                "province": "prueba"
            },
            "required_education": test_consts['education_id'],
            "sector_id": test_consts['sector_id'],
            "company_id": test_consts['company_id']
        },
        "job_languages": [
            {
                "language_id": test_consts['language_id'],
                "level_id": test_consts['level_id']
            }
        ]
    }

    # se realiza la petición HTTP
    response = await client.post(ENDPOINT, headers=headers, json=new_job)

    del new_job["job"]["required_education"]

    # se obtiene el contenido de la respuesta
    response_json = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 201
    check_request_with_response(new_job["job"], response_json)
    # se obtiene el id de la oferta de trabajo creada
    new_job_id = response_json["id"]
    # se obtiene la oferta de trabajo de la base de datos y se comprueba que los datos son correctos
    job_db = await get_database_record(select(Job).where(Job.id == new_job_id), only_one=True)
    check_request_data_saved(new_job["job"], record=job_db)


@pytest.mark.anyio
async def test_update_job(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la actualización de una oferta de trabajo mediante una solicitud HTTP PUT al endpoint correspondiente.
    
    Args:
    - client (AsyncClient): Cliente HTTP para realizar la solicitud.
    - test_consts (dict): Constantes de prueba que contienen la URL del endpoint y el token de administrador.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # obtenemos los datos de la oferta de trabajo a actualizar y su id
    job: dict = test_consts["job"]
    job_id = job["id"]

    # se crea un diccionario con los datos de la nueva oferta de trabajo
    update_job = {
        "title": "update",
        "description": "update",
        "skills": [
            "update"
        ],
        "work_schedule": "FULL-TIME",
        "required_experience": 13,
        "active": False,
        "address": {
            "postal_code": test_consts['address']["postal_code"],
            "street": test_consts['address']["street"],
            "city": test_consts['address']["city"],
            "province": test_consts['address']["province"]
        },
        "required_education": test_consts['education_id'],
        "sector_id": test_consts['sector_id'],
        "company_id": test_consts['company_id']
    }
    
    # se realiza la petición HTTP
    response = await client.put(f"{ENDPOINT}{job_id}/", headers=headers, json=update_job)

    del update_job["required_education"]
    # se actualizan los datos de la oferta de trabajo
    job.update(update_job)

    # se obtiene el contenido de la respuesta
    response_json = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200
    check_request_with_response(job, response_json)
    # se obtiene la oferta de trabajo de la base de datos y se comprueba que los datos son correctos
    job_db = await get_database_record(select(Job).where(Job.id == job_id), only_one=True)
    check_request_data_saved(job, record=job_db)


@pytest.mark.anyio
async def test_partial_update_job(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la actualización parcial de una oferta de trabajo mediante una solicitud HTTP PATCH al endpoint correspondiente.
    
    Args:
    - client (AsyncClient): Cliente HTTP para realizar la solicitud.
    - test_consts (dict): Constantes de prueba que contienen la URL del endpoint y el token de administrador.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # obtenemos los datos de la oferta de trabajo a actualizar y su id
    job: dict = test_consts["job"]
    job_id = job["id"]

    # se crea un diccionario con los datos de la nueva oferta de trabajo
    update_job = {
        "title": "update2",
        "description": "update2",
        "skills": [
            "update",
            "update2"
        ],
    }

    # se realiza la petición HTTP
    response = await client.patch(f"{ENDPOINT}{job_id}/", headers=headers, json=update_job)

    # se actualizan los datos de la oferta de trabajo
    job.update(update_job)

    # se obtiene el contenido de la respuesta
    response_json = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200
    check_request_with_response(job, response_json)
    # se obtiene la oferta de trabajo de la base de datos y se comprueba que los datos son correctos
    job_db = await get_database_record(select(Job).where(Job.id == job_id), only_one=True)
    check_request_data_saved(job, record=job_db)

@pytest.mark.anyio
async def test_delete_job(client: AsyncClient, test_consts: dict):
    """
    Prueba la eliminación de una oferta de trabajo mediante una solicitud HTTP DELETE al endpoint correspondiente.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # obtenemos los datos de la oferta de trabajo a actualizar y su id
    job: dict = test_consts["delete_job"]
    job_id = job["id"]

    # se realiza la petición HTTP
    response = await client.delete(f"{ENDPOINT}{job_id}/", headers=headers)

    # se comprueba que la respuesta es correcta
    assert response.status_code == 204

    # se obtiene la oferta de trabajo de la base de datos y se comprueba que no existe
    job_db = await get_database_record(select(Job).where(Job.id == job_id), only_one=True)
    assert job_db is None
