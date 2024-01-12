from api.database.database_models.models import Job
from api.database.connection import execute_database
from api.database.database_models.metadata.view_name import JOB_KEYWORDS_VIEW_NAME

class JobKeywordsView:
    """Clase para crear y actualizar la vista de palabras clave de las ofertas de trabajo."""

    @staticmethod
    def _create_job_keywords_view() -> str:
        """Crea una vista para obtener las palabras clave de las ofertas de trabajo."""

        VIEW_NAME = JOB_KEYWORDS_VIEW_NAME
        COLUMN_WORD_NAME = "word"
        COLUMN_COUNT_NAME = "count"
        TABLE_NAME = Job.__tablename__
        TITLE_NAME = str(Job.title).split(".")[1]
        DESC_NAME = str(Job.description).split(".")[1]
        
        view_sql = (
        f"DROP MATERIALIZED VIEW IF EXISTS {VIEW_NAME};",
        f"""
        CREATE MATERIALIZED VIEW {VIEW_NAME} AS
        SELECT {COLUMN_WORD_NAME}, COUNT(*) as {COLUMN_COUNT_NAME}
        FROM (
            SELECT UNNEST(COALESCE(regexp_split_to_array(TRIM({TITLE_NAME}), '\s+'), ARRAY[]::text[])) as {COLUMN_WORD_NAME}
            FROM {TABLE_NAME}
            UNION ALL
            SELECT UNNEST(COALESCE(regexp_split_to_array(TRIM({DESC_NAME}), '\s+'), ARRAY[]::text[])) as {COLUMN_WORD_NAME}
            FROM {TABLE_NAME}
        ) AS subquery
        GROUP BY {COLUMN_WORD_NAME};
        """,
        f"CREATE UNIQUE INDEX {VIEW_NAME}_index ON {VIEW_NAME} ({COLUMN_WORD_NAME});"
        )

        return view_sql
    
    @staticmethod
    def _refresh_job_keywords_view() -> str:
        """Actualiza la vista para obtener las palabras clave de las ofertas de trabajo."""

        VIEW_NAME = JOB_KEYWORDS_VIEW_NAME

        return f"REFRESH MATERIALIZED VIEW CONCURRENTLY {VIEW_NAME};"


# funciones para crear y actualizar todas las vistas de la base de datos

@execute_database
def create_database_views() -> tuple[str]:
    """Devuelve una lista con las funciones para crear en la base de datos."""
    
    return (
       *JobKeywordsView._create_job_keywords_view(),
    )

@execute_database
def refresh_database_views() -> tuple[str]:
    """Devuelve una lista con las funciones para crear en la base de datos."""
    
    return (
       JobKeywordsView._refresh_job_keywords_view(),
    )

