from fastapi import BackgroundTasks, Depends, Request
from typing import Annotated
from api.models.enums.models import LogLevel
from api.logging.logging_error import ERROR_LOGGER 
from api.logging.logging_info import INFO_LOGGER
from api.models.enums.models import LogLevel
from api.utils.constants.error_strings import LOG_FORMAT_ERROR
from api.utils.constants.info_strings import RESOURCE_REQUEST
from api.utils.exceptions import HTTPExceptionWithBackgroundTask
from api.utils.constants.http_exceptions import DEFAULT_EXCEPTION
from api.database.database_models.models import User

def print_log(message: str, log_level: LogLevel, recursive: bool = False, **extra_message_info) -> None:
    """Guarda un mensaje en un archivo de log. Puede recibir un usuario para guardar su id en el log.
        También puede recibir una excepción para guardar su mensaje de error en el log.
        
        Args:
            message (str): Mensaje a guardar en el log.
            log_level (LogLevel): Nivel de log.
            recursive (bool): Indica si se está llamando a la función recursivamente para evitar un bucle infinito.
            extra_message_info (dict): Información extra para formatear el mensaje de log."""

    logger = INFO_LOGGER if log_level == LogLevel.INFO else ERROR_LOGGER

    if extra_message_info:
        try:
            message = message.format(**extra_message_info)
        except (KeyError, IndexError, ValueError) as exc:
            if not recursive: print_log(LOG_FORMAT_ERROR, LogLevel.WARNING, recursive=True, exc=exc)

    logger.log(log_level.value, message)


def create_http_exception(**kwargs) -> HTTPExceptionWithBackgroundTask:
    """Crea una excepción HTTPEXceptionWithBackgroundTask. Recibe los siguientes parámetros:
    
        Args:
            status_code (int, optional): Código de estado de la excepción. Por defecto 500.
            detail (str, optional): Detalle de la excepción. Por defecto "Something unexpected has happened on the server, please contact the system administrator.".
            headers (dict, optional): Cabeceras de la excepción. Por defecto None.
            background_task (BackgroundTask, optional): Tarea en segundo plano. Por defecto None.
            
        Returns:
            HTTPExceptionWithBackgroundTask: Excepción HTTP."""

    status_code = kwargs.get("status_code", DEFAULT_EXCEPTION["status_code"])
    detail = kwargs.get("detail", DEFAULT_EXCEPTION["detail"])
    headers = kwargs.get("headers", None)
    background_task = kwargs.get("background_task", None)

    return HTTPExceptionWithBackgroundTask(
        status_code=status_code,
        detail=detail,
        headers=headers,
        background=background_task
    )

# import en esta linea para evitar circular imports
from api.security.security import get_user_from_token

async def endpoint_request_log(request: Request, background_tasks: BackgroundTasks, logged_user: Annotated[User, Depends(get_user_from_token)]) -> None:
    """
    Crea una tarea en segundo plano para guardar en un log la petición a un endpoint.

    Args:
        request (Request): Petición HTTP.
        background_tasks (BackgroundTasks): Tareas en segundo plano.
        logged_user (User): Usuario loggeado.
    """

    METHOD = request.method
    URL = request.url.path
    USER_ID = logged_user.id

    background_tasks.add_task(print_log, RESOURCE_REQUEST, LogLevel.INFO, user_id=USER_ID, http_method=METHOD, resource_url=URL)