import os, logging
from api.utils.constants.error_strings import LOG_FOLDER_CREATE_PERMISSION_DENIED
from api.utils.functions.env_config import CONFIG

# Configuración de los logs
_LOG_INFO_PATH = os.path.join(CONFIG.LOG_PATH, CONFIG.LOG_FOLDER)
_LOG_ERROR_PATH = os.path.join(CONFIG.LOG_PATH, CONFIG.LOG_FOLDER)
_SPACE_BETWEEN_LOGS = "\n" + "-" * 100 + "\n"

try:
    if not os.path.exists(_LOG_INFO_PATH):
        os.makedirs(_LOG_INFO_PATH)
    if not os.path.exists(_LOG_ERROR_PATH):
        os.makedirs(_LOG_ERROR_PATH)
except:
    raise PermissionError(LOG_FOLDER_CREATE_PERMISSION_DENIED)

LOG_INFO_FILE = os.path.join(_LOG_INFO_PATH, CONFIG.LOG_FILE_INFO)
LOG_ERROR_FILE = os.path.join(_LOG_ERROR_PATH, CONFIG.LOG_FILE_ERROR)
FORMATTER = logging.Formatter(f"%(asctime)s - %(name)s - %(levelname)s\n%(message)s{_SPACE_BETWEEN_LOGS}")
