from fastapi import Query, Path

LIMIT = Query(description="Limite de registros devueltos.", gt=0)

OFFSET = Query(description="Permite omitir un número específico de registros en el conjunto de resultados", ge=0)

USER_ID = Path(description="El id del usuario.")

