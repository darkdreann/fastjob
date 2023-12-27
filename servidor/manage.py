from sys import argv
from asyncio import run
from inspect import iscoroutinefunction
from api.utils.functions.run_server import run_server
from api.utils.functions.create_admin import NewAdmin

COMMANDS = {
    "runserver": run_server,
    "createadmin": NewAdmin.create_admin
}

async def main():
    if len(argv) < 2:
        raise ValueError("Faltan argumentos")
    
    if len(argv) > 2:
        raise ValueError("Demasiados argumentos")
    
    COMMAND = argv[1]
    
    if COMMAND not in COMMANDS:
        raise ValueError(f"Argumento no válido: {COMMAND}")
    
    func = COMMANDS[COMMAND]

    await func() if iscoroutinefunction(func) else func()
    
if __name__ == "__main__":
    run(main())