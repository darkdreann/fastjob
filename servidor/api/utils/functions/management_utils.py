from fastapi import status
from api.models.enums import LogLevel
from api.logging.logging_error import ERROR_LOGGER 
from api.logging.logging_info import INFO_LOGGER
from api.models.enums import LogLevel
from api.utils.constants.error_strings import LOG_FORMAT_ERROR
from api.utils.exceptions.http_exception_background import HTTPExceptionWithBackgroundTask
from api.utils.constants.http_exceptions import _DEFAULT_ERROR_MESSAGE



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
            background_task (BackgroundTask, optional): Tarea en segundo plano. Por defecto None."""

    status_code = kwargs.get("status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
    detail = kwargs.get("detail", _DEFAULT_ERROR_MESSAGE)
    headers = kwargs.get("headers", None)
    background_task = kwargs.get("background_task", None)

    return HTTPExceptionWithBackgroundTask(
        status_code=status_code,
        detail=detail,
        headers=headers,
        background=background_task
    )