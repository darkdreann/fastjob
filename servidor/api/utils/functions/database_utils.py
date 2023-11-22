from re import sub
from uuid import UUID
from sqlalchemy import select, Row
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption
from sqlalchemy.sql._typing import _ColumnsClauseArgument as ColumnsClauseArgument, _ColumnExpressionOrStrLabelArgument as ColumnOrderArgument
from starlette.background import BackgroundTask
from typing import Any, Sequence
from pydantic import BaseModel
from api.utils.constants.http_exceptions import INTEGRATION_EXCEPTION, RESOURCE_NOT_FOUND_EXCEPTION, DEFAULT_EXCEPTION
from api.utils.functions.management_utils import print_log
from api.models.enums.models import LogLevel
from api.database.database_models.models import Base, User
from api.utils.constants.error_strings import RESOURCE_NOT_FOUND, UNKNOWN_QUERY_ERROR, RESOURCES_NOT_FOUND
from api.utils.exceptions import DatabaseException, ResourceNotFoundException


def _sequence_param(param):
    """
    Convierte el parámetro en una tupla si no es una secuencia y si no es None. De lo contrario devuelve el parámetro sin cambios.

    Args:
        param: El parámetro a convertir.

    Returns:
        Una tupla que contiene el parámetro si no es una secuencia, de lo contrario devuelve el parámetro sin cambios.
    """
  
    if param is not None and not isinstance(param, Sequence):
        return (param,)
    return param


def _raise_exception(exc: Exception) -> None:
    """Lanza una excepción de error desconocido.

        Args:
            exc (Exception): Excepción original.

        Raises:
            DatabaseException: Excepción de error desconocido.
    """

    background = BackgroundTask(print_log, UNKNOWN_QUERY_ERROR, LogLevel.ERROR, exc=exc)
    raise DatabaseException(error_message=exc, http_response=DEFAULT_EXCEPTION, background_task=background)

def _raise_not_found(log_message: str, **kwargs) -> None:
    """Lanza una excepción de recurso no encontrado.
    
        Args:
            log_message (str): Mensaje de log.
            **kwargs: Argumentos adicionales.
            
        Raises:
            DatabaseException: Excepción de recurso no encontrado.
    """

    background = BackgroundTask(print_log, log_message, LogLevel.WARNING, **kwargs)
    raise ResourceNotFoundException(error_message=log_message, http_response=RESOURCE_NOT_FOUND_EXCEPTION, background_task=background)



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
        
        Raises:
            DatabaseException: Excepción de error de integridad."""

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
                return sub('".*?" ' ,'' ,error_info["message"])
            
            return None
    
        error_index = get_error_index(e.orig.__cause__.__dict__)

        http_exception = INTEGRATION_EXCEPTION[error_index] if error_index in INTEGRATION_EXCEPTION.keys() else {}
        background = BackgroundTask(print_log, e, LogLevel.ERROR)

        raise DatabaseException(error_message=e.detail, http_response=http_exception, background_task=background)
    
    
    except Exception as e:
        await session.rollback()

        background = BackgroundTask(print_log, e, LogLevel.ERROR)

        raise DatabaseException(error_message=str(e), http_response=DEFAULT_EXCEPTION, background_task=background)


async def get_database_records(session: AsyncSession, 
                               *fields: ColumnsClauseArgument, 
                               options: Sequence[ExecutableOption] | ExecutableOption = None, 
                               where: Sequence[bool] | bool = None, 
                               order: Sequence[ColumnOrderArgument] | ColumnOrderArgument = None, 
                               **kwargs) -> Sequence[Row[Any]] | Sequence[Any] | Row[Any] | Any | None:
    """
    Obtiene registros de una tabla de la base de datos.

    Args:
        session (AsyncSession): Sesión de la base de datos.
        model (Base): Modelo que representa la tabla de la base de datos.
        options (Sequence, optional): Lista de campos a cargar. Defaults to None.
        where (Sequence, optional): Lista de condiciones para filtrar los registros. Defaults to None.
        order (Sequence, optional): Lista de campos para ordenar los registros. Defaults to None.
        **kwargs: Argumentos adicionales.
            limit (int, optional): Límite de registros a obtener. Defaults to None.
            offset (int, optional): Desplazamiento de registros a obtener. Defaults to None.
            unique (bool, optional): Indica si se deben obtener registros únicos. Defaults to False.
            scalar (bool, optional): Indica si se deben devolver los registros como escalares. Defaults to True.
            result_list (bool, optional): Indica si se deben devolver los registros como una lista. Defaults to True. En caso de ser False, se devolverá un único registro.

    Returns:
        Sequence[Row[Any]] | Sequence[Any] | Row[Any] | Any | None: Registros obtenidos.

    Raises:
        DatabaseException: Excepción de recurso no encontrado.
    """

    try:
        options = _sequence_param(options)
        where = _sequence_param(where)
        order = _sequence_param(order)

        # Se obtienen los kwargs.
        limit = kwargs.get('limit', None)
        offset = kwargs.get('offset', None)
        unique = kwargs.get('unique', False)
        scalar = kwargs.get('scalar', True)
        result_list = kwargs.get('result_list', True)

        statement = select(*fields)

        # Se añaden las opciones.
        if options:
            statement = statement.options(*options)

        # Se añaden las condiciones.
        if where:
            statement = statement.where(*where)

        # Se añaden el límite.
        if limit:
            statement = statement.limit(limit)
        
        # Se añade el desplazamiento.
        if offset:
            statement = statement.offset(offset)

        if order:
            print(f"cerdo: {order}")
            statement = statement.order_by(*order)

        # Se ejecuta la consulta.
        result = await session.execute(statement)

        # Se devuelven los registros.
        if unique:
            result = result.unique()

        if scalar:
            result = result.scalars()

        if result_list:
            records = result.all()

            if len(records) < 1:
                _raise_not_found(RESOURCES_NOT_FOUND, resource_type=statement.get_final_froms(), query=statement)

            return records
        
        record = result.one_or_none()

        if record is None:
            _raise_not_found(RESOURCES_NOT_FOUND, resource_type=statement.get_final_froms(), query=statement)

        return record
    
    except DatabaseException as e:
        raise e
    except Exception as e:
        _raise_exception(e)

async def get_record_by_id(session: AsyncSession, model: Base, record_id: UUID | tuple[UUID], options: Sequence[ExecutableOption] | ExecutableOption = None) -> Base:
    """
    Obtiene un registro de la base de datos por su id.

    Args:
        session (AsyncSession): Sesión de base de datos.
        model (Base): Modelo de la base de datos.
        record_id (UUID): Id del registro a obtener.
        logged_user (User): Usuario que realiza la petición.
        options (Sequence, optional): Campos adicionales a cargar. Defaults to ().

    Returns:
        Base: Registro obtenido.

    Raises:
        DatabaseException: Si el registro no existe.
    """

    options = _sequence_param(options)
    
    try:
        record = await session.get(model, record_id, options=options)
    except Exception as e:
        _raise_exception(e)

    if record is None:
        _raise_not_found(RESOURCE_NOT_FOUND, resource_id=record_id, resource_type=model.__name__)

    return record



async def get_user_by_id(session: AsyncSession, logged_user: User, model: Base, user_id: UUID, extra_fields: Sequence[ExecutableOption] | ExecutableOption = ()) -> User:
    """
    Obtiene un usuario de la base de datos por su id.

    Args:
        session (AsyncSession): Sesión de base de datos.
        model (Base): Modelo de la base de datos.
        record_id (UUID): Id del registro a obtener.
        logged_user (User): Usuario que realiza la petición.
        extra_fields (list, optional): Campos adicionales a cargar. Defaults to ().
        logged_user (User, optional): Usuario que realiza la petición. Defaults to Depends(get_user_from_token).

    Returns:
        Base: Registro obtenido.

    Raises:
        DatabaseException: Si el registro no existe.
    """

    

    if user_id == logged_user.id: return logged_user

    return await get_record_by_id(session, model, user_id, extra_fields)