import os
import pytest
from fastapi.testclient import TestClient

# Ensure tests always run in MOCK mode (no external calls)
os.environ["MOCK_MODE"] = "true"

from app.main import app

@pytest.fixture(scope="session")
def client():
    return TestClient(app)
