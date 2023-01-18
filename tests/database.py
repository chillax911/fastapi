from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base

# Note: suffix "_test" for the db name
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def session():
    print("my session fixutre ran")
    Base.metadata.drop_all(bind=engine)    # Used to clear the tables.
    Base.metadata.create_all(bind=engine)  # Used to build the tables.    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def client(session):
    def override_get_db():
        try:
            yield session                                # Previously, this was 'yield db'
        finally:
            session.close()                              # Previously, this was 'db.close'
    app.dependency_overrides[get_db] = override_get_db   # This will swap / substitute get_db, this is used extensively through many files. 
    yield TestClient(app)                                # yield is the same as return.