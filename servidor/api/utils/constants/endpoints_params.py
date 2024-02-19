from fastapi import Query, Path, File, Body

LIMIT = Query(description="Límite de registros devueltos.", gt=0)

DEFAULT_LIMIT = 20

OFFSET = Query(description="Permite omitir un número específico de registros en el conjunto de resultados.", ge=0)

DEFAULT_OFFSET = 0

USER_ID = Path(description="El ID del usuario.")

SECTOR_ID = Path(description="El ID del sector.")

SECTOR_CATEGORY_KEYWORD = Path(description="Palabras clave para buscar en la categoría del sector.")

SECTOR_CATEGORY = Path(description="Categoria del sector.")

SECTOR_SUBCATEGORY_KEYWORD = Path(description="Palabras clave para buscar en la subcategoría del sector.")

SECTOR_EXTRA_FIELD = Query(description="Campos de las relaciones de la tabla sector que se quieren obtener. Se pueden especificar varios.")

RESOURCE_SECTOR = Query(description="El sector del recurso del candidato. Puede ser el ID o la categoría del sector.")

SECTOR_ID_QUERY = Query(description=SECTOR_ID.description)

SECTOR_CATEGORY_QUERY = Query(description="La categoría del sector de la oferta de trabajo.")

ADDRESS_ID = Path(description="El ID de la dirección.")

ADDRESS_POSTAL_CODE = Path(description="El código postal de la dirección. Debe ser un número de 5 dígitos.", ge=10000, le=99999)

ADDRESS_POSTAL_CODE_QUERY = Query(description=ADDRESS_POSTAL_CODE.description, ge=10000, le=99999)

ADDRESS_PROVINCE = Query(description="La provincia de la dirección.")

ADDRESS_PROVINCE_KEYWORD = Path(description="Palabras clave para buscar en la provincia de la dirección.")

ADDRESS_EXTRA_FIELD = Query(description="Campos de las relaciones de la tabla address que se quieren obtener. Se pueden especificar varios.")

EDUCATION_ID = Path(description="El ID de la formación.")

EDUCATION_NAME_KEYWORD_QUERY = Query(description="Palabras clave para buscar en el nombre de la formación.")

EDUCATION_NAME_KEYWORD = Path(description="Palabras clave para buscar en el nombre de la formación.")

EDUCATION_LEVEL_NAME_KEYWORD = Query(description="Palabras clave para buscar en el nombre del nivel la formación.")

EDUCATION_ID_BODY = Body(description=EDUCATION_ID.description)

COMPLETION_DATE = Body(description="La fecha de finalización de la formación.")

EDUCATION_LEVEL_ID = Path(description="El ID del nivel de la formación.")

EDUCATION_LEVEL_VALUE_PARAM = Query(description="El valor del nivel de la formación. Debe ser un número mayor a 0.", gt=0)

GET_EDUCATION = Query(description="Permite obtener las formaciones del nivel.")

EDUCATION_EXTRA_FIELD = Query(description="Campos de las relaciones de la tabla education que se quieren obtener. Se pueden especificar varios.")

EDUCATION_NAME_PARAM = Query(description="El nombre de la formación.")

EDUCATION_LEVEL_PARAM = Query(description="El valor del nivel de la formación. Debe ser un número mayor a 0.", gt=0)

LANGUAGE_ID = Path(description="El ID del idioma.")

LANGUAGE_NAME_KEYWORD = Path(description="Palabras clave para buscar en el nombre del idioma.")

LANGUAGE_NAME_KEYWORD_QUERY = Query(description="Palabras clave para buscar en el nombre del idioma.")

LANGUAGE_LEVEL_NAME_KEYWORD = Path(description="Palabras clave para buscar en el nombre del nivel del idioma.")

LANGUAGE_ID_BODY = Body(description=LANGUAGE_ID.description)

LANGUAGE_LEVEL_ID = Path(description="El ID del nivel del idioma.")

LANGUAGE_LEVEL_ID_BODY = Body(description=LANGUAGE_LEVEL_ID.description)

LANGUAGE_LEVEL_EXTRA_FIELD = Query(description="Campos de las relaciones de la tabla language_level que se quieren obtener. Se pueden especificar varios.")

LANGUAGE_EXTRA_FIELD = Query(description="Campos de las relaciones de la tabla language que se quieren obtener. Se pueden especificar varios.")

LANGUAGE_CANDIDATE = Query(description="El ID o el nombre del idioma que debe tener el candidato.")

LANGUAGE_LEVEL_VALUE = Query(description="El valor del nivel de idioma. Debe ser un número mayor a 0.", gt=0)

EXPERIENCE_MONTHS = Query(description="La cantidad de meses requeridos de experiencia del candidato. Debe ser un número mayor a 0.", gt=0)

EXPERIENCE_ID = Path(description="El ID de la experiencia.")

CANDIDATE_EXTRA_FIELD = Query(description="Campos de las relaciones de la tabla candidate que se quieren obtener. Se pueden especificar varios.")

CANDIDATE_MINIMAL_FIELDS = Query(description="Si se quiere obtener solo los campos mínimos para listar los candidatos. Por defecto es falso.")

SKILLS_PARAM = Query(description="Las habilidades del candidato que debe tener el candidato. Se pueden especificar varias.")

AVAILABILITY_PARAM = Query(description="La disponibilidad que debe tener el candidato.")

CV_PARAM = File(description="El curriculum del candidato.", media_type="application/pdf")

COMPANIES_GET_JOBS = Query(description="Si se quieren obtener las ofertas de trabajo de la empresa.")

JOB_ID = Path(description="El ID de la oferta de trabajo.")

JOB_EXTRA_FIELD = Query(description="Campos de las relaciones de la tabla job que se quieren obtener. Se pueden especificar varios.")

KEYWORD = Query(description="La palabra clave para buscar en las ofertas de trabajo.")

JOB_ACTIVE = Query(description="Si se quiere obtener solo las ofertas de trabajo activas. Por defecto es verdadero.")

JOB_MINIMAL_FIELDS = Query(description="Si se quiere obtener solo los campos mínimos para listar las ofertas de trabajo. Por defecto es falso.")

JOB_KEYWORD = Path(description="Palabras clave para buscar en las ofertas de trabajo.")
