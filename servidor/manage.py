import importlib
from sys import argv
from asyncio import run
from pydantic_core import ValidationError
from inspect import iscoroutinefunction
from api.utils.constants.cli_strings import NO_ARGS_ERROR, TOO_MANY_ARGS_ERROR, INVALID_ARG_ERROR, MODULE_ERROR, ENV_VARS_ERROR

AVAILABLE_COMMANDS = {
    "runserver": {
        "import": "api.utils.functions.run_server.run_server",
        "function": "run_server"
    },
    "createadmin": {
        "import": "api.utils.functions.create_admin.NewAdmin",
        "function": "NewAdmin"
    },
    "dockerbuild": {
        "import": "api.utils.functions.docker_build",
        "function": "docker_build"
    }
}

async def execute_command(command: dict) -> None:
    """
    Ejecuta un comando dado.

    Args:
    - command (dict): Diccionario con la información del comando a ejecutar.
    """
    try:
        # Se importa el módulo correspondiente al comando a ejecutar para evitar errores de importación al ejecutar comandos que no necesitan ciertos módulos(por ejemplo el modulo de env_config no es necesario para ejecutar el comando dockerbuild)
        module = importlib.import_module(command["import"])
    except ModuleNotFoundError as exc:
        # Si ocurre un error importando el módulo, se muestra un mensaje de error
        raise Exception(MODULE_ERROR.format(module_name=exc.name))
    except ValidationError as exc:
        # Si ocurre un error importando el módulo, se muestra un mensaje de error
        raise Exception(ENV_VARS_ERROR.format(exc=exc))

    # Se obtiene la función correspondiente al comando
    func = getattr(module, command["function"])

    # Se comprueba si la función es asíncrona, si lo es, se ejecuta con await
    if iscoroutinefunction(func):
        return await func()
    # Si no es asíncrona, se ejecuta normalmente
    return func()

async def main() -> None:
    """
    Función principal del programa.
    Ejecuta un comando proporcionado como argumento de línea de comandos.

    Raises:
    - ValueError: Si no se proporciona ningún argumento o si se proporcionan demasiados.
    - ValueError: Si el argumento proporcionado no es válido.
    """
    # Se comprueba que se haya proporcionado un argumento
    if len(argv) < 2:
        raise ValueError(NO_ARGS_ERROR)
    
    # Se comprueba que no se hayan proporcionado demasiados argumentos
    if len(argv) > 2:
        raise ValueError(TOO_MANY_ARGS_ERROR)
    
    # obtenemos el argumento
    COMMAND_NAME = argv[1]
    
    # Se comprueba que el argumento esté en la lista de comandos
    if COMMAND_NAME not in AVAILABLE_COMMANDS:
        raise ValueError(INVALID_ARG_ERROR.format(COMMAND_NAME=COMMAND_NAME))
    
    # Se obtiene la función correspondiente al comando
    COMMAND = AVAILABLE_COMMANDS[COMMAND_NAME]

    # se ejecuta la función
    await execute_command(COMMAND)
    
if __name__ == "__main__":
    run(main())