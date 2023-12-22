from typing import Self
from starlette.exceptions import HTTPException
from starlette.background import BackgroundTask
from api.utils.constants.http_exceptions import DEFAULT_EXCEPTION

class HTTPExceptionWithBackgroundTask(HTTPException):
    """Clase que extiende la clase HTTPException de Starlette y permite añadirle una tarea en segundo plano."""
    
    def __init__(self, *args, **kwargs) -> Self:
        """
        Constructor de la clase HTTPExceptionWithBackgroundTask.
        
        Args:
        - args: Argumentos de la clase HTTPException de Starlette.
        - kwargs: Argumentos de la clase HTTPException de Starlette.
            
        Returns:
        - Self: Instancia de la clase HTTPExceptionWithBackgroundTask.
        """

        # Si no se ha especificado el código de estado, se usa el código de estado por defecto
        if "status_code" not in kwargs:
            kwargs["status_code"] = DEFAULT_EXCEPTION["status_code"]

        # Si no se ha especificado el mensaje de error, se usa el mensaje de error por defecto
        if "detail" not in kwargs:
            kwargs["detail"] = DEFAULT_EXCEPTION["detail"]
        
        self.background_task = kwargs.pop("background_task", None)
        super().__init__(*args, **kwargs)


class DatabaseException(Exception):
    """Excepción que se lanza cuando ocurre un error interactuando con la base de datos."""
    
    def __init__(self, error_message: str, http_response: dict, background_task: BackgroundTask) -> Self:
        """Constructor de la clase DatabaseException.
        
        Args:
        - error_message: Mensaje de error.
        - http_response: Respuesta HTTP.
        - background_task: Tarea en segundo plano.
            
        Returns:
        - Self: Instancia de la clase DatabaseException.
        """

        self.error_message = error_message
        self.http_response = http_response
        self.background_task = background_task

    def __repr__(self) -> str:
            """
            Devuelve una representación en cadena del objeto.
            
            Returns:
            - str: La representación en cadena del objeto.
            """
            return self.error_message
    

class ResourceNotFoundException(DatabaseException):
    """Excepción que se lanza cuando no se encuentra un recurso en la base de datos."""

class RequestContentTypeError(Exception):
    """Excepción que se lanza cuando el tipo de contenido de un archivo no es el correcto."""

    def __init__(self, error_message) -> Self:
            """
            Inicializa una nueva instancia de la clase Exception personalizada.

            Args:
            - error_message (str): Mensaje de error asociado a la excepción.

            Returns:
            - Self: Instancia de la clase RequestContentTypeError.
            """
            self.error_message = error_message

    def __repr__(self) -> str:
            """
            Devuelve una representación en cadena del objeto.

            Returns:
            - str: La representación en cadena del objeto.
            """
            return self.error_message
