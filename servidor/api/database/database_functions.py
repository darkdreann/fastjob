from api.database.database_models.models import User, Candidate, Company
from api.database.connection import execute_database

def _get_function_check_table(func_name: str, table_name: str, user_id_name: str) -> str:
    """Plantilla para crear una función para comprobar si un usuario tiene una tabla asociada de un tipo de usuario (candidato|empresa)"""

    function_sql = f"""
        CREATE OR REPLACE FUNCTION {func_name}(id UUID)
        RETURNS BOOLEAN AS $$
        DECLARE 
            table_user_id UUID;
        BEGIN
            SELECT {user_id_name} INTO table_user_id FROM {table_name} WHERE {user_id_name} = id;

            RETURN table_user_id IS NOT NULL;

        END;
        $$ LANGUAGE plpgsql;
    """

    return function_sql

def _function_check_candidate_table() -> str:
    """Crea una función para comprobar si un usuario tiene una tabla asociada de un tipo de usuario (candidato|empresa)"""

    FUNC_NAME = "check_has_table_candidate"
    USER_ID_NAME = str(Candidate.user_id).split(".")[1]
    TABLE_NAME = Candidate.__tablename__

    return _get_function_check_table(FUNC_NAME, TABLE_NAME, USER_ID_NAME)

def _function_check_company_table():
    """Crea una función para comprobar si un usuario tiene una tabla asociada company"""

    FUNC_NAME = "check_has_table_company"
    USER_ID_NAME = str(Company.user_id).split(".")[1]
    TABLE_NAME = Company.__tablename__

    return _get_function_check_table(FUNC_NAME, TABLE_NAME, USER_ID_NAME)


def _function_check_user_type() -> str:
    """Crea una función para comprobar si un usuario es de un tipo específico"""

    USER_ID_NAME = str(User.id).split(".")[1]
    TYPE_NAME = str(User.user_type).split(".")[1]
    TABLE_NAME = User.__tablename__

    function_sql = f"""
        CREATE OR REPLACE FUNCTION check_user_type(candidate_id UUID, needed_user_type TEXT)
        RETURNS BOOLEAN AS $$
        DECLARE 
            current_user_type TEXT;
        BEGIN
            SELECT "{TYPE_NAME}" INTO current_user_type FROM "{TABLE_NAME}" WHERE "{USER_ID_NAME}" = candidate_id;

            RETURN needed_user_type = current_user_type;

        END;
        $$ LANGUAGE plpgsql;
    """

    return function_sql

@execute_database
def create_database_functions() -> tuple[str]:
    """Devuelve una lista con las funciones para crear en la base de datos."""

    return (
        _function_check_candidate_table(),
        _function_check_company_table(),
        _function_check_user_type()
    )