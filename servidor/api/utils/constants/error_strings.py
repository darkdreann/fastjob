DATABASE_ERROR = "Error: Algo ha fallado en la base de datos: {exc}."

DATABASE_CREATION_ERROR = "Error: Falló la creación de la base de datos.\n {exc}"	

UNKNOWN_QUERY_ERROR = "Error: Algo salió mal en la consulta:\n {exc}"

RESOURCE_NOT_FOUND = "Error: Recurso {resource_id} tipo {resource_type} solicitado no encontrado"

RESOURCES_NOT_FOUND = "Error: Recursos tipo {resource_type} no encontrados en la consulta:\n {query}"

PERMISSION_USER_NOT_FOUND = "Error: Permiso denegado, usuario no encontrado"

PERMISSION_DENIED = "Error: Permiso denegado, usuario {user_id} no tiene acceso al recurso {resource}"

INVALID_TOKEN = "Error: Token inválido proporcionado:\n {exc}"

INVALID_CREDENTIALS = "Error: No se pudieron validar las credenciales para {username}"

LOG_FOLDER_CREATE_PERMISSION_DENIED = "Error: Permiso denegado para crear la carpeta de logs"

LOG_CONFIG_FILE_ERROR = "Error: Algo salió mal al leer el archivo de configuración de registro:\n {exc}"

LOG_FORMAT_ERROR = "Error: No se puede formatear el mensaje de registro:\n {exc}"

ERROR_RESPONSE_UNEXPECTED_ERROR = "Error: Algo salió mal. Por favor, inténtelo de nuevo más tarde."

SECTOR_GET_PARAMS = "No se pueden usar los parámetros category_name y only_categories al mismo tiempo."

INVALID_EXTRA_FIELDS = "Error: Parámetros de campos adicionales no válidos:\n {field}"

INVALID_CANDIDATE_DIR_PARAMS = "Error: No se pueden usar los parámetros postal_code y province al mismo tiempo."

INVALID_CANDIDATE_SECTOR_PARAMS = "Error: No se pueden usar los parámetros sector_category y sector_id al mismo tiempo."

INVALID_CANDIDATE_LANGUAGE_PARAMS = "Error: No se pueden usar el parámetro language_level sin el parámetro language."

INVALID_EDUCATION_PARAMS = "Error: No se pueden usar los parámetros name con los parámetros level y sector."

INVALID_EDUCATION_PARAMS_FOR_JOBS = "Error: No se puede usar el parámetro name con el parámetro level."

INVALID_CONTENT_TYPE = "Error: Tipo de contenido no válido. URL: {url}"

INVALID_FILE_TYPE = "Error: Tipo de archivo no válido. El archivo debe ser un PDF."

SCHEDULER_ERROR = "Error: Algo salió mal en el planificador de tareas:\n {exc}"

# MENSAJES DE MANEJADORES DE EXCEPCIONES
LOG_INVALID_PARAMS = """
Parámetros inválidos:
  params: {params},
  Solicitud:
    url: {url},
    método: {method}"""

LOG_UNEXPECTED_ERROR = """
Error: {exc},
Solicitud:
  url: {url},
  método: {method}"""
