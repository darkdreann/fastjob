from api.database.connection import Base, get_session
from api.database.database_models.models import *
from api.tests.test_utils.data_json import DATA
from api.models.enums.models import UserType

async def create_test_data() -> None:
    """
    Crea los datos de prueba en la base de datos.

    Esta función se utiliza para crear datos de prueba en la base de datos. Recorre los diferentes modelos y registros
    definidos en la variable DATA y los crea en la sesión de base de datos proporcionada por get_session(). Si ocurre
    algún error durante la creación o confirmación de los datos, se imprime un mensaje de error.
    """
    async for session in get_session():
        try:
            # diccionario con los modelos de la base de datos
            models = {
                "User": User,
                "Sector": Sector,
                "Address": Address,
                "Education": Education,
                "Language": Language,
                "Candidate": Candidate,
                "LanguageLevel": LanguageLevel,
                "EducationLevel": EducationLevel,
                "JobLanguage": JobLanguage,
                "Company": Company,
                "Experience": Experience,
                "Job": Job,
                "JobCandidate": JobCandidate,
                "SectorEducation": SectorEducation,
                "CandidateEducation": CandidateEducation,
                "CandidateLanguage": CandidateLanguage,
                "JobEducation": JobEducation
            }

            # recorre los modelos a ser creados
            for cls in DATA.keys():
                
                # obtiene el modelo de la base de datos
                model = models[cls]

                # si el modelo es User, se junta los datos de los diferentes tipos de usuario
                if model == User:
                    data = DATA[cls][UserType.ADMIN] + DATA[cls][UserType.COMPANY] + DATA[cls][UserType.CANDIDATE]
                else:
                    # si no, se obtienen los datos del modelo
                    data = DATA[cls]

                # recorre los datos del modelo
                for new_data in data:
                    # recorre los campos de los datos y convierte los campos que terminan en id a UUID
                    new_data_with_UUID = {key: value if not key.endswith("id") else UUID(value) for key, value in new_data.items()}

                    # crea el registro y lo añade a la sesión
                    new_record = model(**new_data_with_UUID)
                    session.add(new_record)


        except Exception as exc:
            # si ocurre un error, se imprime un mensaje de error
            print(f"Error: Fallo en la creación de datos de prueba.\n{exc}")

        else:
            try:
                # se intenta hacer commit de los datos
                await session.commit()

            except Exception as exc:
                # si ocurre un error, se hace rollback de los datos y se imprime un mensaje de error
                await session.rollback()
                print(f"Error: Fallo en la confirmación de los datos de prueba. Realizando rollback.\n{exc}")


async def get_database_record(query, only_one: bool = False) -> Base | None:
    """
    Devuelve un objeto de una tabla de la base de datos buscando por un campo.
    
    Args:
    - query: Consulta a la base de datos.
    - only_one: Indica si se devuelve un solo registro o varios.
    """
    
    # se obtiene la sesión de la base de datos
    async for session in get_session():

        # se ejecuta la consulta
        result = await session.execute(query)

        # se obtiene la función para obtener el resultado dependiendo de si se quiere un solo registro o varios
        result_fetch = result.scalars if not only_one else result.scalar
        
        # se obtiene el registro y se devuelve
        record = result_fetch()
        return record
    
async def save_database_record(record: Base) -> None:
    """
    Guarda un registro en la base de datos.
    
    Args:
    - record: Registro a guardar.
    """
    
    # se obtiene la sesión de la base de datos
    async for session in get_session():
        
        # se añade el registro a la sesión
        session.add(record)
        
        try:
            # se intenta hacer commit del registro
            await session.commit()
            
        except Exception as exc:
            # si ocurre un error, se hace rollback del registro y se imprime un mensaje de error
            await session.rollback()


    