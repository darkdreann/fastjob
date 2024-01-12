from typing import Callable, Self
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from api.utils.constants.error_strings import SCHEDULER_ERROR
from api.utils.functions.management_utils import print_log, LogLevel

class AsyncSchedulerManager:
    """Manejador de tareas programadas."""
    
    _instance: AsyncIOScheduler = AsyncIOScheduler()

    @staticmethod
    def _try_function(func: Callable) -> Callable:
        """Función de prueba."""

        # envolvemos la función en un try-except
        async def wrapper(*args, **kwargs):
            """Función envoltorio."""

            try:
                print("asdadasdfsafasfa")
                await func(*args, **kwargs)
            except Exception as exc:
                print_log(SCHEDULER_ERROR, LogLevel.ERROR, exc=exc)

        # devolvemos la función envoltorio
        return wrapper

    
    @classmethod
    def add_job(cls, func: Callable, *args, **kwargs) -> None:
        """
        Añade una tarea programada.

        Args:
        - func: Función a ejecutar (Callable).
        - args: Argumentos de la función (tuple).
        - kwargs: Argumentos de la función (dict).
        """

        func_with_try = cls._try_function(func)

        cls._instance.add_job(func_with_try, *args, **kwargs)

    @classmethod
    def start(cls) -> None:
        """Inicia el manejador de tareas programadas."""

        cls._instance.start()

    @classmethod
    def shutdown(cls) -> None:
        """Detiene el manejador de tareas programadas."""

        cls._instance.shutdown()
