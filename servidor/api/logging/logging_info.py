import logging
from api.logging.logging_config import LOG_INFO_FILE, FORMATTER

INFO_LOGGER = logging.getLogger(__name__)

# Configurar nivel de registro
INFO_LOGGER.setLevel(logging.INFO)

# Configurar manejador de registro
INFO_HANDLER = logging.FileHandler(LOG_INFO_FILE)
INFO_HANDLER.setLevel(logging.INFO)

INFO_HANDLER.setFormatter(FORMATTER)

INFO_LOGGER.addHandler(INFO_HANDLER)