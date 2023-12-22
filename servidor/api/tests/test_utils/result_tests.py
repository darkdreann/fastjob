from datetime import timedelta
from uuid import UUID
from api.models.metadata.constants import DAYS_TO_MONTHS_DIVIDER
from api.database.database_models.models import User, Base
from api.models.enums.models import WorkSchedule, UserType
from api.security.hash_crypt import verify_string_hash


def check_request_with_response(request_data: dict, response_data: dict) -> None:
    """
    Comprueba que el usuario creado coincide con las respuestas de los endpoints.
    
    Args:
    - request_data: Datos enviados en la petición.
    - response_data: Datos recibidos en la respuesta.
    """
    
    # se recorren los datos de la petición
    for key in request_data:
        # si el dato no está en la respuesta, se pasa al siguiente
        if key not in response_data: continue

        # si el dato es un diccionario, se llama a la función recursivamente
        if isinstance(request_data[key], dict):
            check_request_with_response(request_data[key], response_data[key])

        else:
            # si el dato es un string, se convierte a minúsculas, excepto el tipo de usuario, el tin y el la jornada laboral
            if isinstance(request_data[key], str) and not key in ["user_type", "tin", "work_schedule"]: request_data[key] = request_data[key].lower()
            # se comprueba que el dato de la petición coincide con el de la respuesta
            assert response_data[key] == request_data[key], f"{response_data[key]} == {request_data[key]} en {key}"


def check_request_data_saved(request_data: dict, record: Base, user_type: UserType = None) -> None:
    """
    Comprueba que el usuario creado está guardado correctamente en la base de datos.
    
    Args:
    - request_data: Datos enviados en la petición.
    - data: Objeto de la base de datos.
    - user_type: Tipo de usuario a comprobar.
    """
    def transform_record_attribute(record_att):
        """
        Transforma un atributo del registro según su tipo.

        Args:
        - record_att: El atributo de registro a transformar.

        Returns:
        - El atributo de registro transformado.
        """
        if isinstance(record_att, UUID): 
            return str(record_att)
        elif isinstance(record_att, WorkSchedule): 
            return record_att.value
        elif isinstance(record_att, timedelta): 
            return round(record_att.days / DAYS_TO_MONTHS_DIVIDER)
        elif isinstance(request_data[key], str) and key not in ["tin", "work_schedule"]:
            return record_att.lower()
        return record_att


    # se recorren los datos de la petición
    for key in request_data:
        # obtenemos el atributo del objeto de la base de datos
        record_att = getattr(record, key, None)

        # si el atributo no existe, se lanza una excepción
        if record_att is None: raise KeyError(f"Fallo en la prueba: {key} no encontrado en {record}.")
        # si el atributo es password o user_type, se pasa al siguiente
        if key in ["password","user_type"]: continue

        # si el dato es un diccionario, se llama a la función recursivamente
        if isinstance(request_data[key], dict):
            check_request_data_saved(request_data[key], record=record_att, user_type=user_type)
            
        else:
            # se transforma el atributo de registro según su tipo si es necesario
            record_att = transform_record_attribute(record_att)
            # se comprueba que el dato de la petición coincide con el de la base de datos
            assert request_data[key] == record_att, f"{request_data[key]} == {record_att} en {key}"
    
    # si el objeto es un usuario, se comprueba que el tipo de usuario y la contraseña coinciden
    if isinstance(record, User):
        assert user_type == record.user_type, f"{user_type} == {record.user_type} en user_type"
        assert verify_string_hash(request_data["password"], record.password)
