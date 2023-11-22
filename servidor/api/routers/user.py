from fastapi import APIRouter, Depends, status, BackgroundTasks
from typing import Annotated
from uuid import UUID
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from api.database.connection import get_session
from api.utils.functions.database_utils import secure_commit, update_model, get_database_records, get_user_by_id
from api.security.security import TOKEN_URL, get_user_from_token, generate_token, authenticate_user
from api.security.permissions import PermissionsManager
from api.database.database_models.models import User, Adress
from api.models.base_models import Token
from api.models.read_models import ReadUserComplete
from api.models.create_models import CreateUser
from api.models.update_models import UpdateUser
from api.models.partial_update_models import PartialUpdateUser
from api.models.enums.models import UserType, LogLevel
from api.utils.constants.endpoints_params import LIMIT, OFFSET, USER_ID, DEFAULT_LIMIT, DEFAULT_OFFSET
from api.utils.functions.management_utils import print_log, endpoint_request_log
from api.utils.constants.info_strings import USER_LOGIN, USER_TOKEN_RENEW

userRoute = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(PermissionsManager.is_admin), Depends(endpoint_request_log)])
loginRoute = APIRouter(tags=["login", "users"])

@userRoute.get("/",response_model=list[ReadUserComplete])
async def get_users(*, 
                    session: Annotated[AsyncSession, Depends(get_session)], 
                    limit: Annotated[int | None, LIMIT] = DEFAULT_LIMIT,
                    offset: Annotated[int | None, OFFSET] = DEFAULT_OFFSET) -> list[User]:
    """Devuelve todos los usuarios registrados en la base de datos. Solo los administradores pueden acceder a este endpoint. 
        Permite elegir la cantidad de usuarios devueltos y el offset para paginar los resultados.
    
        Args:
            session (AsyncSession): Conexion a la base de datos.
            limit (int | None): Limite de usuarios devueltos.
            offset (int | None): Permite omitir un número específico de usuarios en el conjunto de resultados.
            
        Returns:
            list[ReadUser]: Lista de usuarios registrados en la base de datos."""

    # se obtienen los usuarios
    list_user: list[User] = await get_database_records(session, User, options=joinedload(User.adress), limit=limit, offset=offset)

    return list_user



@userRoute.get("/{user_id}/", response_model=ReadUserComplete)
async def get_user(*, 
                   session:Annotated[AsyncSession, Depends(get_session)],
                   logged_user: Annotated[User, Depends(get_user_from_token)],
                   user_id: Annotated[UUID, USER_ID]) -> User:
    """Devuelve un usuario por su id. Solo los administradores pueden acceder a este endpoint.
    
        Args:
            session (AsyncSession): Conexion a la base de datos.
            logged_user (User): Usuario que realiza la peticion.
            user_id (int): Id del usuario que se quiere obtener.
            
        Returns:
            ReadUser: Usuario que se quiere obtener."""
    
    user: User = await get_user_by_id(session, logged_user, User, user_id, extra_fields=joinedload(User.adress))

    return user

@userRoute.post("/admin/",response_model=ReadUserComplete, status_code=status.HTTP_201_CREATED)
async def create_user(*, 
                      session:Annotated[AsyncSession, Depends(get_session)], 
                      new_user: CreateUser) -> User:
    """Crea un usuario administrador. Solo los administradores pueden acceder a este endpoint.
    
        Args:
            session (AsyncSession): Conexion a la base de datos.
            new_user (CreateUser): Usuario administrador que se quiere crear.
            
        Returns:
            ReadUser: Usuario que se ha creado."""
        
    new_database_user = User(**new_user.model_dump(exclude=["adress"]))

    # se comprueba si la direccion ya existe en la base de datos, si existe se devuelve la direccion que ya existe
    new_database_user.adress = await Adress.get_adress(session, new_user.adress)

    new_database_user.user_type = UserType.ADMIN

    session.add(new_database_user)
    await secure_commit(session)

    return new_database_user


@userRoute.put("/{user_id}/", response_model=ReadUserComplete)
async def update_user(*, 
                      session:Annotated[AsyncSession, Depends(get_session)],
                      logged_user: Annotated[User, Depends(get_user_from_token)],
                      update_user: UpdateUser, 
                      user_id: Annotated[UUID, USER_ID]) -> User:
    """Actualiza un usuario. Solo los administradores pueden acceder a este endpoint.	

        Args:
            session (AsyncSession): Conexion a la base de datos.
            logged_user (User): Usuario que realiza la peticion.
            update_user (UpdateUser): Información de Usuario que se quiere actualizar.
            user_id (int): Id del usuario que se quiere actualizar.
            
        Returns:
            ReadUser: Usuario que se ha actualizado."""
    
    user_to_update = await get_user_by_id(session, logged_user, User, user_id, extra_fields=joinedload(User.adress))
    
    # se actualiza el usuario
    update_model(user_to_update, update_user.model_dump(exclude=["adress"]))

    # se comprueba si la direccion ya existe en la base de datos, si existe se devuelve la direccion que ya existe
    user_to_update.adress = await Adress.get_adress(session, update_user.adress)

    await secure_commit(session)
    await session.refresh(user_to_update)

    return user_to_update


@userRoute.patch("/{user_id}/", response_model=ReadUserComplete)
async def partial_update_user(*, 
                              session:Annotated[AsyncSession, Depends(get_session)],
                              logged_user: Annotated[User, Depends(get_user_from_token)],
                              update_user: PartialUpdateUser, 
                              user_id: Annotated[UUID, USER_ID]) -> User:
    """Actualiza parcialmente un usuario. Solo los administradores pueden acceder a este endpoint.	

        Args:
            session (AsyncSession): Conexion a la base de datos.
            logged_user (User): Usuario que realiza la peticion.
            update_user (PartialUpdateUser): Información de Usuario que se quiere actualizar.
            user_id (int): Id del usuario que se quiere actualizar.
            
        Returns:
            ReadUser: Usuario que se ha actualizado."""
    
    user_to_update = await get_user_by_id(session, logged_user, User, user_id, extra_fields=joinedload(User.adress))
    
    # se quita los parametros que no se quieren actualizar
    new_user_data_no_unset = update_user.model_dump(exclude=["adress"],exclude_unset=True)
    
    # se actualiza el usuario
    update_model(user_to_update, new_user_data_no_unset)

    # si se quiere actualizar la direccion se comprueba si la direccion ya existe en la base de datos, si existe se devuelve la direccion que ya existe
    if update_user.adress:	
        user_to_update.adress = await Adress.get_adress(session, update_user.adress)

    await secure_commit(session)
    await session.refresh(user_to_update)

    return user_to_update


@userRoute.delete("/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(*, 
                      session:Annotated[AsyncSession, Depends(get_session)], 
                      logged_user: Annotated[User, Depends(get_user_from_token)],
                      user_id: Annotated[UUID, USER_ID]) -> None:
    """Elimina un usuario. Solo los administradores pueden acceder a este endpoint.	

        Args:
            session (AsyncSession): Conexion a la base de datos.
            logged_user (UserDB): Usuario que realiza la peticion.
            user_id (int): Id del usuario que se quiere eliminar."""
    
    user_to_delete = await get_user_by_id(session, logged_user, User, user_id)

    await session.delete(user_to_delete)
    await secure_commit(session)

@loginRoute.post(f"/{TOKEN_URL}/",response_model=Token)
async def login_user(*, 
                     session: Annotated[AsyncSession, Depends(get_session)],
                     background_tasks: BackgroundTasks,
                     form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """Creación de token de autenticación para el usuario. Si el usuario no existe o la contraseña es incorrecta devuelve un error.
        
        Args:
            session (Session): Conexion a la base de datos.
            form_data (OAuth2PasswordRequestForm): Datos del formulario de login.
            
        Returns:
            Token: Token de autenticación."""

    # se comprueba si el usuario existe y si la contraseña es correcta
    user: User = await authenticate_user(session=session, username=form_data.username, password=form_data.password)
    
    # se crea el token de autenticacion
    token: Token = generate_token(user)

    background_tasks.add_task(print_log, USER_LOGIN, LogLevel.INFO, user_id=user.id)

    return token



@loginRoute.post(f"/{TOKEN_URL}/renew/", response_model=Token)
async def renew_token(*, 
                      background_tasks: BackgroundTasks,
                      logged_user: Annotated[User, Depends(get_user_from_token)]) -> Token:
    """Renueva el token de autenticación del usuario. Si el usuario no esta autenticado devuelve un error.
    
        Args:
            logged_user (UserDB): Usuario que realiza la peticion.
            
        Returns:
            Token: Token de autenticación."""

    # se crea el nuevo token de autenticacion
    newToken: Token = generate_token(logged_user)

    background_tasks.add_task(print_log, USER_TOKEN_RENEW, LogLevel.INFO, user_id=logged_user.id)

    return newToken
    

    






