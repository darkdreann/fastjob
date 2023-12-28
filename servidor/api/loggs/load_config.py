import os, yaml, re
from api.utils.constants.error_strings import LOG_FOLDER_CREATE_PERMISSION_DENIED, LOG_CONFIG_FILE_ERROR
from api.utils.functions.env_config import CONFIG

def env_var_constructor(loader, node):
    """
    Constructor de variables de entorno.

    Carga el valor de una variable de entorno especificada en el nodo YAML.

    Args:
    - loader (YAMLLoader): El cargador YAML.
    - node (Node): El nodo YAML que contiene el nombre de la variable de entorno.

    Returns:
    - str: El valor de la variable de entorno o una cadena vacía si no está definida.
    """
    # Se obtiene el nombre de la variable de entorno
    value = loader.construct_scalar(node)
    # Se obtiene el valor de la variable de entorno y se devuelve
    return getattr(CONFIG, value[2:-1])

try:
    # Se crea la carpeta de logs si no existe
    if not os.path.exists(CONFIG.APP_LOG_FOLDER):
        os.makedirs(CONFIG.APP_LOG_FOLDER)
except:
    # Si no se puede crear la carpeta de logs, se lanza una excepción
    raise PermissionError(LOG_FOLDER_CREATE_PERMISSION_DENIED)

try:
    YAML_ENV_REGEX = r'\$\{[^}]+\}'

    # Se añade el constructor de variables de entorno al cargador YAML
    yaml.SafeLoader.add_implicit_resolver('!env_var', re.compile(YAML_ENV_REGEX), None)
    yaml.SafeLoader.add_constructor('!env_var', env_var_constructor)

    # Se carga el archivo de configuración de logs
    with open(CONFIG.APP_LOGGING_CONFIG_FILE, 'r') as config_file:
        config_data = yaml.safe_load(config_file)

except Exception as exc:
    # Si se produce un error al cargar el archivo de configuración de logs, se lanza una excepción
    raise Exception(LOG_CONFIG_FILE_ERROR.format(exc=exc))

