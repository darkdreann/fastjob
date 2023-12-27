from platform import system
from typing import Self, Any
from uvicorn import run
from api.utils.functions.env_config import CONFIG
from api.main import app

# Determina si el sistema operativo es Windows
_IS_WINDOWS = system() == "Windows"

# Si el sistema operativo no es Windows, importa la clase BaseApplication de Gunicorn, los UvicornWorker y crea una clase App para iniciar el servidor
if not _IS_WINDOWS:
    from gunicorn.app.base import BaseApplication
    from uvicorn.workers import UvicornWorker

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
                self.cfg.set(key.lower(), value)

        def load(self) -> Any:
            """
            Carga la aplicación del servidor y la devuelve.

            Returns:
                application: La aplicación del servidor.
            """
            return self.application
        
def _run_windows_server() -> None:
    """
    Ejecuta el servidor en el sistema operativo Windows.
    """
    import api.main

    module_name = api.main.__name__
    app_var_name = f"{app=}".split("=")[0]

    app_server = f"{module_name}:{app_var_name}"

    run(
        app=app_server,
        host=CONFIG.SERVER_IP,
        port=CONFIG.SERVER_PORT,
        workers=CONFIG.SERVER_WORKERS
    )

def _run_linux_server() -> None:
    """
    Ejecuta el servidor en un entorno Linux.
    """
    BIND = f"{CONFIG.SERVER_IP}:{CONFIG.SERVER_PORT}"

    options = {
        'bind': BIND,
        'workers': CONFIG.SERVER_WORKERS,
        'worker_class': UvicornWorker,
    }

    _App(app, options).run()

def run_server() -> None:
    """
    Inicia el servidor de la aplicación.

    Este método configura y ejecuta el servidor de la aplicación utilizando la dirección IP y el puerto
    especificados en la configuración. También se especifica el número de trabajadores y la clase de
    trabajador utilizada por el servidor.
    """

    # Si el sistema operativo es Windows, ejecuta el servidor utilizando el método run_windows_server
    if _IS_WINDOWS:
        _run_windows_server()
    # Si el sistema operativo no es Windows, ejecuta el servidor utilizando la clase App y el método run
    else:
        _run_linux_server()

    