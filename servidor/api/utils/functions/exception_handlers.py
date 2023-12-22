from fastapi import status
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from fastapi.utils import is_body_allowed_for_status_code
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.background import BackgroundTask
from api.models.enums.models import LogLevel
from api.utils.functions.management_utils import print_log
from api.utils.constants.error_strings import ERROR_RESPONSE_UNEXPECTED_ERROR, LOG_UNEXPECTED_ERROR, LOG_INVALID_PARAMS, INVALID_CONTENT_TYPE
from api.utils.exceptions import HTTPExceptionWithBackgroundTask, DatabaseException, ResourceNotFoundException, RequestContentTypeError


async def http_exception_background_task_handler(request: Request, exc: HTTPExceptionWithBackgroundTask) -> Response:
    """
    Función que maneja las excepciones HTTPExceptionWithBackgroundTask.
    Registra el error en un archivo de log y devuelve una respuesta HTTP.

    Args:
    - request (Request): Request que generó la excepción.
    - exc (HTTPExceptionWithBackgroundTask): Excepción relacionada con HTTP.

    Returns:
    - Response: Respuesta HTTP.
    """

    # si el código de estado permite el uso de un body, se devuelve un JSONResponse
    if is_body_allowed_for_status_code(exc.status_code):
        return JSONResponse({"detail": exc.detail}, status_code=exc.status_code, headers=exc.headers, background=exc.background_task)
    
    # si el código de estado no permite el uso de un body, se devuelve un Response
    return Response(status_code=exc.status_code, headers=exc.headers, background=exc.background_task)


async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Función que maneja las excepciones RequestValidationError.
    Registra el error en un archivo de log y devuelve una respuesta HTTP.

    Args:
    - request (Request): Request que generó la excepción.
    - exc (RequestValidationError): Excepción relacionada con la validación de los parámetros de una request.

    Returns:
    - JSONResponse: Respuesta HTTP.
    """

    # se obtienen los errores de validación
    errors = exc.errors()

    # crea una tarea en segundo plano para registrar el error en un archivo de log
    background = BackgroundTask(print_log, LOG_INVALID_PARAMS, LogLevel.WARNING, params=errors, url=request.url, method=request.method)

    # devuelve una respuesta HTTP
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": jsonable_encoder(errors)},
        background=background
    )


async def request_content_type_exception_handler(request: Request, exc: RequestContentTypeError) -> JSONResponse:
    """
    Función que maneja las excepciones RequestContentTypeError.
    Registra el error en un archivo de log y devuelve una respuesta HTTP.

    Args:
    - request (Request): Request que generó la excepción.
    - exc (RequestContentTypeError): Excepción relacionada con la validación del tipo de contenido de una request.

    Returns:
    - JSONResponse: Respuesta HTTP.
    """

    # crea una tarea en segundo plano para registrar el error en un archivo de log
    background = BackgroundTask(print_log, INVALID_CONTENT_TYPE, LogLevel.WARNING, url=request.url)

    # devuelve una respuesta HTTP
    return JSONResponse(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        content={"detail": exc.error_message},
        background=background
    )

async def database_exception_handler(request: Request, exc: DatabaseException | ResourceNotFoundException) -> JSONResponse:
    """
    Función que maneja las excepciones DatabaseException y ResourceNotFoundException.
    Registra el error en un archivo de log y devuelve una respuesta HTTP.
    
    Args:
    - request (Request): Request que generó la excepción.
    - exc (DatabaseException): Excepción relacionada con la base de datos.

    Returns:
    - JSONResponse: Respuesta HTTP. 
    """

    # obtiene el mensaje de error
    content = {"detail":exc.http_response["detail"]}
    # obtiene el código de estado
    status_code = exc.http_response["status_code"]
    # obtiene la tarea en segundo plano
    background = exc.background_task

    # devuelve una respuesta HTTP
    return JSONResponse(content, status_code=status_code, background=background)

async def unknown_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Función que maneja las excepciones no controladas. Registra el error en un archivo de log y cierra el servidor.
    
    Args:
    - request (Request): Request que generó la excepción.
    - exc (Exception): Excepción no controlada.

    Returns:
    - JSONResponse: Respuesta HTTP.
    """
    
    # crea una tarea en segundo plano para registrar el error en un archivo de log
    background = BackgroundTask(print_log, LOG_UNEXPECTED_ERROR, LogLevel.CRITICAL, exc=exc, url=request.url, method=request.method)
    # devuelve una respuesta HTTP
    return JSONResponse({"detail":ERROR_RESPONSE_UNEXPECTED_ERROR}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, background=background)
