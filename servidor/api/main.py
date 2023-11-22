from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.utils.functions.exception_handlers import http_exception_backgroud_task_handler, request_validation_exception_handler, unknown_exception_handler, database_exception_handler
from api.utils.functions.exception_handlers import HTTPExceptionWithBackgroundTask, RequestValidationError, DatabaseException, ResourceNotFoundException
from api.utils.functions.env_config import CONFIG
from api.utils.functions.management_utils import print_log
from api.database.connection import create_database_functions, create_tables, close_connection, OperationalError, ArgumentError
from api.utils.constants.error_strings import TABLES_AND_FUNCTIONS_FAILED
from api.utils.constants.info_strings import SERVER_STARTED, SERVER_STOPPED
from api.models.enums.models import LogLevel
from api.routers import *


if CONFIG.DEVELOPMENT:
    from api.tests.test_utils.db_manage_test import create_test_data
    from api.database.connection import drop_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await create_database_functions()
        await create_tables()

    except (OperationalError, ArgumentError) as exc:
        raise RuntimeError(TABLES_AND_FUNCTIONS_FAILED.format(exc=exc))
    
    if CONFIG.DEVELOPMENT:
        await create_test_data()

    print_log(SERVER_STARTED, LogLevel.INFO)

    yield 

    if CONFIG.DEVELOPMENT:
        await drop_tables()

    await close_connection()
    print_log(SERVER_STOPPED, LogLevel.INFO)




app = FastAPI(lifespan=lifespan)

#app.include_router(candidate.candidateRoute)
app.include_router(user.loginRoute)
app.include_router(user.userRoute)
app.include_router(sector.sectorRoute)
app.include_router(adress.adressRoute)
app.include_router(education.educationRoute)
app.include_router(language.languageRoute)

app.add_exception_handler(HTTPExceptionWithBackgroundTask, http_exception_backgroud_task_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(DatabaseException, database_exception_handler)
app.add_exception_handler(ResourceNotFoundException, database_exception_handler)
app.add_exception_handler(Exception, unknown_exception_handler)