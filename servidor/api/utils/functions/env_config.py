import os
from pydantic import model_validator
from pydantic_core import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

# Valores por defecto en caso de que no se encuentren en el archivo .env
_DEFAULT_DEV = False

class _Settings(BaseSettings):
    """
    Clase que define la configuración de variables de entorno para la aplicación.
    """
    model_config = SettingsConfigDict(env_file_encoding='utf-8', extra='ignore')
    
    DEVELOPMENT: bool = _DEFAULT_DEV
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_EMAIL: str
    SMTP_PASSWORD: str 
    EMAIL_TO_SEND: str
    SUBJECT: str
    DATABASE_IP: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    POOL_SIZE: int
    MAX_OVERFLOW: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    TOKEN_URL: str
    ALGORITHM: str
    TOKEN_TYPE: str
    PASSWORD_CRYPT_SCHEME: str
    SECRET_KEY: str
    TEST_DATA_JSON_PATH: str | None = None
    SERVER_IP: str | None = None
    SERVER_PORT: int | None = None
    SERVER_WORKERS: int | None = None
    LOGS_PATH: str
    APP_LOG_FOLDER: str
    LOG_FILE_INFO: str
    LOG_FILE_ERROR: str
    APP_LOGGING_CONFIG_FILE: str
    CONFIG_FILE_PATH: str
    GUNICORN_LOG_LEVEL: str | None = None
    GUNICORN_LOG_FOLDER: str | None = None
    GUNICORN_ACCESS_LOG: str | None = None
    GUNICORN_ERROR_LOG: str | None = None
    SCHEDULER_INTERVAL: int = 10

    @model_validator(mode='after')
    def log_path(self):
        """
        Cambia el valor de las variables de entorno que contienen rutas para que contengan la ruta completa.
        """
        
        # ruta donde se guardan todos los logs
        self.LOGS_PATH = f"/{self.LOGS_PATH}"

        # ruta de la carpeta de logs de la aplicación
        self.APP_LOG_FOLDER = os.path.join(self.LOGS_PATH, self.APP_LOG_FOLDER)
        # ruta de los archivos de logs de la aplicación
        self.LOG_FILE_INFO = os.path.join(self.APP_LOG_FOLDER, self.LOG_FILE_INFO)
        self.LOG_FILE_ERROR = os.path.join(self.APP_LOG_FOLDER, self.LOG_FILE_ERROR)

        # ruta del archivo de configuración de logs de la aplicación
        self.APP_LOGGING_CONFIG_FILE = f"{self.CONFIG_FILE_PATH}/{self.APP_LOGGING_CONFIG_FILE}"

        # si estamos en desarrollo no se cambian las rutas de los logs de Gunicorn ya que no se usan
        if self.DEVELOPMENT:
            return self
        
        # ruta de la carpeta de logs de Gunicorn
        self.GUNICORN_LOG_FOLDER = os.path.join(self.LOGS_PATH, self.GUNICORN_LOG_FOLDER)
        # ruta de los archivos de logs de Gunicorn
        self.GUNICORN_ACCESS_LOG = os.path.join(self.GUNICORN_LOG_FOLDER, self.GUNICORN_ACCESS_LOG)
        self.GUNICORN_ERROR_LOG = os.path.join(self.GUNICORN_LOG_FOLDER, self.GUNICORN_ERROR_LOG)
        
        

        return self

try:
    # Crea una instancia de la clase _Settings
    CONFIG = _Settings()

 # Si no se pueden cargar las variables de entorno se crea una instancia de la clase _Settings usando el archivo .env
except ValidationError:
    # Se comprueba si se está en desarrollo
    DEV = bool(os.getenv("DEVELOPMENT", _DEFAULT_DEV))
    # Si se está en desarrollo se usa el archivo .env.dev, si no se usa el archivo .env
    ENV_FILE = ".env" if not DEV else ".env.dev"
    # Se crea la instancia de la clase _Settings
    CONFIG = _Settings(_env_file=ENV_FILE)

