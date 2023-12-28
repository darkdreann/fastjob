
import os, platform
from typing import Self, Any
from api.main import app
from api.utils.constants.error_strings import LOG_FOLDER_CREATE_PERMISSION_DENIED
from api.utils.functions.env_config import CONFIG
from api.utils.constants.cli_strings import WINDOWS_NOT_SUPPORTED

# Se comprueba si el sistema operativo es Windows
_IS_WINDOWS = platform.system() == "Windows"

# Si el sistema operativo no es Windows, se importa la clase FastAPIApplication
if not _IS_WINDOWS:
    from gunicorn.app.base import BaseApplication

    class _App(BaseApplication):
        """
        Clase que representa la aplicación del servidor.
        """

        def __init__(self, app, options=None) -> Self:
            """
            Inicializa una instancia de la clase App.

            Args:
            - app (FastAPI): La aplicación del servidor.
            - options (dict, opcional): Diccionario con las opciones de configuración del servidor.

            Returns:
            - Self: Una instancia de la clase App.
            """
            try:
                # Se crea la carpeta de logs de Gunicorn si no existe
                if not os.path.exists(CONFIG.GUNICORN_LOG_FOLDER):
                    os.makedirs(CONFIG.GUNICORN_LOG_FOLDER)
            except:
                # Si no se puede crear la carpeta de logs, se lanza una excepción
                raise PermissionError(LOG_FOLDER_CREATE_PERMISSION_DENIED)

            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self) -> None:
            """
            Carga la configuración del servidor a partir de las opciones proporcionadas.
            Solo se cargan las opciones que están presentes en la configuración del servidor
            y que tienen un valor no nulo.
            """
            config = {key: value for key, value in self.options.items()
                        if key in self.cfg.settings and value is not None}
            for key, value in config.items():
                self.cfg.set(key, value)

        def load(self) -> Any:
            """
            Carga la aplicación del servidor y la devuelve.

            Returns:
                application: La aplicación del servidor.
            """
            return self.application


def run_server() -> None:
    """
    Inicia el servidor de la aplicación.

    Este método configura y ejecuta el servidor de la aplicación utilizando la dirección IP y el puerto
    especificados en la configuración. También se especifica el número de trabajadores y la clase de
    trabajador utilizada por el servidor.
    """

    # Si el sistema operativo es Windows, se lanza una excepción ya que no se puede ejecutar el servidor en Windows
    if _IS_WINDOWS:
        raise NotImplementedError(WINDOWS_NOT_SUPPORTED)

    BIND = f"{CONFIG.SERVER_IP}:{CONFIG.SERVER_PORT}"

    options = {
        'bind': BIND,
        'workers': CONFIG.SERVER_WORKERS,
        'worker_class': "uvicorn.workers.UvicornWorker",
        'accesslog': CONFIG.GUNICORN_ACCESS_LOG,
        'errorlog': CONFIG.GUNICORN_ERROR_LOG,
        'loglevel': CONFIG.GUNICORN_LOG_LEVEL
    }

    _App(app, options).run()