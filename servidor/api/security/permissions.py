from typing import Annotated
from uuid import UUID
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.background import BackgroundTask
from api.database.database_models.models import User, Candidate
from api.security.security import get_user_from_token
from api.models.enums.models import UserType
from api.models.enums.models import LogLevel
from api.utils.functions.management_utils import print_log, create_http_exception
from api.utils.constants.error_strings import PERMISSION_DENIED, PERMISSION_DENIED_RESOURCE_NOT_VALID
from api.utils.constants.http_exceptions import FORBIDDEN_EXCEPTION, INCORRECT_RESOURCE_EXCEPTION
from api.database.connection import get_session

class PermissionsManager:
    """Clase que maneja los permisos de los usuarios. Si no recibe parametros, comprueba por defecto si el usuario es admin."""

    @staticmethod
    async def _raise_exception(ERROR: str, http_exception: dict = FORBIDDEN_EXCEPTION, **kwargs):
        """
        Método que lanza una excepción de tipo HTTPException. Crea un background task para imprimir el log del error con el mensaje de error y los argumentos que se le pasan.
        
        Args:
            ERROR (str): El mensaje de error.
            **kwargs: Los argumentos que se pasan al mensaje de error.
        """

        background = BackgroundTask(print_log, ERROR, log_level=LogLevel.ERROR, **kwargs)
        raise create_http_exception(**http_exception, background_task=background)
    

    @classmethod
    async def _is_owner(cls, request: Request, logged_user: User, resource_id: UUID) -> None:
        """
        Método que comprueba si el usuario es el dueño del recurso. Si no lo es, lanza una excepción de tipo HTTPException.
        Si el usuario es admin, no se comprueba si es el dueño del recurso.

        Args:
            request (Request): informacion de la petición.
            logged_user (User): El usuario que hace la petición.
            resource_id (UUID): El id del recurso que se quiere obtener.
        """
        if logged_user.user_type != UserType.ADMIN and logged_user.id != resource_id:
            await cls._raise_exception(PERMISSION_DENIED, user_id=logged_user.id, resource=request.url)

    @classmethod
    async def is_admin(cls, request: Request, user: Annotated[User, Depends(get_user_from_token)]) -> None:
        """
        Método que comprueba si el usuario es admin. Si no lo es, lanza una excepción de tipo HTTPException.	

        Args:
            request (Request): informacion de la petición.
            user (User): El usuario que hace la petición.	
        """

        if user.user_type != UserType.ADMIN:
            await cls._raise_exception(PERMISSION_DENIED, user_id=user.id, resource=request.url)

    @classmethod
    async def is_candidate_resource_owner(cls, request: Request, logged_user: Annotated[User, Depends(get_user_from_token)], candidate_id: UUID) -> None:
        """
        Método que comprueba si el usuario tipo candidato es el dueño del recurso. Si no lo es, lanza una excepción de tipo HTTPException.
        Si el usuario es admin, no se comprueba si es el dueño del recurso.

        Args:
            request (Request): informacion de la petición.
            user (User): El usuario que hace la petición.	
            candidate_id (UUID): El id del candidato que se quiere obtener.
        """

        await cls._is_owner(request, logged_user, candidate_id)


    @classmethod
    async def is_company_resource_owner(cls, request: Request, logged_user: Annotated[User, Depends(get_user_from_token)], company_id: UUID) -> None:
        """
        Método que comprueba si el usuario tipo empresa es el dueño del recurso. Si no lo es, lanza una excepción de tipo HTTPException.
        Si el usuario es admin, no se comprueba si es el dueño del recurso.

        Args:
            request (Request): informacion de la petición.
            user (User): El usuario que hace la petición.	
            candidate_id (UUID): El id del candidato que se quiere obtener.
        """

        await cls._is_owner(request, logged_user, company_id)


    @classmethod
    async def is_logged(cls, request: Request, user: Annotated[User, Depends(get_user_from_token)]) -> None:
        """
        Verifica si el usuario está autenticado.

        Args:
            request (Request): La solicitud HTTP entrante.
            user (User): El usuario autenticado.

        Raises:
            HTTPException: Si el usuario no está autenticado.
        """
        
        if not user:
            await cls._raise_exception(PERMISSION_DENIED, user_id="No Auth", resource=request.url)




        
        






