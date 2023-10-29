from fastapi import status
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from fastapi.utils import is_body_allowed_for_status_code
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.background import BackgroundTask
from api.utils.functions.management_utils import print_log
from api.utils.constants.error_strings import ERROR_RESPONSE_UNEXPECTED_ERROR, LOG_UNEXPECTED_ERROR, LOG_INVALID_PARAMS
from api.utils.exceptions.http_exception_background import HTTPExceptionWithBackgroundTask
from api.models.enums import LogLevel

async def http_exception_backgroud_task_handler(request: Request, exc: HTTPExceptionWithBackgroundTask) -> Response:

    if is_body_allowed_for_status_code(exc.status_code):
        return JSONResponse({"detail": exc.detail}, status_code=exc.status_code, headers=exc.headers, background=exc.background)
    return Response(status_code=exc.status_code, headers=exc.headers, background=exc.background)


async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:

    errors = exc.errors()

    background = BackgroundTask(print_log, LOG_INVALID_PARAMS, LogLevel.WARNING, params=errors, url=request.url, method=request.method)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": jsonable_encoder(errors)},
        background=background
    )

async def unknown_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Función que maneja las excepciones no controladas. Registra el error en un archivo de log y cierra el servidor.
    
        Args:
            request (Request): Request que generó la excepción.
            exc (Exception): Excepción no controlada."""
    
    background = BackgroundTask(print_log, LOG_UNEXPECTED_ERROR, LogLevel.CRITICAL, exc=exc, url=request.url, method=request.method)
    return JSONResponse(ERROR_RESPONSE_UNEXPECTED_ERROR, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, background=background)

