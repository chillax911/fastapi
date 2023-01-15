from fastapi.testclient import TestClient
import pytest
from app.main import app
from app import schemas

from app.config import settings

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
# from alembic import command

# Note: suffix "_test" for the db name
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine) # Used to build the tables.

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db   # This will swap / substitute get_db, this is used extensively through many files. 

# client = TestClient(app)   # This has been moved to below, inside a pytest fixture function.

@pytest.fixture   # Using the sqlalchemy method
def client():
    Base.metadata.drop_all(bind=engine)    # Used to clear the tables.
    Base.metadata.create_all(bind=engine)  # Used to build the tables.
    yield TestClient(app)                  # yield is the same as return.
    # Notice that the tables are NOT cleared after the test.
    # This is a personal preference. It allows you to view the data after the test. It is cleared at the next test.

# @pytest.fixture   # Using the alembic method
# def client():
#     command.upgrate("head")
#     yield TestClient(app)                  # yield is the same as return.
#     command.downgrade("base")


def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == 'Hello World! Welcome to the New Year!!!'
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password": "password321"})
    # print(res.json())
    # assert res.json().get("email") == "hello123@gmail.com"
    new_user = schemas.UserOut(**res.json())  # This will have the structure of the schemas.UserOut pydantic model. Now we can test that the structure is correct. 
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201