from fastapi import APIRouter, Depends, status, BackgroundTasks
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select
from sqlalchemy.orm import joinedload
from starlette.background import BackgroundTask
from uuid import UUID
from api.database.connection import get_session
from api.utils.functions.database_utils import secure_commit, update_model
from api.security.security import TOKEN_URL, get_user_from_token, generate_token, authenticate_user
from api.security.permissions import PermissionsManager
from api.database.database_models.models import User, Adress
from api.models.base_models import Token
from api.models.read_models import ReadUserComplete
from api.models.create_models import CreateUser
from api.models.update_models import UpdateUser
from api.models.partial_update_models import PartialUpdateUser
from api.models.enums import UserType, LogLevel
from api.utils.constants.endpoints_params import LIMIT, OFFSET, USER_ID
from api.utils.constants.http_exceptions import USER_NOT_FOUND_EXCEPTION
from api.utils.functions.management_utils import print_log, create_http_exception
from api.utils.constants.info_strings import USERS_GET, USER_GET_BY_ID, USER_CREATE, USER_UPDATE, USER_DELETE, USER_LOGIN, USER_TOKEN_RENEW
from api.utils.constants.error_strings import USER_NOT_FOUND

userRoute = APIRouter(prefix="/users", tags=["users"])

@userRoute.get("/",response_model=list[ReadUserComplete], dependencies=[Depends(PermissionsManager())])
async def get_users(*, 
                    session: Annotated[AsyncSession, Depends(get_session)], 
                    logged_user: Annotated[User, Depends(get_user_from_token)],
                    background_tasks: BackgroundTasks,
                    limit: Annotated[int | None, LIMIT] = 20,
                    offset: Annotated[int | None, OFFSET]  = 0):
    """Devuelve todos los usuarios registrados en la base de datos. Solo los administradores pueden acceder a este endpoint. 
        Permite elegir la cantidad de usuarios devueltos y el offset para paginar los resultados.
    
        Args:
            session (AsyncSession): Conexion a la base de datos.
            user (User): Usuario que realiza la peticion.
            limit (int | None): Limite de usuarios devueltos.
            offset (int | None): Permite omitir un número específico de usuarios en el conjunto de resultados.
            
        Returns:
            list[ReadUser]: Lista de usuarios registrados en la base de datos."""

    # query para obtener todos los usuarios de la base de datos con un limite y un offset
    statement = select(User).limit(limit).offset(offset).options(joinedload(User.adress))
    result = await session.execute(statement)

    list_user = result.scalars().all()

    background_tasks.add_task(print_log, USERS_GET, LogLevel.INFO, user_id=logged_user.id)
    return list_user



@userRoute.get("/{user_id}/", response_model=ReadUserComplete, dependencies=[Depends(PermissionsManager())])
async def get_user(*, 
                   session:Annotated[AsyncSession, Depends(get_session)],
                   logged_user: Annotated[User, Depends(get_user_from_token)],
                   background_tasks: BackgroundTasks,
                   user_id: Annotated[UUID, USER_ID]):
    """Devuelve un usuario por su id. Solo los administradores pueden acceder a este endpoint.
    
        Args:
            session (AsyncSession): Conexion a la base de datos.
            user (User): Usuario que realiza la peticion.
            user_id (int): Id del usuario que se quiere obtener.
            
        Returns:
            ReadUser: Usuario que se quiere obtener."""

    # si el usuario que se quiere obtener es el mismo que el que realiza la peticion se devuelve el usuario que realiza la peticion
    if user_id == logged_user.id: return logged_user

    # si no se devuelve el usuario que se quiere obtener
    userResponse = await session.get(User, user_id, options=[joinedload(User.adress)])

    background_tasks.add_task(print_log, USER_GET_BY_ID, LogLevel.INFO, resource_id=user_id, user_id=logged_user.id)
    return userResponse

@userRoute.post("/admin/",response_model=ReadUserComplete, status_code=status.HTTP_201_CREATED, dependencies=[Depends(PermissionsManager())])
async def create_user(*, 
                      session:Annotated[AsyncSession, Depends(get_session)], 
                      logged_user: Annotated[User, Depends(get_user_from_token)],
                      background_tasks: BackgroundTasks,
                      new_user: CreateUser):
    """Crea un usuario administrador. Solo los administradores pueden acceder a este endpoint.
    
        Args:
            session (AsyncSession): Conexion a la base de datos.
            user (User): Usuario que realiza la peticion.
            new_user (CreateUser): Usuario administrador que se quiere crear.
            
        Returns:
            ReadUser: Usuario que se ha creado."""
        
    new_database_user = User(**new_user.model_dump(exclude=["adress"]))

    # se comprueba si la direccion ya existe en la base de datos, si existe se devuelve la direccion que ya existe
    new_database_user.adress = await Adress.get_adress(session, new_user.adress)

    new_database_user.user_type = UserType.ADMIN

    session.add(new_database_user)
    await secure_commit(session)

    background_tasks.add_task(print_log, USER_CREATE, LogLevel.INFO, resource_id=new_database_user.id, user_id=logged_user.id)
    return new_database_user


@userRoute.put("/{user_id}/", response_model=ReadUserComplete, dependencies=[Depends(PermissionsManager())])
async def update_user(*, 
                      session:Annotated[AsyncSession, Depends(get_session)],
                      logged_user: Annotated[User, Depends(get_user_from_token)],
                      background_tasks: BackgroundTasks,
                      update_user: UpdateUser, 
                      user_id: Annotated[UUID, USER_ID]):
    """Actualiza un usuario. Solo los administradores pueden acceder a este endpoint.	

        Args:
            session (AsyncSession): Conexion a la base de datos.
            user (User): Usuario que realiza la peticion.
            update_user (UpdateUser): Información de Usuario que se quiere actualizar.
            user_id (int): Id del usuario que se quiere actualizar.
            
        Returns:
            ReadUser: Usuario que se ha actualizado."""
    
    # se obtiene el usuario que se quiere actualizar si es diferente al usuario que realiza la peticion o se usa el usuario que realiza la peticion
    user_to_update: User = await session.get(User, user_id, options=[joinedload(User.adress)]) if logged_user.id != user_id else logged_user

    if user_to_update is None:
        background = BackgroundTask(print_log, USER_NOT_FOUND, LogLevel.WARNING, resource_id=user_id, user_id=logged_user.id)
        raise create_http_exception(**USER_NOT_FOUND_EXCEPTION, background_task=background)
    
    # se actualiza el usuario
    update_model(user_to_update, update_user.model_dump(exclude=["adress"]))

    # se comprueba si la direccion ya existe en la base de datos, si existe se devuelve la direccion que ya existe
    user_to_update.adress = await Adress.get_adress(session, update_user.adress)

    await secure_commit(session)
    await session.refresh(user_to_update)

    background_tasks.add_task(print_log, USER_UPDATE, LogLevel.INFO, resource_id=user_to_update.id, user_id=logged_user.id)
    return user_to_update


@userRoute.patch("/{user_id}/", response_model=ReadUserComplete, dependencies=[Depends(PermissionsManager())])
async def partial_update_user(*, 
                              session:Annotated[AsyncSession, Depends(get_session)],
                              logged_user: Annotated[User, Depends(get_user_from_token)],
                              background_tasks: BackgroundTasks,
                              update_user: PartialUpdateUser, 
                              user_id: Annotated[UUID, USER_ID]):
    """Actualiza parcialmente un usuario. Solo los administradores pueden acceder a este endpoint.	

        Args:
            session (AsyncSession): Conexion a la base de datos.
            user (User): Usuario que realiza la peticion.
            update_user (PartialUpdateUser): Información de Usuario que se quiere actualizar.
            user_id (int): Id del usuario que se quiere actualizar.
            
        Returns:
            ReadUser: Usuario que se ha actualizado."""
    
    # se obtiene el usuario que se quiere actualizar si es diferente al usuario que realiza la peticion o se usa el usuario que realiza la peticion
    user_to_update = await session.get(User, user_id, options=[joinedload(User.adress)]) if logged_user.id != user_id else logged_user
    
    if user_to_update is None:
        background = BackgroundTask(print_log, USER_NOT_FOUND, LogLevel.WARNING, resource_id=user_id, user_id=logged_user.id)
        raise create_http_exception(**USER_NOT_FOUND_EXCEPTION, background_task=background)

    # se quita los parametros que no se quieren actualizar
    new_user_data_no_unset = update_user.model_dump(exclude=["adress"],exclude_unset=True)
    
    # se actualiza el usuario
    update_model(user_to_update, new_user_data_no_unset)

    # si se quiere actualizar la direccion se comprueba si la direccion ya existe en la base de datos, si existe se devuelve la direccion que ya existe
    if update_user.adress:	
        user_to_update.adress = await Adress.get_adress(session, update_user.adress)

    await secure_commit(session)
    await session.refresh(user_to_update)

    background_tasks.add_task(print_log, USER_UPDATE, LogLevel.INFO, resource_id=user_to_update.id, user_id=logged_user.id)
    return user_to_update


@userRoute.delete("/{user_id}/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(PermissionsManager())])
async def delete_user(*, 
                      session:Annotated[AsyncSession, Depends(get_session)], 
                      logged_user: Annotated[User, Depends(get_user_from_token)],
                      background_tasks: BackgroundTasks,
                      user_id: Annotated[UUID, USER_ID]):
    """Elimina un usuario. Solo los administradores pueden acceder a este endpoint.	

        Args:
            session (AsyncSession): Conexion a la base de datos.
            user (UserDB): Usuario que realiza la peticion.
            user_id (int): Id del usuario que se quiere eliminar."""

    # se obtiene el usuario que se quiere eliminar si es diferente al usuario que realiza la peticion o se usa el usuario que realiza la peticion
    user_to_delete: User = await session.get(User, user_id) if logged_user.id != user_id else logged_user

    if user_to_delete is None:
        background = BackgroundTask(print_log, USER_NOT_FOUND, LogLevel.WARNING, resource_id=user_id, user_id=logged_user.id)
        raise create_http_exception(**USER_NOT_FOUND_EXCEPTION, background_task=background)

    await session.delete(user_to_delete)
    await secure_commit(session)

    background_tasks.add_task(print_log, USER_DELETE, LogLevel.INFO, resource_id=user_to_delete.id, user_id=logged_user.id)



@userRoute.post(f"/{TOKEN_URL}/",response_model=Token)
async def login_user(*, 
                     session: Annotated[AsyncSession, Depends(get_session)],
                     background_tasks: BackgroundTasks,
                     form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
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



@userRoute.post(f"/{TOKEN_URL}/renew/", response_model=Token)
async def renew_token(*, 
                      session: Annotated[AsyncSession, Depends(get_session)],
                      background_tasks: BackgroundTasks,
                      logged_user: Annotated[User, Depends(get_user_from_token)]):
    """Renueva el token de autenticación del usuario. Si el usuario no esta autenticado devuelve un error.
    
        Args:
            session (Session): Conexion a la base de datos.
            user (UserDB): Usuario que realiza la peticion.
            
        Returns:
            Token: Token de autenticación."""

    # se crea el nuevo token de autenticacion
    newToken: Token = generate_token(logged_user)

    background_tasks.add_task(print_log, USER_TOKEN_RENEW, LogLevel.INFO, user_id=logged_user.id)

    return newToken
    

    






