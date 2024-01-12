from subprocess import Popen
from api.utils.constants.cli_strings import DOCKER_BUILD_MSG, INPUT_DOCKER_TYPE, INPUT_DOCKER_NAME, INPUT_FRESH_BUILD, DOCKER_BUILD_SUCCESS
from api.utils.constants.cli_strings import DOCKER_TYPE_ERROR, DOCKER_NAME_ERROR, DOCKER_FRESH_BUILD_ERROR, DOCKER_BUILD_FAILED

_TYPE = {
    "dev": {
            "docker_compose":"docker-compose.dev.yml",
            "env_file": ".env.dev"
        },
    "prod": {
            "docker_compose":"docker-compose.yml",
            "env_file": ".env"
        },
}

def _docker_build_input(text: str) -> str | None:
    """
    Pregunta al usuario si desea realizar una construcción de Docker.

    Args:
    - text (str): El texto de la pregunta a mostrar al usuario.

    Retorna:
    - str | None: La opción seleccionada por el usuario. Si el usuario selecciona "y", retorna "--build". Si el usuario selecciona "n", retorna una cadena vacía. Si el usuario ingresa una opción inválida, retorna None.
    """
    # Se obtiene la respuesta del usuario
    text = input(text).lower()

    # Si la respuesta no es "y" o "n", se retorna None
    if text not in ["y", "n"]:
        return None

    # Si la respuesta es "y", se retorna "--build" sino se retorna una cadena vacía
    if text == "y":
        return "--build"
    return ""

def docker_build() -> None:
    """
    Crea un contenedor Docker con docker-compose utilizando los argumentos proporcionados por el usuario.
    """
    
    print(DOCKER_BUILD_MSG)

    # Se obtiene el tipo de contenedor mientras no sea válido
    while (tipo_docker := input(INPUT_DOCKER_TYPE).lower()) not in _TYPE:
        print(DOCKER_TYPE_ERROR)

    # Se obtiene el nombre del contenedor mientras no sea válido
    while (nombre_contenedor := input(INPUT_DOCKER_NAME)) == "" and len(nombre_contenedor) < 4:
        print(DOCKER_NAME_ERROR)

    # Se obtiene la opción de reconstruir las imágenes mientras no sea válida
    while (fresh_build := _docker_build_input(INPUT_FRESH_BUILD)) is None:
        print(DOCKER_FRESH_BUILD_ERROR)

    # Se ejecuta el comando docker-compose up con los argumentos correspondientes elegidos por el usuario
    process = Popen(["docker-compose", "-f", f"{_TYPE[tipo_docker]['docker_compose']}", "--env-file", f"{_TYPE[tipo_docker]['env_file']}", "-p", nombre_contenedor, "up", fresh_build, "-d"])

    # Espera a que termine el proceso
    process.communicate()

    if process.returncode != 0:
        return print(DOCKER_BUILD_FAILED)

    print(DOCKER_BUILD_SUCCESS)

    


    
