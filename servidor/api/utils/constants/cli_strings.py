############## CREATE ADMIN ##############

# INFO #
CREATE_ADMIN_MSG = """
##### Creación de administrador CLI #####
Introduce los datos del administrador:
"""

INPUT_USERNAME = "Introduzca el nombre de usuario del administrador: "

INPUT_EMAIL = "Introduzca el correo electrónico del administrador: "

INPUT_PASSWORD = "Introduzca la contraseña del administrador: "

INPUT_PASSWORD_CONFIRMATION = "Confirme la contraseña del administrador: "

INPUT_NAME = "Introduzca el nombre del administrador: "

INPUT_SURNAME = "Introduzca los apellidos del administrador: "

INPUT_PHONES = "Introduzca los números de teléfono del administrador(separados por comas): "

INPUT_POSTAL_CODE = "Introduzca el código postal del administrador: "

INPUT_STREET = "Introduzca la calle del administrador: "

INPUT_CITY = "Introduzca la ciudad del administrador: "

INPUT_PROVINCE = "Introduzca la provincia del administrador: "

# ERROR #
EMPTY_USERNAME = "El nombre de usuario no puede estar vacío."

USERNAME_LENGTH_ERROR = "El nombre de usuario debe tener entre {MIN} y {MAX} caracteres."

DUPLICATED_USERNAME = "El nombre de usuario ya existe. Vuelve a intentarlo."

EMAIL_ERROR = "El correo electrónico no es válido."

DUPLICATED_EMAIL = "El correo electrónico ya existe. Vuelve a intentarlo."

PASSWORDS_NOT_MATCH = "Las contraseñas no coinciden. Vuelve a intentarlo."

EMPTY_NAME = "El nombre no puede estar vacío. Vuelve a intentarlo."

EMPTY_SURNAME = "Los apellidos no pueden estar vacíos. Vuelve a intentarlo."

PHONES_ERROR = "Los números de teléfono no son válidos. Vuelve a intentarlo."

POSTAL_CODE_ERROR = "El código postal no es válido. Vuelve a intentarlo."

EMPTY_STREET = "La calle no puede estar vacía. Vuelve a intentarlo."

EMPTY_CITY = "La ciudad no puede estar vacía. Vuelve a intentarlo."

EMPTY_PROVINCE = "La provincia no puede estar vacía. Vuelve a intentarlo."

############## DOCKER BUILD ##############

# INFO #
DOCKER_BUILD_MSG = "##### Creación de contenedor docker #####"

INPUT_DOCKER_TYPE = "Introduzca el tipo de contenedor (dev|prod): "

INPUT_DOCKER_NAME = "Introduzca el nombre del contenedor: "

INPUT_FRESH_BUILD = "¿Desea reconstruir las imágenes? (y/n): "

DOCKER_BUILD_SUCCESS = "El contenedor se ha creado correctamente. Se ha iniciado en segundo plano."

# ERROR #
DOCKER_TYPE_ERROR = "El tipo de contenedor no es válido. Vuelve a intentarlo."

DOCKER_NAME_ERROR = "Introduzca un nombre de contenedor con al menos 4 caracteres o más."

DOCKER_FRESH_BUILD_ERROR = "La opción seleccionada no es válida. Vuelve a intentarlo."

DOCKER_BUILD_FAILED = "No se ha podido crear el contenedor. Vuelve a intentarlo."

############## RUN SERVER ##############

# ERROR #
WINDOWS_NOT_SUPPORTED = "No se puede ejecutar el servidor en un sistema Windows."

############## MANAGE ##############

# ERROR #
MODULE_ERROR = "No se ha podido importar el modulo {module_name} correctamente.\n Compruebe que el modulo esta instalado."

ENV_VARS_ERROR = "No se han encontrado las variables de entorno necesarias para ejecutar el comando.\n{exc}"

NO_ARGS_ERROR = "No se ha proporcionado ningún argumento."

TOO_MANY_ARGS_ERROR = "Se han proporcionado demasiados argumentos."

INVALID_ARG_ERROR = "El argumento proporcionado no es válido: {COMMAND_NAME}"

