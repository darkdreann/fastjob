import pytest, random
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.orm import contains_eager
from api.tests.test_utils.db_manage_test import get_database_record
from api.models.enums.models import UserType
from api.database.database_models.models import User, Address, Candidate
from api.tests.test_utils.result_tests import check_request_data_saved, check_request_with_response
from api.security.security import generate_token
from api.tests.test_utils.db_manage_test import DATA


@pytest.fixture(scope="module")
async def test_consts() -> dict:
    """Devuelve las constantes de prueba."""

    ENDPOINT = "/candidates/"

    # se obtiene el primer usuario administrador de la información de prueba
    admin = DATA["User"][UserType.ADMIN.value][0]
    # se obtiene el token de autenticación de un usuario administrador
    admin_token = generate_token(User(**admin)).access_token

    # se obtiene un candidato aleatorio de la información de prueba para eliminar y se elimina de la lista de usuarios candidatos
    delete_candidate_user = DATA["User"][UserType.CANDIDATE.value].pop(random.randrange(len(DATA["User"][UserType.CANDIDATE.value])))
    # se obtiene los datos del candidato a eliminar
    delete_candidate = next(filter(lambda c: c["user_id"] == delete_candidate_user["id"], DATA["Candidate"]))
    # se elimina el candidato de la lista de candidatos
    DATA["Candidate"].remove(delete_candidate)
    # se junta la información de usuario y candidato
    delete_candidate["user"] = delete_candidate_user

    # se obtienen todos los usuarios candidatos de la información de prueba
    all_candidates_user = DATA["User"][UserType.CANDIDATE.value]
    all_candidates = DATA["Candidate"]

    # se juntan los datos de usuario y candidato
    for cand in all_candidates:
        cand["user"] = next(filter(lambda u: u["id"] == cand["user_id"], all_candidates_user))

    # se obtiene un candidato aleatorio de la información de prueba
    candidate = random.choice(DATA["Candidate"])

    # se crea un diccionario con las constantes de prueba y se devuelve
    consts = {
        "admin_token": admin_token,
        "all_candidates": all_candidates,
        "candidate": candidate,
        "delete_candidate": delete_candidate,
        "endpoint": ENDPOINT
    }
    return consts

@pytest.mark.anyio
async def test_get_candidates(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la funcionalidad de obtener todos los candidatos a través del endpoint.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # se obtienen todos los usuarios de las constantes de prueba
    candidates = test_consts["all_candidates"]

    # se realiza la petición HTTP
    response = await client.get(ENDPOINT, headers=headers)

    # se obtiene el contenido de la respuesta
    response_json: list = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200

    # se recorren las direcciones de la respuesta y se comprueba que los datos son correctos
    for candidate in candidates:
        candidate_from_response = next(filter(lambda u: u["user"]["id"] == candidate["user_id"], response_json))
        check_request_with_response(candidate, candidate_from_response)

@pytest.mark.anyio
async def test_get_candidate(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la funcionalidad de obtener un candidato mediante el endpoint correspondiente.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # se obtiene el candidato de las constantes de prueba y su id
    candidate = test_consts["candidate"]
    candidate_id = candidate["user_id"]

    # se realiza la petición HTTP
    response = await client.get(f"{ENDPOINT}{candidate_id}/", headers=headers)

    # se obtiene el contenido de la respuesta
    response_json: list = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200
    check_request_with_response(candidate, response_json)

@pytest.mark.anyio
async def test_create_candidate(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la creación de un candidato mediante una solicitud HTTP POST al endpoint correspondiente.
    
    Args:
    - client (AsyncClient): Cliente HTTP para realizar la solicitud.
    - test_consts (dict): Constantes de prueba que contienen la URL del endpoint y el token de administrador.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # se crea un diccionario con los datos de la nueva dirección
    new_candidate = {
        "skills": [
            "java"
        ],
        "availability": [
            "FULL-TIME"
        ],
        "user": {
            "username": "raul12",
            "email": "raul12@example.com",
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
    response = await client.post(ENDPOINT, headers=headers, json=new_candidate)

    # se obtiene el contenido de la respuesta
    response_json = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 201
    check_request_with_response(new_candidate, response_json)
    # se obtiene el candidato de la base de datos y se comprueba que los datos son correctos
    candidate_db = await get_database_record(select(Candidate).where(User.username == new_candidate["user"]["username"])
                                             .join(
                                                 target=User,
                                                onclause=User.id == Candidate.user_id
                                             )
                                             .join(
                                                 target=Address,
                                                 onclause=Address.id == User.address_id
                                             )
                                             .options(contains_eager(Candidate.user).contains_eager(User.address)), only_one=True)
    check_request_data_saved(new_candidate, record=candidate_db, user_type=UserType.CANDIDATE)



@pytest.mark.anyio
async def test_update_candidate(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la creación de un candidato mediante una solicitud HTTP POST al endpoint correspondiente.
    
    Args:
    - client (AsyncClient): Cliente HTTP para realizar la solicitud.
    - test_consts (dict): Constantes de prueba que contienen la URL del endpoint y el token de administrador.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # obtenemos los datos del candidato a actualizar y su id
    candidate: dict = test_consts["candidate"]
    candidate_id = candidate["user_id"]

    # se crea un diccionario con los datos de la nueva dirección
    update_candidate = {
        "skills": [
            "java"
        ],
        "availability": [
            "FULL-TIME"
        ],
        "user": {
            "username": "actualizado",
            "email": "actualizado@example.com",
            "name": "actualizado",
            "surname": "actualizado",
            "phone_numbers": [
                613985123
            ],
            "password": "actualizadO12!",
            "address": {
                "postal_code": 16000,
                "street": "prueba",
                "city": "prueba",
                "province": "prueba"
            }
        }
    }


    # se realiza la petición HTTP
    response = await client.put(f"{ENDPOINT}{candidate_id}/", headers=headers, json=update_candidate)

    # se actualizan los datos del candidato
    candidate.update(update_candidate)

    # se obtiene el contenido de la respuesta
    response_json = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200
    check_request_with_response(candidate, response_json)
    # se obtiene el candidato de la base de datos y se comprueba que los datos son correctos
    candidate_db = await get_database_record(select(Candidate).where(User.username == update_candidate["user"]["username"])
                                             .join(
                                                 target=User,
                                                onclause=User.id == Candidate.user_id
                                             )
                                             .join(
                                                 target=Address,
                                                 onclause=Address.id == User.address_id
                                             )
                                             .options(contains_eager(Candidate.user).contains_eager(User.address)), only_one=True)
    check_request_data_saved(candidate, record=candidate_db, user_type=UserType.CANDIDATE)


@pytest.mark.anyio
async def test_partial_update_candidate(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la creación de un candidato mediante una solicitud HTTP POST al endpoint correspondiente.
    
    Args:
    - client (AsyncClient): Cliente HTTP para realizar la solicitud.
    - test_consts (dict): Constantes de prueba que contienen la URL del endpoint y el token de administrador.
    """
    
    # se obtiene la URL del endpoint
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # obtenemos los datos del candidato a actualizar y su id
    candidate: dict = test_consts["candidate"]
    candidate_id = candidate["user_id"]

    # se crea un diccionario con los datos de la nueva dirección
    update_candidate = {
        "skills": [
            "java",
            "python"
        ],
        "user": {
            "username": "new_actualizado",
            "email": "actualizado_parcial@example.com",
            "password": "actualizadO12!",
        }
    }


    # se realiza la petición HTTP
    response = await client.patch(f"{ENDPOINT}{candidate_id}/", headers=headers, json=update_candidate)

    # se actualizan los datos del candidato
    candidate.update(update_candidate)

    # se obtiene el contenido de la respuesta
    response_json = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200
    check_request_with_response(candidate, response_json)
    # se obtiene el candidato de la base de datos y se comprueba que los datos son correctos
    candidate_db = await get_database_record(select(Candidate).where(User.username == update_candidate["user"]["username"])
                                             .join(
                                                 target=User,
                                                onclause=User.id == Candidate.user_id
                                             )
                                             .join(
                                                 target=Address,
                                                 onclause=Address.id == User.address_id
                                             )
                                             .options(contains_eager(Candidate.user).contains_eager(User.address)), only_one=True)
    check_request_data_saved(candidate, record=candidate_db, user_type=UserType.CANDIDATE)

@pytest.mark.anyio
async def test_delete_candidate(client: AsyncClient, test_consts: dict):
    """
    Prueba la eliminación de un candidato mediante una solicitud HTTP DELETE al endpoint correspondiente.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """
    ENDPOINT = test_consts["endpoint"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['admin_token']}"}

    # obtenemos los datos del candidato a actualizar y su id
    candidate: dict = test_consts["delete_candidate"]
    candidate_id = candidate["user_id"]

    # se realiza la petición HTTP
    response = await client.delete(f"{ENDPOINT}{candidate_id}/", headers=headers)

    # se comprueba que la respuesta es correcta
    assert response.status_code == 204

    # se obtiene el candidato de la base de datos y se comprueba que no existe
    user = await get_database_record(select(Candidate).where(Candidate.user_id == candidate_id), only_one=True)
    assert user is None