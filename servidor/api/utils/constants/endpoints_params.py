from fastapi import Query, Path

LIMIT = Query(description="Limite de registros devueltos.", gt=0)

DEFAULT_LIMIT = 20

OFFSET = Query(description="Permite omitir un número específico de registros en el conjunto de resultados", ge=0)

DEFAULT_OFFSET = 0

USER_ID = Path(description="El id del usuario.")

SECTOR_CATEGORY = Query(description="La categoría del sector. Para obtener todas sus subcategorías. No se puede usar con el parámetro 'only_category'.")

ONLY_CATEGORY = Query(description="Si se quiere obtener solo la categoría del sector. No se puede usar con el parámetro 'category'.")

SECTOR_ID = Path(description="El id del sector.")

SECTOR_EXTRA_FIELD = Query(description="Campos de las relaciones de la tabla sector que se quieren obtener. Se pueden especificar varios.")

ADRESS_ID = Path(description="El id de la dirección.")

ADRESS_POSTAL_CODE = Path(..., description="El código postal de la dirección. Debe ser un número de 5 dígitos.", ge=10000, le=99999)

ADRESS_EXTRA_FIELD = Query(description="Campos de las relaciones de la tabla adress que se quieren obtener. Se pueden especificar varios.")

EDUCATION_ID = Path(description="El id de la formación.")

EDUCATION_LEVEL_ID = Path(description="El id del nivel de formación.")

EDUCATION_LEVEL_EXTRA_FIELD = Query(description="Campos de las relaciones de la tabla education que se quieren obtener. Se pueden especificar varios.")

LANGUAGE_ID = Path(description="El id del idioma.")

LANGUAGE_LEVEL_ID = Path(description="El id del nivel de idioma.")

LANGUAGE_LEVEL_EXTRA_FIELD = Query(description="Campos de las relaciones de la tabla language_level que se quieren obtener. Se pueden especificar varios.")

LANGUAGE_EXTRA_FIELD = Query(description="Campos de las relaciones de la tabla language que se quieren obtener. Se pueden especificar varios.")

