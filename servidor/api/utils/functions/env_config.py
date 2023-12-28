import os
from pydantic import model_validator
from pydantic_settings import BaseSettings

# Valores por defecto en caso de que no se encuentren en el archivo .env
_DEFAULT_TOKEN_EXPIRE_MINUTES = 30
_DEFAULT_TOKEN_URL = "/token"
_DEFAULT_ALGORITHM = "HS256"
_DEFAULT_PASSWORD_CRYPT_SCHEME = "bcrypt"
_DEFAULT_TOKEN_TYPE = "bearer"
_DEFAULT_POOL_SIZE = 1
_DEFAULT_MAX_OVERFLOW = 0
_DEFAULT__TEST_DATA_JSON_PATH = "test_data.json"
_DEFAULT_SERVER_IP = "localhost"
_DEFAULT_SERVER_PORT = 8000
_DEFAULT_SERVER_WORKERS = 1
_DEFAULT_LOGGING_CONFIG_FILE = "logging_config.yml"

class _Settings(BaseSettings):
    """
    Clase que define la configuración de variables de entorno para la aplicación.
    """
    
    DEVELOPMENT: bool
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
    POOL_SIZE: int = _DEFAULT_POOL_SIZE
    MAX_OVERFLOW: int = _DEFAULT_MAX_OVERFLOW
    ACCESS_TOKEN_EXPIRE_MINUTES: int = _DEFAULT_TOKEN_EXPIRE_MINUTES
    TOKEN_URL: str = _DEFAULT_TOKEN_URL
    ALGORITHM: str = _DEFAULT_ALGORITHM
    TOKEN_TYPE: str = _DEFAULT_TOKEN_TYPE
    PASSWORD_CRYPT_SCHEME: str = _DEFAULT_PASSWORD_CRYPT_SCHEME
    SECRET_KEY: str
    TEST_DATA_JSON_PATH: str = _DEFAULT__TEST_DATA_JSON_PATH
    SERVER_IP: str = _DEFAULT_SERVER_IP
    SERVER_PORT: int = _DEFAULT_SERVER_PORT
    SERVER_WORKERS: int = _DEFAULT_SERVER_WORKERS
    LOGS_PATH: str
    APP_LOG_FOLDER: str
    LOG_FILE_INFO: str
    LOG_FILE_ERROR: str
    APP_LOGGING_CONFIG_FILE: str = _DEFAULT_LOGGING_CONFIG_FILE
    CONFIG_FILE_PATH: str
    GUNICORN_LOG_LEVEL: str | None = None
    GUNICORN_LOG_FOLDER: str | None = None
    GUNICORN_ACCESS_LOG: str | None = None
    GUNICORN_ERROR_LOG: str | None = None

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
        # ruta de la carpeta de logs de Gunicorn
        self.GUNICORN_LOG_FOLDER = os.path.join(self.LOGS_PATH, self.GUNICORN_LOG_FOLDER)
        # ruta de los archivos de logs de Gunicorn
        self.GUNICORN_ACCESS_LOG = os.path.join(self.GUNICORN_LOG_FOLDER, self.GUNICORN_ACCESS_LOG)
        self.GUNICORN_ERROR_LOG = os.path.join(self.GUNICORN_LOG_FOLDER, self.GUNICORN_ERROR_LOG)
        # ruta del archivo de configuración de logs de la aplicación
        self.APP_LOGGING_CONFIG_FILE = f"{self.CONFIG_FILE_PATH}/{self.APP_LOGGING_CONFIG_FILE}"

        return self

# Crea una instancia de la clase _Settings
CONFIG = _Settings()

