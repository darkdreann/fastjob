import pytest
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from api.main import app


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
            print("Client is ready")
            yield client


