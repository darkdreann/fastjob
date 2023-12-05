from api.database.database_models.models import User
from api.security.hash_crypt import verify_string_hash


def check_request_with_response(request_data: dict, response_data: dict) -> None:
    """Comprueba que el usuario creado coincide con las respuestas de los endpoints.
    
        Args:
            request_data: Datos enviados en la petición.
            response_data: Datos recibidos en la respuesta."""
    
    for key in request_data:
        if key not in response_data: continue

        if isinstance(request_data[key], dict):
            check_request_with_response(request_data[key], response_data[key])

        else:
            if isinstance(request_data[key], str) and not key == "user_type": request_data[key] = request_data[key].lower()
            assert response_data[key] == request_data[key], f"{response_data[key]} == {request_data[key]} in {key}"


async def check_request_data_saved(request_data: dict, **kwargs) -> None:
    """Comprueba que el usuario creado esta guardado correctamente en la base de datos.
    
        Args:
            request_data: Datos enviados en la petición
            **kwargs:
                -> data: Objeto de la base de datos
                -> user_type: Tipo de usuario a comprobar"""

    record = kwargs.get("data")

    for key in request_data:
        record_att = getattr(record, key, None)

        if record_att is None: raise KeyError(f"Test fail: {key} not found in {record}.")
        if key in ["password","user_type"]: continue
        if key.endswith("id"): record_att = str(record_att)

        if isinstance(request_data[key], dict):
            await check_request_data_saved(request_data[key], data=record_att)
            
        else:
            if isinstance(request_data[key], str): request_data[key] = request_data[key].lower()
            assert request_data[key] == record_att, f"{request_data[key]} == {record_att} in {key}"
            
    if isinstance(record, User):
        assert kwargs["user_type"] == record.user_type
        assert verify_string_hash(request_data["password"], record.password)
