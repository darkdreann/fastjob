from api.database.database_models.models import User, Candidate, Company

def _get_function_check_table(func_name: str, table_name: str, user_id_name: str) -> str:
    """Plantiilla para crear una función para comprobar si un usuario tiene una tabla asociada de un tipo de usuario (candidato|empresa)"""

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

    func_name = "check_has_table_candidate"
    user_id_name = str(Candidate.user_id).split(".")[1]
    table_name = Candidate.__tablename__

    return _get_function_check_table(func_name, table_name, user_id_name)

def _function_check_company_table():
    """Crea una función para comprobar si un usuario tiene una tabla asociada company"""

    func_name = "check_has_table_company"
    user_id_name = str(Company.user_id).split(".")[1]
    table_name = Company.__tablename__

    return _get_function_check_table(func_name, table_name, user_id_name)


def _function_check_user_type() -> str:
    """Crea una función para comprobar si un usuario es de un tipo específico"""

    user_id_name = str(User.id).split(".")[1]
    type_name = str(User.user_type).split(".")[1]
    table_name = User.__tablename__

    function_sql = f"""
        CREATE OR REPLACE FUNCTION check_user_type(candidate_id UUID, needed_user_type TEXT)
        RETURNS BOOLEAN AS $$
        DECLARE 
            current_user_type TEXT;
        BEGIN
            SELECT "{type_name}" INTO current_user_type FROM "{table_name}" WHERE "{user_id_name}" = candidate_id;

            RETURN needed_user_type = current_user_type;

        END;
        $$ LANGUAGE plpgsql;
    """

    return function_sql



def get_database_functions() -> list[str]:
    """Devuelve una lista con las funciones para crear en la base de datos."""

    return [
        _function_check_candidate_table(),
        _function_check_company_table(),
        _function_check_user_type()
    ]
