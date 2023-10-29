import re, pytest, random
from httpx import AsyncClient
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from api.tests.test_utils.db_manage_test import get_database_record
from api.models.enums import UserType
from api.utils.constants.http_exceptions import USER_NOT_FOUND_EXCEPTION, INTEGRATION_EXCEPTION, FORBIDDEN_EXCEPTION
from api.database.database_models.models import User
from api.database.database_models.metadata.constraint_name import UserConstraint
from api.tests.test_utils.result_tests import check_request_data_saved, check_request_with_response
from api.security.security import generate_token
from api.models.enums import UserType
from api.tests.test_utils.db_manage_test import DATA

@pytest.fixture(scope="module")
async def test_consts():
    """Devuelve las constantes de prueba."""	

    adress = DATA["Adress"][0]
    admin = DATA["User"][UserType.ADMIN.value][0]
    delete_user = DATA["User"][UserType.CANDIDATE.value].pop(random.randrange(len(DATA["User"][UserType.CANDIDATE.value])))
    candidate = random.choice(DATA["User"][UserType.CANDIDATE.value])
    admin_token = generate_token(User(**admin)).access_token
    normal_user_token = generate_token(User(**candidate)).access_token
    
    all_users = DATA["User"][UserType.CANDIDATE.value] + DATA["User"][UserType.ADMIN.value] + DATA["User"][UserType.COMPANY.value]

    consts = {
        "JWT_REGEX": r"^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$",
        "ADMIN_TOKEN": admin_token,
        "NORMAL_USER_TOKEN": normal_user_token,
        "DELETE_USER": delete_user,
        "CANDIDATE": candidate,
        "ADMIN": admin,
        "ADRESS": adress,
        "ALL_USERS": all_users
    }
    
    return consts


@pytest.mark.anyio
async def test_login_admin(client: AsyncClient, test_consts: dict):
    """Prueba la creacion de un token de autenticacion para un usuario administrador existente."""

    admin: User = test_consts["ADMIN"]
    data={"username": admin["username"], "password": admin["password"]}

    response = await client.post(f"/users/login/", data=data)
    json = response.json()

    assert response.status_code == 200
    assert json["token_type"] == "bearer"
    assert re.match(test_consts["JWT_REGEX"], json["access_token"])


@pytest.mark.anyio
async def test_login_normal_user(client: AsyncClient, test_consts: dict):
    """Prueba la creacion de un token de autenticacion para un usuario normal existente."""
    
    candidate: User = test_consts["CANDIDATE"]
    data={"username": candidate["username"], "password": candidate["password"]}

    response = await client.post(f"/users/login/", data=data)
    json = response.json()

    assert response.status_code == 200
    assert json["token_type"] == "bearer"
    assert re.match(test_consts["JWT_REGEX"], json["access_token"])

@pytest.mark.anyio
async def test_renew_token(client: AsyncClient, test_consts: dict):
    """Prueba la renovacion de un token de autenticacion."""

    headers={"Authorization": f"Bearer {test_consts['ADMIN_TOKEN']}"}

    response = await client.post("/users/login/renew/", headers=headers)

    json = response.json()
    assert response.status_code == 200
    assert json["token_type"] == "bearer"
    assert re.match(test_consts["JWT_REGEX"], json["access_token"])

@pytest.mark.anyio
async def test_create_user_admin(client: AsyncClient, test_consts: dict):
    """Prueba la creacion de un usuario admin."""

    headers={"Authorization": f"Bearer {test_consts['ADMIN_TOKEN']}"}

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
        "adress": {
            "postal_code": 19999,
            "street": "calle falsa",
            "city": "vigo",
            "province": "pontevedra"
        }
    }

    response = await client.post("/users/admin/", headers=headers, json=new_user_data)

    user_response = response.json()
    assert response.status_code == 201

    check_request_with_response(new_user_data, user_response)
    database_user = await get_database_record(select(User).where(User.username == new_user_data["username"]).options(joinedload(User.adress)), only_one=True)
    await check_request_data_saved(new_user_data, data=database_user, user_type=UserType.ADMIN)


@pytest.mark.anyio
async def test_get_user(client: AsyncClient, test_consts: dict):
    """Prueba para obtener un usuario concreto."""

    headers={"Authorization": f"Bearer {test_consts['ADMIN_TOKEN']}"}

    user: dict = test_consts["CANDIDATE"]
    user_id = user["id"]

    response = await client.get(f"/users/{user_id}/", headers=headers)
    user_response = response.json()

    assert response.status_code == 200
    check_request_with_response(user, user_response)


@pytest.mark.anyio
async def test_update_user(client: AsyncClient, test_consts: dict):
    """Prueba de actualizacion de un usuario."""

    headers={"Authorization": f"Bearer {test_consts['ADMIN_TOKEN']}"}

    user: dict = test_consts["CANDIDATE"]
    adress: dict = test_consts["ADRESS"]
    user_id = user["id"]

    user["username"] = "juan40"
    user["email"] = "juan40@gmail.com"
    user["name"] = "Juan"
    user["password"] = "Juan4090*"

    user["adress"] = adress
    


    response = await client.put(f"/users/{user_id}/", headers=headers, json=user)
    
    user_response = response.json()

    assert response.status_code == 200
    check_request_with_response(user, user_response)
    database_user = await get_database_record(select(User).where(User.username == user["username"]).options(joinedload(User.adress)), only_one=True)
    await check_request_data_saved(user, data=database_user, user_type=user["user_type"])


@pytest.mark.anyio
async def test_partial_update_user(client: AsyncClient, test_consts: dict):
    """Prueba de actualizacion parcial de un usuario."""
    
    headers={"Authorization": f"Bearer {test_consts['ADMIN_TOKEN']}"}

    user: dict = test_consts["CANDIDATE"]
    user_id = user["id"]

    updated_user_data = {
        "username": "new_juan",
        "email": "new_juan@example.com",
        "surname": "new"
    }

    user.update(updated_user_data)

    response = await client.patch(f"/users/{user_id}/", headers=headers, json=updated_user_data)

    user_response = response.json()

    assert response.status_code == 200
    check_request_with_response(user, user_response)
    database_user = await get_database_record(select(User).where(User.username == user["username"]).options(joinedload(User.adress)), only_one=True)
    await check_request_data_saved(user, data=database_user, user_type=user["user_type"])

@pytest.mark.anyio
async def test_get_users(client: AsyncClient, test_consts: dict):
    """Prueba para obtener una lista de usuarios."""

    headers={"Authorization": f"Bearer {test_consts['ADMIN_TOKEN']}"}

    users = test_consts["ALL_USERS"]

    response = await client.get("/users/", headers=headers)

    users_response: list = response.json()

    assert response.status_code == 200

    for user_test in users:

        user_response = next(filter(lambda u: u["id"] == user_test["id"], users_response))
        check_request_with_response(user_test, user_response)
    

@pytest.mark.anyio
async def test_delete_user(client: AsyncClient, test_consts: dict):

    """Prueba para eliminar un usuario."""

    headers={"Authorization": f"Bearer {test_consts['ADMIN_TOKEN']}"}

    user: dict = test_consts['DELETE_USER']
    user_id = user["id"]

    response = await client.delete(f"/users/{user_id}/", headers=headers)

    assert response.status_code == 204

    user = await get_database_record(select(User).where(User.id == user_id), only_one=True)

    assert user is None

@pytest.mark.anyio
async def test_create_user_unauthorized(client: AsyncClient, test_consts: dict):
    """El usuario no está autenticado y trata de crear un usuario. Se espera un error 401 (Unauthorized)."""

    response = await client.post("/users/admin/", json={})

    response_json = response.json()
    
    assert response.status_code == 401
    assert response_json["detail"] == "Not authenticated"

@pytest.mark.anyio
async def test_create_user_forbidden(client: AsyncClient, test_consts: dict):
    """El usuario autenticado no tiene permisos para crear un usuario y trata de hacerlo. Se espera un error 403 (Forbidden)."""

    headers = {"Authorization": f"Bearer {test_consts['NORMAL_USER_TOKEN']}"}

    response = await client.post("/users/admin/", headers=headers, json={})

    response_json = response.json()

    assert response.status_code == FORBIDDEN_EXCEPTION["status_code"]
    assert response_json["detail"] == FORBIDDEN_EXCEPTION["detail"]


@pytest.mark.anyio
async def test_create_user_duplicate_username(client: AsyncClient, test_consts: dict):
    """El usuario autenticado intenta crear un usuario con un nombre de usuario que ya existe. Se espera un error 400 (Bad Request)."""

    headers = {"Authorization": f"Bearer {test_consts['ADMIN_TOKEN']}"}

    new_user_data = test_consts["CANDIDATE"].copy()

    new_user_data["email"] = "new_email1234@gmail.com"

    response = await client.post("/users/admin/", headers=headers, json=new_user_data)

    response_json = response.json()


    assert response.status_code == INTEGRATION_EXCEPTION[UserConstraint.DUPLICATE_USERNAME]["status_code"]
    assert response_json["detail"] == INTEGRATION_EXCEPTION[UserConstraint.DUPLICATE_USERNAME]["detail"]

@pytest.mark.anyio
async def test_create_user_duplicate_email(client: AsyncClient, test_consts: dict):
    """El usuario autenticado intenta crear un usuario con un correo electrónico que ya existe. Se espera un error 400 (Bad Request)."""

    headers = {"Authorization": f"Bearer {test_consts['ADMIN_TOKEN']}"}

    new_user_data = test_consts["CANDIDATE"].copy()
    new_user_data["username"] = "new_username9921"

    response = await client.post("/users/admin/", headers=headers, json=new_user_data)

    response_json = response.json()
    
    assert response.status_code == INTEGRATION_EXCEPTION[UserConstraint.DUPLICATE_EMAIL]["status_code"]
    assert response_json["detail"] == INTEGRATION_EXCEPTION[UserConstraint.DUPLICATE_EMAIL]["detail"]


@pytest.mark.anyio
async def test_update_user_not_found(client: AsyncClient, test_consts: dict):
    """El usuario autenticado intenta actualizar un usuario que no existe. Se espera un error 404 (Not Found)."""

    headers = {"Authorization": f"Bearer {test_consts['ADMIN_TOKEN']}"}

    fake_id = uuid4()

    response = await client.patch(f"/users/{fake_id}/", headers=headers, json={})

    response_json = response.json()

    assert response.status_code == USER_NOT_FOUND_EXCEPTION["status_code"]
    assert response_json["detail"] == USER_NOT_FOUND_EXCEPTION["detail"]

@pytest.mark.anyio
async def test_delete_user_not_found(client: AsyncClient, test_consts: dict):
    """El usuario autenticado intenta eliminar un usuario que no existe. Se espera un error 404 (Not Found)."""

    headers = {"Authorization": f"Bearer {test_consts['ADMIN_TOKEN']}"}

    fake_id = uuid4()

    response = await client.delete(f"/users/{fake_id}/", headers=headers)

    response_json = response.json()

    assert response.status_code == USER_NOT_FOUND_EXCEPTION["status_code"]
    assert response_json["detail"] == USER_NOT_FOUND_EXCEPTION["detail"]
