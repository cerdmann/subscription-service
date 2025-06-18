import pytest
from app import create_app
from src.database import engine, Base

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    Base.metadata.create_all(bind=engine)
    yield app
    Base.metadata.drop_all(bind=engine)