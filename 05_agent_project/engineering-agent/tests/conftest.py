import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage.memory import memory


@pytest.fixture
def client() -> TestClient:
    memory.clear()
    return TestClient(app)
