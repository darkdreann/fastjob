from api.database.connection import Base, get_session
from api.database.database_models.models import *
from api.tests.test_utils.data_json import DATA

async def create_test_data() -> None:
    """Crea los datos de prueba en la base de datos."""

    async for session in get_session():
        try:
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

                model = models[cls]


                if model == User:
                    for user_type in DATA[cls].keys():
                        for new_data in DATA[cls][user_type]:
                            new_record = model(**new_data)
                            session.add(new_record)

                else:
                    # recorre los diferentes registros a ser creados
                    for new_data in DATA[cls]:

                        new_record = model(**new_data)
                        session.add(new_record)

        except Exception as exc:
            print(f"Error: Test data creation failed.\n{exc}")

        else:
            try:
                await session.commit()

            except Exception as exc:
                await session.rollback()
                
                print(f"Error: Test data commit failed. Rolling back.\n{exc}")


async def get_database_record(query, only_one: bool = False) -> Base | None:
    """Devuelve un objeto de una tabla de la base de datos buscando por un campo.
    
        Args:
            table: Tabla de la base de datos de la que se quiere obtener el objeto.
            field: Campo por el que se quiere buscar.
            value: Valor del campo por el que se quiere buscar."""
    
    async for session in get_session():

        result = await session.execute(query)

        result_fetch = result.scalars if not only_one else result.scalar

        record = result_fetch()

        return record


    