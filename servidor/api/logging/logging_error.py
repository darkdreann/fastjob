import logging
from api.logging.logging_config import LOG_ERROR_FILE, FORMATTER
from api.logging.handler_critical import EMAIL_HANDLER

ERROR_LOGGER = logging.getLogger(__name__)

# Configurar nivel de registro
ERROR_LOGGER.setLevel(logging.WARNING)

# Configurar manejador de registro
ERROR_HANDLER = logging.FileHandler(LOG_ERROR_FILE)
ERROR_HANDLER.setLevel(logging.WARNING)

ERROR_HANDLER.setFormatter(FORMATTER)

ERROR_LOGGER.addHandler(ERROR_HANDLER)
#ERROR_LOGGER.addHandler(EMAIL_HANDLER)

#ERROR DEBUG HANDLER (PARA DEBUGEAR)
ERROR_DEBUG_HANDLER = logging.StreamHandler()
ERROR_DEBUG_HANDLER.setLevel(logging.ERROR)

ERROR_DEBUG_HANDLER.setFormatter(FORMATTER)

ERROR_LOGGER.addHandler(ERROR_DEBUG_HANDLER)