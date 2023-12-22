from json import load
from datetime import date
from api.models.enums.models import UserType
from api.utils.functions.env_config import CONFIG

# ruta del archivo json
_JSON_PATH = CONFIG.TEST_DATA_JSON_PATH

# se carga el archivo json
with open(_JSON_PATH, encoding="utf-8") as file:
    _DATA = load(file)

def _get_test_datas() -> dict:
    """
    Devuelve los datos de prueba.

    Retorna un diccionario que contiene los datos de prueba para diferentes modelos.
    Los datos de prueba se generan a partir de la variable _DATA, que contiene la información
    necesaria para crear los registros de prueba.

    Returns:
    - dict: Un diccionario que contiene los datos de prueba para diferentes modelos.
    """
    test_datas = {}

    # recorre los modelos a ser creados
    for cls in _DATA:
        try:
            # crea una lista vacía para el modelo
            test_datas[cls] = []
            
            # si el modelo es User, se crean listas vacías para cada tipo de usuario
            if cls == "User":
                test_datas[cls] = {
                    UserType.ADMIN: [],
                    UserType.CANDIDATE: [],
                    UserType.COMPANY: []
                }
            
            # recorre los diferentes registros a ser creados
            for new_data in _DATA[cls]:
                # si el modelo es CandidateEducation o Experience, se convierten las fechas a objetos date
                if cls in ["CandidateEducation", "Experience"]:
                    
                    # se convierten las fechas a objetos date
                    if cls == "CandidateEducation": new_data["completion_date"] = date(**new_data["completion_date"])
                    if cls == "Experience": new_data["start_date"] = date(**new_data["start_date"])
                    if cls == "Experience" and "end_date" in new_data: new_data["end_date"] = date(**new_data["end_date"])

                # si el modelo es User, se añade el tipo de usuario a la lista correspondiente, si no se añade el registro a la lista
                test_datas[cls].append(new_data) if cls != "User" else test_datas[cls][new_data["user_type"]].append(new_data)
       
        except KeyError as exc:
            # si no se encuentra el modelo, se muestra un error
            print(f"Error: {exc} class does not exist.")

        except TypeError as exc:
            # si ocurre un error al crear el registro, se muestra un error
            print(f"Error: {exc}")

    return test_datas

# se obtienen los datos de prueba
DATA = _get_test_datas()