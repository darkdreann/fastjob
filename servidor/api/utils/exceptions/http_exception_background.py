from starlette.exceptions import HTTPException

class HTTPExceptionWithBackgroundTask(HTTPException):
    """Clase que extiende la clase HTTPException de Starlette que permite añadirle una tarea en segundo plano."""
    
    def __init__(self, *args, **kwargs):
        """Constructor de la clase HTTPExceptionWithBackgroundTask.
        
            Args:
                *args: Argumentos de la clase HTTPException de Starlette.
                **kwargs: Argumentos de la clase HTTPException de Starlette."""
        
        self.background = kwargs.pop("background", None)
        super().__init__(*args, **kwargs)
        