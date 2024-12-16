import pytest
from core.app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True  # Enables Flask's testing mode
    client = app.test_client()
    yield client