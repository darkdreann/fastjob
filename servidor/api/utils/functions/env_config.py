from platform import system
from pydantic_settings import BaseSettings
from api.utils.constants.error_strings import ENV_FILE_NOT_FOUND, ENV_UNEXPECTED_ERROR
from dotenv import load_dotenv

# Valores por defecto en caso de que no se encuentren en el archivo .env
_DEFAULT_FOLDER = "app_folder"
_DEFAULT_FILE_INFO = "app_info.log"
_DEFAULT_FILE_ERROR = "app_error.log"
_DEFAULT_LOG_PATH_WINDOWS = "C:\Windows\System32\LogFiles\\"
_DEFAULT_LOG_PATH_LINUX = "/var/log/"
_DEFAULT_LOG_PATH = _DEFAULT_LOG_PATH_WINDOWS if system() == "Windows" else _DEFAULT_LOG_PATH_LINUX
_DEFAULT_TOKEN_EXPIRE_MINUTES = 30
_DEFAULT_TOKEN_URL = "/token"
_DEFAULT_ALGORITHM = "HS256"
_DEFAULT_PASSWORD_CRYPT_SCHEME = "bcrypt"
_DEFAULT_TOKEN_TYPE = "bearer"
_DEFAULT_POOL_SIZE = 5
_DEFAULT_MAX_OVERFLOW = 5
_DEFAULT_DEV = "False"


class _Settings(BaseSettings):
    DEVELOPMENT: bool = _DEFAULT_DEV
    LOG_FOLDER: str = _DEFAULT_FOLDER
    LOG_FILE_INFO: str = _DEFAULT_FILE_INFO
    LOG_FILE_ERROR: str = _DEFAULT_FILE_ERROR
    LOG_PATH: str = _DEFAULT_LOG_PATH
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_EMAIL: str
    SMTP_PASSWORD: str 
    EMAIL_TO_SEND: str
    SUBJECT: str
    DATABASE_IP: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DEVELOPMENT_DATABASE_NAME: str
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

try:
    load_dotenv()
    CONFIG = _Settings()

except FileNotFoundError:
    raise FileNotFoundError(ENV_FILE_NOT_FOUND)

except Exception as exc:
    raise Exception(ENV_UNEXPECTED_ERROR.format(exc=exc))