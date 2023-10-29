import re
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.background import BackgroundTask
from pydantic import BaseModel
from api.utils.constants.http_exceptions import INTEGRATION_EXCEPTION
from api.utils.functions.management_utils import create_http_exception
from api.models.enums import LogLevel
from api.utils.functions.management_utils import print_log

def update_model(model_to_update: BaseModel, new_data: dict) -> None:
    """Actualiza los atributos de un modelo con los datos de otro modelo o diccionario.
    
        Args:
            model_to_update (BaseModel): Modelo a actualizar.
            new_data (dict): Diccionario con los datos a actualizar."""

    new_data_dict = vars(new_data) if not isinstance(new_data, dict) else new_data

    for atribute in new_data_dict.keys():
        setattr(model_to_update, atribute, new_data_dict[atribute])


async def secure_commit(session: AsyncSession) -> None:
    """Realiza un commit de la sesión, si se produce una excepción de integridad, hace rollback y lanza una excepción.
    
        Args:
            session (AsyncSession): Sesión de la base de datos.
            integrity_exceptions (dict, optional): Diccionario con las excepciones de integridad.
            server_exception (HTTPException, optional): Excepción a lanzar en caso de error. Por defecto SERVER_EXCEPTION."""

    try:
        await session.commit()

    except IntegrityError as e:
        await session.rollback()
    
        def get_error_index(error_info: dict) -> str:
            """Devuelve el índice del error.
            
                Args:
                    error_info (dict): Diccionario con la información del error.
                    
                Returns:
                    str: Índice del error."""

            if "constraint_name" in error_info.keys():
                return error_info['constraint_name']
            
            if "message" in error_info.keys():
                return re.sub('".*?" ' ,'' ,error_info["message"])
            
            return None
    
        error_index = get_error_index(e.orig.__cause__.__dict__)

        http_exception = INTEGRATION_EXCEPTION[error_index] if error_index in INTEGRATION_EXCEPTION.keys() else {}
        background = BackgroundTask(print_log, e, LogLevel.ERROR)

        raise create_http_exception(**http_exception, background_task=background)
    
    
    except Exception as e:
        await session.rollback()

        background = BackgroundTask(print_log, e, LogLevel.ERROR)

        raise create_http_exception(background_task=background)

