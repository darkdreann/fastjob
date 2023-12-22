import re, pytest, random
from httpx import AsyncClient
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from api.tests.test_utils.db_manage_test import get_database_record
from api.models.enums.models import UserType
from api.utils.constants.http_exceptions import RESOURCE_NOT_FOUND_EXCEPTION, INTEGRATION_EXCEPTION, FORBIDDEN_EXCEPTION, CREDENTIALS_EXCEPTION
from api.database.database_models.models import User
from api.database.database_models.metadata.constraint_name import UserConstraint
from api.tests.test_utils.result_tests import check_request_data_saved, check_request_with_response
from api.security.security import generate_token
from api.models.enums.models import UserType
from api.tests.test_utils.db_manage_test import DATA

@pytest.fixture(scope="module")
async def test_consts() -> dict:
    """Devuelve las constantes de prueba."""

    LOGIN_ENDPOINT = "/login/"
    ENDPOINT = "/users/"

    # se obtiene un usuario admin aleatorio de la información de prueba para eliminarlo en el test y se elimina de la información de prueba
    delete_user = DATA["User"][UserType.ADMIN.value].pop(random.randrange(len(DATA["User"][UserType.ADMIN.value])))

    # se obtiene el primer usuario administrador de la información de prueba
    admin = random.choice(DATA["User"][UserType.ADMIN.value])
    # se obtiene el token de autenticación de un usuario administrador
    admin_token = generate_token(User(**admin)).access_token

    # se obtiene un usuario candidato aleatorio de la información de prueba
    candidate = random.choice(DATA["User"][UserType.CANDIDATE.value])
    # se obtiene el token de autenticación de un usuario normal
    normal_user_token = generate_token(User(**candidate)).access_token

    # se obtiene un administrador aleatorio de la información de prueba
    user_update = random.choice(DATA["User"][UserType.ADMIN.value])

    # se obtiene la primera dirección de la información de prueba
    address = random.choice(DATA["Address"])

    # se obtienen todos los administradores de la información de prueba
    all_admins = DATA["User"][UserType.ADMIN.value]

    # se crea un diccionario con las constantes de prueba y se devuelve
    consts = {
        "JWT_REGEX": r"^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$",
        "ADMIN_TOKEN": admin_token,
        "NORMAL_USER_TOKEN": normal_user_token,
        "DELETE_USER": delete_user,
        "user_update": user_update,
        "ADMIN": admin,
        "ADDRESS": address,
        "all_admins": all_admins,
        "LOGIN_ENDPOINT": LOGIN_ENDPOINT,
        "ENDPOINT": ENDPOINT
    }
    return consts


@pytest.mark.anyio
async def test_login_admin(client: AsyncClient, test_consts: dict) -> None:
    """
    Prueba la creacion de un token de autenticacion para un usuario administrador existente.

    Args:
    - client (AsyncClient): Cliente asincrónico para realizar las peticiones HTTP.
    - test_consts (dict): Constantes de prueba que contienen el usuario administrador.
    """
    ENDPOINT = test_consts["LOGIN_ENDPOINT"]

    # se obtiene el usuario administrador de las constantes de prueba
    admin: User = test_consts["ADMIN"]
    # se crea un diccionario con los datos de autenticación
    data={"username": admin["username"], "password": admin["password"]}

    # se realiza la petición HTTP
    response = await client.post(ENDPOINT, data=data)

    # se obtiene el contenido de la respuesta
    json = response.json()

    # se comprueba que la respuesta es correctat
    assert response.status_code == 200
    assert json["token_type"] == "bearer"
    assert re.match(test_consts["JWT_REGEX"], json["access_token"])



@pytest.mark.anyio
async def test_create_user_admin(client: AsyncClient, test_consts: dict):
    """
    Prueba la creacion de un usuario admin.

    Esta función prueba la creación de un usuario administrador en el sistema.
    Se envía una solicitud HTTP POST al endpoint '/users/admin/' con los datos del nuevo usuario.
    Se espera que la respuesta tenga un código de estado 201 (Created).
    Además, se verifica que los datos enviados coincidan con los datos almacenados en la base de datos.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las solicitudes.
    - test_consts (dict): Constantes de prueba.
    """

    ENDPOINT = test_consts["ENDPOINT"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['ADMIN_TOKEN']}"}

    # se crea un diccionario con los datos del nuevo usuario
    new_user_data = {
        "username": "new_admin",
        "email": "new_admin@gmail.com",
        "name": "José",
        "surname": "López",
        "phone_numbers": [
            645143984,
            698128745
        ],
        "password": "Admin1234.",
        "address": {
            "postal_code": 19999,
            "street": "calle falsa",
            "city": "vigo",
            "province": "pontevedra"
        }
    }

    # se realiza la petición HTTP
    response = await client.post(f"{ENDPOINT}admin/", headers=headers, json=new_user_data)

    # se obtiene el contenido de la respuesta
    user_response = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 201
    check_request_with_response(new_user_data, user_response)
    # se obtiene el usuario de la base de datos y se comprueba que los datos son correctos
    database_user = await get_database_record(select(User).where(User.username == new_user_data["username"]).options(joinedload(User.address)), only_one=True)
    check_request_data_saved(new_user_data, record=database_user, user_type=UserType.ADMIN)

@pytest.mark.anyio
async def test_get_users(client: AsyncClient, test_consts: dict):
    """
    Prueba la función de obtener usuarios.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """

    ENDPOINT = test_consts["ENDPOINT"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['ADMIN_TOKEN']}"}

    # se obtienen todos los usuarios de las constantes de prueba
    users = test_consts["all_admins"]

    # se realiza la petición HTTP
    response = await client.get(ENDPOINT, headers=headers)

    # se obtiene el contenido de la respuesta
    users_response: list = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200
    
    # se recorren los usuarios de la respuesta y se comprueba que los datos son correctos
    for user_test in users:
        user_response = next(filter(lambda u: u["id"] == user_test["id"], users_response))
        check_request_with_response(user_test, user_response)

@pytest.mark.anyio
async def test_get_user(client: AsyncClient, test_consts: dict):
    """
    Prueba para obtener un usuario concreto.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """

    ENDPOINT = test_consts["ENDPOINT"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['ADMIN_TOKEN']}"}

    # se obtiene el usuario candidato de las constantes de prueba
    user: dict = test_consts["user_update"]
    # se obtiene el id del usuario
    user_id = user["id"]

    # se realiza la petición HTTP
    response = await client.get(f"{ENDPOINT}{user_id}/", headers=headers)

    # se obtiene el contenido de la respuesta
    user_response = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200
    check_request_with_response(user, user_response)

@pytest.mark.anyio
async def test_renew_token(client: AsyncClient, test_consts: dict):
    """
    Prueba la renovacion de un token de autenticacion.

    Esta función prueba la renovación de un token de autenticación.
    Se envía una solicitud POST al endpoint "/login/renew/" con el token de autenticación del administrador.
    Se espera que la respuesta tenga un código de estado 200 y que el tipo de token sea "bearer".
    Además, se verifica que el token de acceso cumpla con la expresión regular definida en test_consts.

    Args:
    - client (AsyncClient): Cliente HTTP asincrónico para realizar las solicitudes.
    - test_consts (dict): Diccionario con constantes de prueba.
    """

    ENDPOINT = test_consts["LOGIN_ENDPOINT"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['ADMIN_TOKEN']}"}

    # se realiza la petición HTTP
    response = await client.post(f"{ENDPOINT}renew/", headers=headers)

    # se obtiene el contenido de la respuesta
    json = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200
    assert json["token_type"] == "bearer"
    assert re.match(test_consts["JWT_REGEX"], json["access_token"])

@pytest.mark.anyio
async def test_update_user(client: AsyncClient, test_consts: dict):
    """
    Prueba de actualizacion de un usuario.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """

    ENDPOINT = test_consts["ENDPOINT"]

    headers={"Authorization": f"Bearer {test_consts['ADMIN_TOKEN']}"}

    # se obtiene el usuario candidato de las constantes de prueba
    user: dict = test_consts["user_update"]

    # se obtiene la dirección del usuario
    address: dict = test_consts["ADDRESS"]
    # se obtiene el id del usuario
    user_id = user["id"]

    # se actualizan los datos del usuario
    user["username"] = "juan40"
    user["email"] = "juan40@gmail.com"
    user["name"] = "Juan"
    user["password"] = "Juan4090*"
    user["address"] = address
    user["address_id"] = address["id"]
    
    # se realiza la petición HTTP
    response = await client.put(f"{ENDPOINT}{user_id}/", headers=headers, json=user)
    
    # se obtiene el contenido de la respuesta
    user_response = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200
    check_request_with_response(user, user_response)

    # se obtiene el usuario de la base de datos y se comprueba que los datos son correctos
    database_user = await get_database_record(select(User).where(User.username == user["username"]).options(joinedload(User.address)), only_one=True)
    check_request_data_saved(user, record=database_user, user_type=user["user_type"])


@pytest.mark.anyio
async def test_partial_update_user(client: AsyncClient, test_consts: dict):
    """
    Prueba la actualización parcial de un usuario.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """

    ENDPOINT = test_consts["ENDPOINT"]
    
    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['ADMIN_TOKEN']}"}

    # se obtiene el usuario candidato de las constantes de prueba
    user: dict = test_consts["user_update"]
    # se obtiene el id del usuario
    user_id = user["id"]

    # se actualizan los datos del usuario
    updated_user_data = {
        "username": "new_juan",
        "email": "new_juan@example.com",
        "surname": "new"
    }

    # se actualiza el usuario
    user.update(updated_user_data)

    # se realiza la petición HTTP
    response = await client.patch(f"{ENDPOINT}{user_id}/", headers=headers, json=updated_user_data)

    # se obtiene el contenido de la respuesta
    user_response = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == 200
    check_request_with_response(user, user_response)

    # se obtiene el usuario de la base de datos y se comprueba que los datos son correctos
    database_user = await get_database_record(select(User).where(User.username == user["username"]).options(joinedload(User.address)), only_one=True)
    check_request_data_saved(user, record=database_user, user_type=user["user_type"])


    

@pytest.mark.anyio
async def test_delete_user(client: AsyncClient, test_consts: dict):
    """
    Prueba la funcionalidad de eliminar un usuario.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """

    ENDPOINT = test_consts["ENDPOINT"]

    # se crea un diccionario con los datos de autenticación
    headers={"Authorization": f"Bearer {test_consts['ADMIN_TOKEN']}"}

    # se obtiene el usuario candidato de las constantes de prueba
    user: dict = test_consts['DELETE_USER']
    # se obtiene el id del usuario
    user_id = user["id"]

    # se realiza la petición HTTP
    response = await client.delete(f"{ENDPOINT}{user_id}/", headers=headers)

    # se comprueba que la respuesta es correcta
    assert response.status_code == 204

    # se obtiene el usuario de la base de datos y se comprueba que no existe
    user = await get_database_record(select(User).where(User.id == user_id), only_one=True)
    assert user is None

@pytest.mark.anyio
async def test_create_user_unauthorized(client: AsyncClient, test_consts: dict):
    """
    El usuario no está autenticado y trata de crear un usuario.

    Args:
    - client (AsyncClient): El cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """

    ENDPOINT = test_consts["ENDPOINT"]

    # se realiza la petición HTTP
    response = await client.post(f"{ENDPOINT}admin/", json={})

    # se obtiene el contenido de la respuesta
    response_json = response.json()

    # se comprueba que la respuesta es correcta  
    assert response.status_code == 401
    assert response_json["detail"] == CREDENTIALS_EXCEPTION["detail"]

@pytest.mark.anyio
async def test_create_user_forbidden(client: AsyncClient, test_consts: dict):
    """
    Prueba la creación de un usuario con un token de usuario normal, lo cual debería devolver un error de acceso denegado.

    Args:
    - client (AsyncClient): El cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """

    ENDPOINT = test_consts["ENDPOINT"]

    # se crea un diccionario con los datos de autenticación
    headers = {"Authorization": f"Bearer {test_consts['NORMAL_USER_TOKEN']}"}

    # se realiza la petición HTTP
    response = await client.post(f"{ENDPOINT}admin/", headers=headers, json={})

    # se obtiene el contenido de la respuesta
    response_json = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == FORBIDDEN_EXCEPTION["status_code"]
    assert response_json["detail"] == FORBIDDEN_EXCEPTION["detail"]


@pytest.mark.anyio
async def test_create_user_duplicate_username(client: AsyncClient, test_consts: dict):
    """
    Prueba la creación de un usuario con un nombre de usuario duplicado.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """

    ENDPOINT = test_consts["ENDPOINT"]

    # se crea un diccionario con los datos de autenticación
    headers = {"Authorization": f"Bearer {test_consts['ADMIN_TOKEN']}"}

    # se hace una copia de los datos de un usuario candidato
    new_user_data = test_consts["user_update"].copy()

    # se cambia el email del usuario para que de error de nombre de usuario duplicado
    new_user_data["email"] = "new_email1234@gmail.com"

    # se realiza la petición HTTP
    response = await client.post(f"{ENDPOINT}admin/", headers=headers, json=new_user_data)

    # se obtiene el contenido de la respuesta
    response_json = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == INTEGRATION_EXCEPTION[UserConstraint.DUPLICATE_USERNAME]["status_code"]
    assert response_json["detail"] == INTEGRATION_EXCEPTION[UserConstraint.DUPLICATE_USERNAME]["detail"]

@pytest.mark.anyio
async def test_create_user_duplicate_email(client: AsyncClient, test_consts: dict):
    """
    Prueba la creación de un usuario con un correo electrónico duplicado.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """

    ENDPOINT = test_consts["ENDPOINT"]

    # se crea un diccionario con los datos de autenticación
    headers = {"Authorization": f"Bearer {test_consts['ADMIN_TOKEN']}"}

    # se hace una copia de los datos de un usuario candidato
    new_user_data = test_consts["user_update"].copy()
    # se cambia el nombre de usuario del usuario para que de error de email duplicado
    new_user_data["username"] = "new_username9921"

    # se realiza la petición HTTP
    response = await client.post(f"{ENDPOINT}admin/", headers=headers, json=new_user_data)

    # se obtiene el contenido de la respuesta
    response_json = response.json()
    
    # se comprueba que la respuesta es correcta
    assert response.status_code == INTEGRATION_EXCEPTION[UserConstraint.DUPLICATE_EMAIL]["status_code"]
    assert response_json["detail"] == INTEGRATION_EXCEPTION[UserConstraint.DUPLICATE_EMAIL]["detail"]


@pytest.mark.anyio
async def test_update_user_not_found(client: AsyncClient, test_consts: dict):
    """
    Prueba la actualización de un usuario que no se encuentra en la base de datos.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """

    ENDPOINT = test_consts["ENDPOINT"]

    # se crea un diccionario con los datos de autenticación
    headers = {"Authorization": f"Bearer {test_consts['ADMIN_TOKEN']}"}

    # creamos un id aleatorio
    fake_id = uuid4()

    # se realiza la petición HTTP
    response = await client.patch(f"{ENDPOINT}{fake_id}/", headers=headers, json={})

    # se obtiene el contenido de la respuesta
    response_json = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == RESOURCE_NOT_FOUND_EXCEPTION["status_code"]
    assert response_json["detail"] == RESOURCE_NOT_FOUND_EXCEPTION["detail"]

@pytest.mark.anyio
async def test_delete_user_not_found(client: AsyncClient, test_consts: dict):
    """
    Prueba la eliminación de un usuario que no se encuentra en la base de datos.

    Args:
    - client (AsyncClient): Cliente HTTP para realizar las peticiones.
    - test_consts (dict): Constantes de prueba.
    """

    ENDPOINT = test_consts["ENDPOINT"]

    # se crea un diccionario con los datos de autenticación
    headers = {"Authorization": f"Bearer {test_consts['ADMIN_TOKEN']}"}

    # creamos un id aleatorio
    fake_id = uuid4()

    # se realiza la petición HTTP
    response = await client.delete(f"{ENDPOINT}{fake_id}/", headers=headers)

    # se obtiene el contenido de la respuesta
    response_json = response.json()

    # se comprueba que la respuesta es correcta
    assert response.status_code == RESOURCE_NOT_FOUND_EXCEPTION["status_code"]
    assert response_json["detail"] == RESOURCE_NOT_FOUND_EXCEPTION["detail"]
