from re import match
from typing import Annotated
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from starlette.background import BackgroundTask
from datetime import datetime, timedelta
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select
from api.database.connection import get_session
from api.models.base_models import Token
from api.utils.constants.http_exceptions import CREDENTIALS_EXCEPTION
from api.database.database_models.models import User
from api.models.enums.models import LogLevel
from api.utils.functions.management_utils import print_log
from api.utils.exceptions import HTTPExceptionWithBackgroundTask
from api.utils.constants.error_strings import PERMISSION_USER_NOT_FOUND, INVALID_TOKEN, INVALID_CREDENTIALS
from api.utils.functions.env_config import CONFIG
from api.security.hash_crypt import verify_string_hash

TOKEN_URL = CONFIG.TOKEN_URL
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl=CONFIG.TOKEN_URL, auto_error=False)

def generate_token(user: User) -> Token:
    """
    Recibe un usuario y devuelve un token de seguridad.
    
    Args:
    - user (User): Usuario a incluir en el token de seguridad.
        
    Returns:
    - Token: Token de seguridad.
    """
    
    # creamos el token con el id del usuario, el tipo de usuario y la fecha de expiración
    data = {
        "sub": str(user.id),
        "user_type": user.user_type,
        "exp": datetime.utcnow() + timedelta(minutes=CONFIG.ACCESS_TOKEN_EXPIRE_MINUTES)
    }

    # codificamos el token
    encoded_jwt = jwt.encode(data, CONFIG.SECRET_KEY, algorithm=CONFIG.ALGORITHM)

    token = Token(access_token=encoded_jwt, token_type=CONFIG.TOKEN_TYPE)

    return token

async def get_user_from_token(session: Annotated[AsyncSession, Depends(get_session)], token: Annotated[str, Depends(OAUTH2_SCHEME)]) -> User:
    """
    Recibe un token de seguridad y devuelve el usuario que corresponde al token de seguridad.
    
    Args:
    - session (AsyncSession): Sesión de la base de datos.
    - token (str): Token de seguridad.

    Returns:
    - User: Usuario que corresponde al token de seguridad.

    Raises:
    - HTTPException: No se ha podido autenticar el usuario.
    """
    
    try:
        # decodificamos el token
        payload = jwt.decode(token, CONFIG.SECRET_KEY, algorithms=[CONFIG.ALGORITHM])
        # obtenemos el id del usuario
        id: UUID = payload.get("sub")

    except Exception as exc:
        # si no se ha podido decodificar el token, lanzamos una excepción y generamos un background task para imprimir el log del error
        background = BackgroundTask(print_log, INVALID_TOKEN, log_level=LogLevel.ERROR, exc=exc)
        raise HTTPExceptionWithBackgroundTask(**CREDENTIALS_EXCEPTION, background_task=background)
    
    # obtenemos el usuario
    user = await session.get(User, id)

    # si el usuario no existe, lanzamos una excepción y generamos un background task para imprimir el log del error
    if user is None:
        background = BackgroundTask(print_log, PERMISSION_USER_NOT_FOUND, log_level=LogLevel.ERROR)
        raise HTTPExceptionWithBackgroundTask(**CREDENTIALS_EXCEPTION, background_task=background)
    
    return user

async def get_user_from_token_or_none(session: Annotated[AsyncSession, Depends(get_session)], token: Annotated[str, Depends(OAUTH2_SCHEME)] = None) -> User | None:
    """
    Recibe un token de seguridad y devuelve el usuario que corresponde al token de seguridad. A diferencia de get_user_from_token, si no se puede autenticar devuelve None. 
    Utilizado cuando no es necesario autenticar al usuario pero se quiere autenticar si es posible.
    
    Args:
    - session (AsyncSession): Sesión de la base de datos.
    - token (str): Token de seguridad.

    Returns:
    - User: Usuario que corresponde al token de seguridad o None si no se ha podido autenticar.
    """
    
    try:
        # decodificamos el token
        user = await get_user_from_token(session, token)
    except:
        return None
    
    return user


async def authenticate_user(session: AsyncSession, username: str, password: str) -> User | None:
    """
    Autentica al usuario y devuelve el usuario si este existe y la contraseña es correcta, sino devuelve None.
    
    Args:
    - session (AsyncSession): Conexión a la base de datos.
    - username (str): Nombre de usuario o email del usuario que se quiere autenticar.
    - password (str): Contraseña del usuario que se quiere autenticar.

    Returns:
    - User: Usuario autenticado o None.
    """

    EMAIL_REGEX = r"[\w\W]+@[\w\W]+\.[\w\W]+"

    # convertimos la indentificación del usuario a minúsculas
    username = username.lower()

    # comprabamos si la identificación del usuario es un email o un nombre de usuario y obtenemos el campo de la base de datos que corresponde
    condition = User.username == username if not match(EMAIL_REGEX, username) else User.email == username
    # creamos la consulta
    statement = select(User).where(condition)
    # ejecutamos la consulta
    result = await session.execute(statement)
    # obtenemos el usuario
    user: User = result.scalar()

    # si el usuario no existe o la contraseña no es correcta, lanzamos una excepción y generamos un background task para imprimir el log del error
    if not user or not verify_string_hash(password, user.password):
        background = BackgroundTask(print_log, INVALID_CREDENTIALS, log_level=LogLevel.ERROR, username=username)
        raise HTTPExceptionWithBackgroundTask(**CREDENTIALS_EXCEPTION, background_task=background)

    return user
