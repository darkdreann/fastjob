from json import load
from datetime import date
from api.models.enums.models import UserType

_JSON_PATH = "test_data.json"

with open(_JSON_PATH, encoding="utf-8") as file:
    _DATA = load(file)


def _get_test_datas() -> dict:
    """Devuelve los datos de prueba."""
    test_datas = {}

    # recorre los modelos a ser creados
    for cls in _DATA:
        try:
            test_datas[cls] = []

            if cls == "User":
                test_datas[cls] = {
                    UserType.ADMIN: [],
                    UserType.CANDIDATE: [],
                    UserType.COMPANY: []
                }
            
            # recorre los diferentes registros a ser creados
            for new_data in _DATA[cls]:
                if cls in ["CandidateEducation", "Experience"]:
                    
                    if cls == "CandidateEducation": new_data["completion_date"] = date(**new_data["completion_date"])
                    if cls == "Experience": new_data["start_date"] = date(**new_data["start_date"]) ; new_data["end_date"] = date(**new_data["end_date"])


                test_datas[cls].append(new_data) if cls != "User" else test_datas[cls][new_data["user_type"]].append(new_data)
       
        except KeyError as exc:
            print(f"Error: {exc} class does not exist.")

        except TypeError as exc:
            print(f"Error: {exc}")

    return test_datas
    
DATA = _get_test_datas()