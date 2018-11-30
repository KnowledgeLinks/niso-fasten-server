import pytest
import app as service

@pytest.fixture
def app():
    return service.api


def test_home(app):
    r = app.requests.get("/")
    assert r.text.endswith(f"{service.__version__} NISO FASTEN Server")
