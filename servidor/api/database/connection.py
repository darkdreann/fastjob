from sqlalchemy import text, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.exc import OperationalError, ArgumentError
from api.database.database_functions import get_database_functions
from api.database.database_models.models import Base
from api.utils.constants.error_strings import DATABASE_ERROR
from api.utils.functions.env_config import CONFIG


# Database configuration
DATABASE = CONFIG.DATABASE_NAME if not CONFIG.DEVELOPMENT else CONFIG.DEVELOPMENT_DATABASE_NAME
DATABASE_URL = f"postgresql+asyncpg://{CONFIG.DATABASE_USERNAME}:{CONFIG.DATABASE_PASSWORD}@{CONFIG.DATABASE_IP}:{CONFIG.DATABASE_PORT}/{DATABASE}"

try:
    engine = create_async_engine(DATABASE_URL, echo=CONFIG.DEVELOPMENT, pool_size=CONFIG.POOL_SIZE, max_overflow=CONFIG.MAX_OVERFLOW)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    
except (OperationalError, ArgumentError) as exc:
    raise ConnectionError(DATABASE_ERROR.format(exc=exc))

async def create_tables():
    """Crea las tablas en la base de datos."""

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    
async def drop_tables():
    """Elimina las tablas de la base de datos."""

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)

async def create_database_functions():
    """Crea las funciones de usuario en PostgreSQL."""

    database_funcs = get_database_functions()

    async with engine.connect() as connection:
        for func in database_funcs:
            await connection.execute(text(func))
        await connection.commit()
        
async def get_session():
    """Obtiene una sesión de la base de datos."""

    async with session_maker() as session:
        yield session

async def close_connection():
    """Cierra la conexión a la base de datos."""

    await engine.dispose()


