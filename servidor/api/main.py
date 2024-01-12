from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.routers import *
from api.models.enums.models import LogLevel
from api.utils.functions.env_config import CONFIG
from api.utils.functions.management_utils import print_log
from api.utils.constants.error_strings import DATABASE_CREATION_ERROR
from api.utils.constants.info_strings import SERVER_STARTED, SERVER_STOPPED
from api.database.connection import create_tables, close_connection, OperationalError, ArgumentError
from api.utils.functions.exception_handlers import HTTPExceptionWithBackgroundTask, RequestValidationError, DatabaseException, ResourceNotFoundException, RequestContentTypeError
from api.utils.functions.exception_handlers import http_exception_background_task_handler, request_validation_exception_handler, unknown_exception_handler, database_exception_handler, request_content_type_exception_handler
from api.database.database_views import create_database_views, refresh_database_views
from api.database.database_models.view_models import create_all_views_instances
from api.database.database_functions import create_database_functions
from api.utils.functions.schedule_tasks import AsyncSchedulerManager



# si estamos en desarrollo, importamos las funciones de creación de datos de prueba y eliminación de tablas
if CONFIG.DEVELOPMENT:
    from api.tests.test_utils.db_manage_test import create_test_data
    from api.database.connection import drop_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Función asincrónica que maneja el ciclo de vida de la aplicación.

    Realiza las siguientes tareas:
    - Crea las funciones de la base de datos.
    - Crea las tablas en la base de datos.
    - En modo de desarrollo, crea datos de prueba.
    - Imprime un mensaje de inicio del servidor.
    - Espera hasta que se cierre la aplicación.
    - En modo de desarrollo, elimina las tablas de la base de datos.
    - Cierra la conexión con la base de datos.
    - Imprime un mensaje de parada del servidor.
    """
    try:
        # se intenta crear las funciones, tablas, vistas y tareas programadas de la base de datos
        await create_database_functions()
        await create_tables()
        await create_database_views()
        await create_all_views_instances()
        AsyncSchedulerManager.add_job(refresh_database_views, 'interval', minutes=CONFIG.SCHEDULER_INTERVAL)
        AsyncSchedulerManager.start()

    except (OperationalError, ArgumentError) as exc:
        # si ocurre un error, se lanza una excepción
        raise RuntimeError(DATABASE_CREATION_ERROR.format(exc=exc))
    
    # si estamos en desarrollo, se crean datos de prueba
    if CONFIG.DEVELOPMENT:
        await create_test_data()

    # se imprime un log de inicio del servidor
    print_log(SERVER_STARTED, LogLevel.INFO)

    yield

    # si estamos en desarrollo, se eliminan las tablas de la base de datos
    if CONFIG.DEVELOPMENT:
        await drop_tables()

    AsyncSchedulerManager.shutdown()
    # se cierra la conexión con la base de datos
    await close_connection()
    # se imprime un log de parada del servidor
    print_log(SERVER_STOPPED, LogLevel.INFO)

# se crea la aplicación
app = FastAPI(lifespan=lifespan)

# se añaden las rutas
app.include_router(user.login_route)
app.include_router(user.user_route)
app.include_router(sector.sector_route)
app.include_router(address.address_route)
app.include_router(education.education_route)
app.include_router(language.language_route)
app.include_router(candidate.candidate_route)
app.include_router(experience.candidate_experience_route)
app.include_router(candidate_language.candidate_language_route)
app.include_router(candidate_education.candidate_education_route)
app.include_router(company.company_route)
app.include_router(job.job_route)
app.include_router(job_candidate.job_candidate_route)

# se añaden los manejadores de excepciones
app.add_exception_handler(HTTPExceptionWithBackgroundTask, http_exception_background_task_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(RequestContentTypeError, request_content_type_exception_handler)
app.add_exception_handler(DatabaseException, database_exception_handler)
app.add_exception_handler(ResourceNotFoundException, database_exception_handler)
app.add_exception_handler(Exception, unknown_exception_handler)