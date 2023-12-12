from fastapi import Query, Path, File

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

ADRESS_POSTAL_CODE = Path(description="El código postal de la dirección. Debe ser un número de 5 dígitos.", ge=10000, le=99999)

ADRESS_POSTAL_CODE_QUERY = Query(description="El código postal de la dirección. Debe ser un número de 5 dígitos.", ge=10000, le=99999)

ADRESS_PROVINCE = Query(description="La provincia de la dirección.")

ADRESS_EXTRA_FIELD = Query(description="Campos de las relaciones de la tabla address que se quieren obtener. Se pueden especificar varios.")

EDUCATION_ID = Path(description="El id de la formación.")

EDUCATION_LEVEL_ID = Path(description="El id del nivel de formación.")

GET_EDUCATION = Query(description="Si se quiere obtener las formaciones.")

EDUCATION_EXTRA_FIELD = Query(description="Campos de las relaciones de la tabla education que se quieren obtener. Se pueden especificar varios.")

EDUCATION_NAME_PARAM = Query(description="El nombre de la formación.")

EDUCATION_LEVEL_PARAM = Query(description="El nivel de la formación. Debe ser un número mayor a 0.", ge=0)

LANGUAGE_ID = Path(description="El id del idioma.")

LANGUAGE_LEVEL_ID = Path(description="El id del nivel de idioma.")

LANGUAGE_LEVEL_EXTRA_FIELD = Query(description="Campos de las relaciones de la tabla language_level que se quieren obtener. Se pueden especificar varios.")

LANGUAGE_EXTRA_FIELD = Query(description="Campos de las relaciones de la tabla language que se quieren obtener. Se pueden especificar varios.")

LANGUAGE_CANDIDATE = Query(description="El id o el nombre del idioma que debe tener el candidato.")

LANGUAGE_LEVEL_VALUE = Query(description="El valor del nivel de idioma. Debe ser un número mayor a 0.", ge=0)

EXPERIENCE_MONTHS = Query(description="Los meses de experiencia del candidato. Debe ser un número.")

EXPERIENCE_ID = Path(description="El id de la experiencia.")

RESOURCE_SECTOR = Query(description="El sector del recurso del candidato. Puede ser el id o la categoría del sector.")

CANDIDATE_EXTRA_FIELD = Query(description="Campos de las relaciones de la tabla candidate que se quieren obtener. Se pueden especificar varios.")

SKILLS_PARAM = Query(description="Las habilidades del candidato. Se pueden especificar varias.")

AVAILABILITY_PARAM = Query(description="La disponibilidad del candidato. Se pueden especificar varias.")

CV_PARAM = File(description="El CV del candidato.", media_type="application/pdf")

COMPANIES_GET_JOBS = Query(description="Si se quieren obtener las ofertas de trabajos de la empresa.")

JOB_ID = Path(description="El id de la oferta de trabajo.")

JOB_EXTRA_FIELD = Query(description="Campos de las relaciones de la tabla job que se quieren obtener. Se pueden especificar varios.")