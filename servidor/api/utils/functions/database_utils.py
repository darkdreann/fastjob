from re import sub
from uuid import UUID
from typing import Any, Sequence
from sqlalchemy import select, Row
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption
from sqlalchemy.sql._typing import _ColumnsClauseArgument as ColumnsClauseArgument, _ColumnExpressionOrStrLabelArgument as ColumnArgument
from starlette.background import BackgroundTask
from collections.abc import Iterable
from api.utils.constants.http_exceptions import INTEGRATION_EXCEPTION, RESOURCE_NOT_FOUND_EXCEPTION, DEFAULT_EXCEPTION
from api.utils.functions.management_utils import print_log
from api.models.enums.models import LogLevel
from api.database.database_models.models import Base, User
from api.utils.constants.error_strings import RESOURCE_NOT_FOUND, UNKNOWN_QUERY_ERROR, RESOURCES_NOT_FOUND
from api.utils.exceptions import DatabaseException, ResourceNotFoundException


def _iterable_param(param):
    """
    Convierte el parámetro en una tupla si no es iterable, si es un diccionario y si no es None. 
    De lo contrario, devuelve el parámetro sin cambios.

    Args:
    - param: El parámetro a convertir.

    Returns:
    - Una tupla que contiene el parámetro si no es una secuencia, de lo contrario devuelve el parámetro sin cambios.
    """

    # Si el parámetro no es iterable o es un diccionario, se convierte en una tupla.
    if param is not None and (not isinstance(param, Iterable) or isinstance(param, dict)):
        return (param,)
    return param

def _raise_exception(exc: Exception) -> None:
    """
    Lanza una excepción DatabaseException con el mensaje de error de la excepción original.

    Args:
    - exc (Exception): Excepción original.

    Raises:
    - DatabaseException: Excepción de error de base de datos.
    """

    # Se crea una tarea en segundo plano para imprimir el log del error.
    background = BackgroundTask(print_log, UNKNOWN_QUERY_ERROR, LogLevel.ERROR, exc=exc)
    # Se lanza la excepción.
    raise DatabaseException(error_message=exc, http_response=DEFAULT_EXCEPTION, background_task=background)

def _raise_not_found(log_message: str, **kwargs) -> None:
    """
    Lanza una excepción de recurso no encontrado.
    
    Args:
    - log_message (str): Mensaje de log.
    - kwargs: Argumentos adicionales.

    Raises:
    - DatabaseException: Excepción de recurso no encontrado.
    """

    # Se crea una tarea en segundo plano para imprimir el log del error.
    background = BackgroundTask(print_log, log_message, LogLevel.WARNING, **kwargs)
    # Se lanza la excepción.
    raise ResourceNotFoundException(error_message=log_message, http_response=RESOURCE_NOT_FOUND_EXCEPTION, background_task=background)


async def secure_commit(session: AsyncSession) -> None:
    """
    Realiza un commit de la sesión capturando las posibles excepciones.
    Si se produce una excepción, se realiza un rollback de la sesión y se lanza una excepción DatabaseException.
    Esa excepción será capturada por el manejador de excepciones de la aplicación y se devolverá una respuesta HTTP con el código de error correspondiente.

    Args:
    - session (AsyncSession): Sesión de la base de datos.

    Raises:
    - DatabaseException: Excepción de error de integridad.
    """

    try:
        # Se realiza el commit.
        await session.commit()

    except IntegrityError as e:
        # Se realiza el rollback. 
        await session.rollback()
    
        
        def get_error_index(error_info: dict) -> str | None:
            """
            Permite obtener el nombre de la constraint que ha provocado el error.
            En caso de no existir, se devuelve el mensaje de error.
            Si no existe el mensaje de error, se devuelve None.
            
            Args:
            - error_info (dict): Diccionario con la información del error.

            Returns:
            - str: Índice del error.
            """
            
            # si existe el índice "constraint_name", se devuelve su valor.
            if "constraint_name" in error_info.keys():
                return error_info['constraint_name']
            
            # si existe el índice "message", se devuelve su valor sin los elementos entre comillas.
            if "message" in error_info.keys():
                return sub('".*?" ' ,'' ,error_info["message"])
            
            return None

        # Se obtiene el índice del error.
        error_index = get_error_index(e.orig.__cause__.__dict__)

        # Se obtiene el mensaje de error usando el índice. Si no existe, se devuelve el mensaje por defecto.
        http_exception = INTEGRATION_EXCEPTION[error_index] if error_index in INTEGRATION_EXCEPTION.keys() else DEFAULT_EXCEPTION
        # Se crea una tarea en segundo plano para imprimir el log del error.
        background = BackgroundTask(print_log, e, LogLevel.ERROR)

        # Se lanza la excepción.
        raise DatabaseException(error_message=e.detail, http_response=http_exception, background_task=background)
    
    
    except Exception as e:
        # Se realiza el rollback.
        await session.rollback()

        # Se crea una tarea en segundo plano para imprimir el log del error.
        background = BackgroundTask(print_log, e, LogLevel.ERROR)

        # Se lanza la excepción.
        raise DatabaseException(error_message=str(e), http_response=DEFAULT_EXCEPTION, background_task=background)


async def get_database_records(session: AsyncSession, 
                               *fields: ColumnsClauseArgument,
                               froms: Sequence[Base] | Base = None,
                               joins: Sequence[dict] | dict = None,
                               options: Sequence[ExecutableOption] | ExecutableOption = None, 
                               where: Sequence[bool] | bool = None,
                               group_by: Sequence[ColumnArgument] | ColumnArgument = None,
                               having: Sequence[bool] | bool = None,
                               order: Sequence[ColumnArgument] | ColumnArgument = None, 
                               **kwargs) -> Sequence[Row[Any]] | Sequence[Any] | Row[Any] | Any | None:
    """
    Obtiene los registros de la base de datos que cumplen con las condiciones indicadas.
    Puede devolver una lista de registros, un único registro o un único valor.

    Args:
    - session (AsyncSession): Sesión de la base de datos.
    - model (Base): Modelo que representa la tabla de la base de datos.
    - fields (ColumnsClauseArgument): Campos a obtener.
    - joins (Sequence[dict], optional): Lista de joins. Defaults to None:
        - target (Base): Modelo que representa la tabla de la base de datos.
        - onclause (bool): Condición de unión. Defaults to None.
        - isouter (bool): Indica si es un join externo. Defaults to False.
        - full (bool): Indica si es un join completo. Defaults to False.
    - options (Sequence, optional): Lista de campos a cargar. Defaults to None.
    - where (Sequence, optional): Lista de condiciones para filtrar los registros. Defaults to None.
    - group_by (Sequence | optional): Lista de campos para agrupar los registros.
    - having (Sequence | optional): Lista de condiciones para filtrar los registros agrupados.
    - order (Sequence, optional): Lista de campos para ordenar los registros. Defaults to None.
    - **kwargs: Argumentos adicionales.
        - distinct (bool, optional): Indica si se deben obtener registros únicos. Defaults to False.
        - limit (int, optional): Límite de registros a obtener. Defaults to None.
        - offset (int, optional): Desplazamiento de registros a obtener. Defaults to None.
        - unique (bool, optional): Indica si se deben obtener registros únicos. Defaults to False.
        - scalar (bool, optional): Indica si se deben devolver los registros como escalares. Defaults to True.
        - result_list (bool, optional): Indica si se deben devolver los registros como una lista. Defaults to True. En caso de ser False, se devolverá un único registro.

    Returns:
    - Sequence[Row[Any]] | Sequence[Any] | Row[Any] | Any | None: Registros obtenidos.

    Raises:
    - DatabaseException: Excepción de recurso no encontrado.
    """

    try:
        # Se convierten los parámetros en tuplas si no lo son.
        froms = _iterable_param(froms)
        joins = _iterable_param(joins)
        options = _iterable_param(options)
        where = _iterable_param(where)
        group_by = _iterable_param(group_by)
        having = _iterable_param(having)
        order = _iterable_param(order)

        # Se obtienen los kwargs.
        limit = kwargs.get('limit', None)
        offset = kwargs.get('offset', None)
        unique = kwargs.get('unique', False)
        scalar = kwargs.get('scalar', True)
        result_list = kwargs.get('result_list', True)
        distinct = kwargs.get('distinct', False)

        # Se crea la consulta inicial con los campos a obtener.
        statement = select(*fields)

        # si existen joins, se añaden a la consulta.
        if joins:
            # recorremos los joins y los añadimos a la consulta.
            for join in joins:
                statement = statement.join(**join)

        # si se ha indicado que se deben obtener registros únicos, se añade la opción.
        if distinct:
            statement = statement.distinct()

        # si se han indicado las tablas, se añaden a la consulta.
        if froms:
            statement = statement.select_from(*froms)
    
        # si se han indicado las opciones, se añaden a la consulta.
        if options:
            statement = statement.options(*options)

        # si se han indicado las condiciones, se añaden a la consulta.
        if where:
            statement = statement.where(*where)

        # si se ha indicado el límite, se añade a la consulta.
        if limit:
            statement = statement.limit(limit)
        
        # si se ha indicado el desplazamiento, se añade a la consulta.
        if offset:
            statement = statement.offset(offset)

        # si se han indicado los campos para agrupar, se añaden a la consulta.
        if group_by:
            statement = statement.group_by(*group_by)

        # si se han indicado las condiciones para filtrar los registros agrupados, se añaden a la consulta.
        if having:
            statement = statement.having(*having)

        # si se han indicado los campos para ordenar, se añaden a la consulta.
        if order:
            statement = statement.order_by(*order)

        # Se ejecuta la consulta.
        result = await session.execute(statement)

        # si se han indicado registros únicos, aplicamos el filtro.
        if unique:
            result = result.unique()

        # si se han indicado registros escalares, aplicamos el filtro.
        if scalar:
            result = result.scalars()

        # si se ha indicado que se deben devolver los registros como una lista, obtenemos todos los registros.
        if result_list:
            records = result.all()

            # si no se han obtenido registros, se lanza una excepción.
            if len(records) < 1:
                _raise_not_found(RESOURCES_NOT_FOUND, resource_type=statement.get_final_froms(), query=statement)

            return records
        
        # si no se ha indicado que se deben devolver los registros como una lista, obtenemos un único registro.
        record = result.one_or_none()

        # si no se ha obtenido un registro, se lanza una excepción.
        if record is None:
            _raise_not_found(RESOURCES_NOT_FOUND, resource_type=statement.get_final_froms(), query=statement)

        return record
    
    except DatabaseException as exc:
        raise exc
    
    except Exception as exc:
        _raise_exception(exc)

async def get_record_by_id(session: AsyncSession, model: Base, record_id: UUID, options: Sequence[ExecutableOption] | ExecutableOption = None) -> Base:
    """
    Obtiene un registro de la base de datos por su id.

    Args:
    - session (AsyncSession): Sesión de base de datos.
    - model (Base): Modelo de la base de datos.
    - record_id (UUID): Id del registro a obtener.
    - options (Sequence, optional): Campos adicionales a cargar. Por defecto ().

    Returns:
    - Base: Registro obtenido.

    Raises:
    - DatabaseException: Si el registro no existe.
    """

    # Se convierte en una tupla si no lo es.
    options = _iterable_param(options)
    
    try:
        # intentamos obtener el registro.
        record = await session.get(model, record_id, options=options)

    except Exception as e:
        # si se produce un error, se lanza una excepción.
        _raise_exception(e)

    # si no se ha obtenido un registro, se lanza una excepción.
    if record is None:
        _raise_not_found(RESOURCE_NOT_FOUND, resource_id=record_id, resource_type=model.__name__)

    return record



async def get_user_by_id(session: AsyncSession, logged_user: User, user_id: UUID, options: Sequence[ExecutableOption] | ExecutableOption = ()) -> User:
    """
    Obtiene un usuario de la base de datos por su id.

    Args:
    - session (AsyncSession): Sesión de base de datos.
    - logged_user (User): Usuario que realiza la petición.
    - user_id (UUID): Id del usuario a obtener.
    - options (Sequence, optional): Campos adicionales a cargar. Por defecto ().
    
    Returns:
    - Base: Registro obtenido.

    Raises:
    - DatabaseException: Si el registro no existe.
    """

    # Si el usuario que realiza la petición es el mismo que el que se quiere obtener, se devuelve el usuario.
    if user_id == logged_user.id:
        await session.refresh(logged_user, ["address"])
        return logged_user

    # devolvemos el resultado de la función get_record_by_id.
    return await get_record_by_id(session, User, user_id, options)