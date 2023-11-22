from typing import Self
from starlette.exceptions import HTTPException
from starlette.background import BackgroundTask

class HTTPExceptionWithBackgroundTask(HTTPException):
    """Clase que extiende la clase HTTPException de Starlette que permite añadirle una tarea en segundo plano."""
    
    def __init__(self, *args, **kwargs) -> Self:
        """Constructor de la clase HTTPExceptionWithBackgroundTask.
        
        Args:
            *args: Argumentos de la clase HTTPException de Starlette.
            **kwargs: Argumentos de la clase HTTPException de Starlette.
            
        Returns:
            Self: Instancia de la clase HTTPExceptionWithBackgroundTask.
        """
        
        self.background = kwargs.pop("background", None)
        super().__init__(*args, **kwargs)


class DatabaseException(Exception):
    """Excepción que se lanza cuando ocurre un error interactuando con la base de datos."""
    
    def __init__(self, error_message: str, http_response: dict, background_task: BackgroundTask) -> Self:
        """Constructor de la clase DatabaseException.
        
        Args:
            error_message: Mensaje de error.
            http_response: Respuesta HTTP.
            background_task: Tarea en segundo plano.
            
        Returns:
            Self: Instancia de la clase DatabaseException.
        """

        self.error_message = error_message
        self.http_response = http_response
        self.background_task = background_task

    def __repr__(self) -> str:
        return self.error_message
    

class ResourceNotFoundException(DatabaseException):
    """Excepción que se lanza cuando no se encuentra un recurso en la base de datos."""