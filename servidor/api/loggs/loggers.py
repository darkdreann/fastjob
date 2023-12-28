import logging.config, logging
from api.loggs.load_config import config_data

# Carga la configuración de logs
logging.config.dictConfig(config_data)

# Se obtienen los loggers de la aplicación
INFO_LOGGER = logging.getLogger("app_info")
ERROR_LOGGER = logging.getLogger("app_error")