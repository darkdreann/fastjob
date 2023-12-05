from fastapi import status
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from fastapi.utils import is_body_allowed_for_status_code
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.background import BackgroundTask
from api.utils.functions.management_utils import print_log
from api.utils.constants.error_strings import ERROR_RESPONSE_UNEXPECTED_ERROR, LOG_UNEXPECTED_ERROR, LOG_INVALID_PARAMS, INVALID_CONTENT_TYPE
from api.utils.exceptions import HTTPExceptionWithBackgroundTask, DatabaseException, ResourceNotFoundException, RequestContentTypeError
from api.models.enums.models import LogLevel


async def http_exception_backgroud_task_handler(request: Request, exc: HTTPExceptionWithBackgroundTask) -> Response:
    """Función que maneja las excepciones relacionadas con HTTP. Registra el error en un archivo de log y cierra el servidor.

    Args:
        request (Request): Request que generó la excepción.
        exc (HTTPExceptionWithBackgroundTask): Excepción relacionada con HTTP.
        
    Returns:
        Response: Respuesta HTTP.
    """


    if is_body_allowed_for_status_code(exc.status_code):
        return JSONResponse({"detail": exc.detail}, status_code=exc.status_code, headers=exc.headers, background=exc.background)
    return Response(status_code=exc.status_code, headers=exc.headers, background=exc.background)


async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Función que maneja las excepciones relacionadas con la validación de los parámetros de una request. Registra el error en un archivo de log y cierra el servidor.

    Args:
        request (Request): Request que generó la excepción.
        exc (RequestValidationError): Excepción relacionada con la validación de los parámetros de una request.
    
    Returns:
        JSONResponse: Respuesta HTTP.
    """

    errors = exc.errors()

    background = BackgroundTask(print_log, LOG_INVALID_PARAMS, LogLevel.WARNING, params=errors, url=request.url, method=request.method)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": jsonable_encoder(errors)},
        background=background
    )


async def request_content_type_exception_handler(request: Request, exc: RequestContentTypeError) -> JSONResponse:
    """Función que maneja las excepciones relacionadas con la validación de los parámetros de una request. Registra el error en un archivo de log y cierra el servidor.

    Args:
        request (Request): Request que generó la excepción.
        exc (RequestValidationError): Excepción relacionada con la validación de los parámetros de una request.
    
    Returns:
        JSONResponse: Respuesta HTTP.
    """

    background = BackgroundTask(print_log, INVALID_CONTENT_TYPE, LogLevel.WARNING, url=request.url)

    return JSONResponse(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        content={"detail": exc.error_message},
        background=background
    )

async def database_exception_handler(request: Request, exc: DatabaseException | ResourceNotFoundException) -> JSONResponse:
    """Función que maneja las excepciones relacionadas con la base de datos. Registra el error en un archivo de log y cierra el servidor.
    
        Args:
            request (Request): Request que generó la excepción.
            exc (DatabaseException): Excepción relacionada con la base de datos.
            
        Returns:
            JSONResponse: Respuesta HTTP. """
    
    content = {"detail":exc.http_response["detail"]}
    status_code = exc.http_response["status_code"]
    background = exc.background_task

    return JSONResponse(content, status_code=status_code, background=background)

async def unknown_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Función que maneja las excepciones no controladas. Registra el error en un archivo de log y cierra el servidor.
    
        Args:
            request (Request): Request que generó la excepción.
            exc (Exception): Excepción no controlada.
        
        Returns:
            JSONResponse: Respuesta HTTP."""
    
    background = BackgroundTask(print_log, LOG_UNEXPECTED_ERROR, LogLevel.CRITICAL, exc=exc, url=request.url, method=request.method)
    return JSONResponse({"detail":ERROR_RESPONSE_UNEXPECTED_ERROR}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, background=background)

