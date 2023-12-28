from typing import Annotated
from fastapi import BackgroundTasks, Depends, Request
from api.models.enums.models import LogLevel
from api.loggs.loggers import ERROR_LOGGER, INFO_LOGGER
from api.models.enums.models import LogLevel
from api.database.database_models.models import User
from api.utils.constants.error_strings import LOG_FORMAT_ERROR
from api.utils.constants.info_strings import RESOURCE_REQUEST

def print_log(message: str, log_level: LogLevel, recursive: bool = False, **extra_message_info) -> None:
    """
    Guarda un mensaje en un archivo de log. Puede recibir parámetros para formatear el mensaje.
    Si se produce un error al formatear el mensaje, se intentará imprimir un mensaje de error en el log.
    Si se vuelve a producir un error al imprimir el mensaje de error, no se volverá a intentar imprimir el mensaje de error.
        
    Args:
    - message (str): Mensaje a guardar en el log.
    - log_level (LogLevel): Nivel de log.
    - recursive (bool): Indica si se está llamando a la función recursivamente para evitar un bucle infinito.
    - extra_message_info (dict): Información extra para formatear el mensaje de log.
    """

    # Si es un log de info, se usa el logger de info, si no lo es, se usa el logger de error
    logger = INFO_LOGGER if log_level == LogLevel.INFO else ERROR_LOGGER

    # Si hay información extra para formatear el mensaje, se intenta formatear
    if extra_message_info:
        try:
            message = message.format(**extra_message_info)
        # Si se produce un error al formatear el mensaje, se intenta imprimir un mensaje de error en el log pasando la recursive a True para evitar un bucle infinito.
        except (KeyError, IndexError, ValueError) as exc:
            if not recursive:
                print_log(LOG_FORMAT_ERROR, LogLevel.ERROR, recursive=True, exc=exc)

    # Se guarda el mensaje en el log
    logger.log(log_level.value, message)

# import en esta línea para evitar circular imports
from api.security.security import get_user_from_token_or_none

async def endpoint_request_log(request: Request, background_tasks: BackgroundTasks, logged_user: Annotated[User, Depends(get_user_from_token_or_none)]) -> None:
    """
    Crea una tarea en segundo plano para guardar en un log la petición a un endpoint.
    Puede recibir el usuario loggeado para incluir su id en el log, si no se recibe, se incluirá "No Auth".

    Args:
    - request (Request): Petición HTTP.
    - background_tasks (BackgroundTasks): Tareas en segundo plano.
    - logged_user (User): Usuario loggeado.
    """

    # Se obtiene el método HTTP y la URL de la petición
    METHOD = request.method
    URL = request.url.path
    # por defecto, el id del usuario es "No Auth"
    USER_ID = "No Auth"

    # Si se ha recibido un usuario loggeado, se obtiene su id
    if logged_user:
        USER_ID = logged_user.id

    # Se crea una tarea en segundo plano para guardar en un log la petición a un endpoint
    background_tasks.add_task(print_log, RESOURCE_REQUEST, LogLevel.INFO, user_id=USER_ID, http_method=METHOD, resource_url=URL)