from typing import Self
from sqlalchemy import MetaData
from api.database.connection import engine
from api.database.database_models.metadata.view_name import JOB_KEYWORDS_VIEW_NAME

class JobKeywordModel:
    """
    Modelo para la vista de palabras clave de trabajo.
    """

    SINGLETON_INSTANCE = None

    def __init__(self, view) -> Self:
            """
            Inicializa una instancia de la clase.

            Args:
            - view: La vista asociada al modelo.
            """
            self.view = view

    @classmethod
    async def _create_instance(cls) -> None:
            """
            Crea una instancia de la clase.

            Esta función se encarga de crear una instancia de la clase actual.
            Utiliza la biblioteca SQLAlchemy para reflejar las vistas en la base de datos
            y asigna la tabla correspondiente a la instancia.
            """
            metadata = MetaData()

            async with engine.begin() as connection:
                await connection.run_sync(metadata.reflect, views=True)

            instance = metadata.tables[JOB_KEYWORDS_VIEW_NAME]

            cls.SINGLETON_INSTANCE = cls(instance)

    @classmethod
    def get_view(cls) -> Self:
        return cls.SINGLETON_INSTANCE.view

async def create_all_views_instances() -> None:
    """
    Crea todas las instancias de vistas.

    Esta función asincrónica crea todas las instancias de vistas en la base de datos.
    """
    await JobKeywordModel._create_instance()