from typing import Annotated, Self
from fastapi import Depends
from enum import Enum
from starlette.background import BackgroundTask
from uuid import UUID
from api.database.database_models.models import User
from api.security.security import get_user_from_token
from api.models.enums import UserType
from api.models.enums import LogLevel
from api.utils.functions.management_utils import print_log, create_http_exception
from api.utils.constants.error_strings import PERMISSION_DENIED, PERMISSION_USER_NOT_FOUND
from api.utils.constants.http_exceptions import FORBIDDEN_EXCEPTION


class PermissionsManager:
    """Clase que maneja los permisos de los usuarios. Si no recibe parametros, comprueba por defecto si el usuario es admin."""

    class Permission(Enum):
        """Enum que contiene los permisos."""

        IS_CANDIDATE = lambda **param : param["user"].user_type == UserType.CANDIDATE
        IS_COMPANY = lambda **param : param["user"].user_type == UserType.COMPANY
        IS_OWNER = lambda **param : param["user"].id == param["resource_id"]
        

        IS_JOB_OWNER = lambda **param : NotImplementedError("Not implemented yet")


    def __init__(self, permission: Permission = None) -> Self:
        """Crea una instancia de PermissionsManager. Para ser usado como dependencia en los endpoints. Recibe un permiso a comprobar.
           Puede no recibir un permiso, ya que por defecto comprueba si el usuario es admin. En ese caso seria un endpoint solo para admin.
            
            Args:
                permission Permission | None: Lista con los permisos que se quieren comprobar. Por defecto None.
                
            Returns:
                PermissionsManager: Instancia de PermissionsManager."""

        self.permission = permission
        

    def __call__(self, user: Annotated[User, Depends(get_user_from_token)], user_id: UUID | None = None) -> None:
        """Comprueba si el usuario tiene permiso para acceder a un recurso. 
            Siempre comprueba si el usuario es admin, en caso que lo sea no sigue comprobando permisos.
        
            Args:
                user (UserDB): Usuario.
                user_id (UUID, optional): Id del usuario duenio del recurso. None por defecto.
                
            Raises:
                HTTPException: Excepción si el usuario no tiene permiso para acceder al recurso."""
        
        def rais_exception(ERROR: str, **kwargs):
            background = BackgroundTask(print_log, ERROR, log_level=LogLevel.ERROR, **kwargs)
            raise create_http_exception(**FORBIDDEN_EXCEPTION, background_task=background)

        if not user:
            rais_exception(PERMISSION_USER_NOT_FOUND)
        
        if user.user_type == UserType.ADMIN: return

        if self.permission is None:
            rais_exception(PERMISSION_DENIED, user_id=user.id, resource_id=user_id)

        if not self.permission(user=user, resource_id=user_id):
            rais_exception(PERMISSION_DENIED, user_id=user.id, resource_id=user_id)

        
        






