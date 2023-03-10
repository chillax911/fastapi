from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
from app import models
from app.oauth2 import create_access_token

# Note: suffix "_test" for the db name
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)    # Used to clear the tables.
    Base.metadata.create_all(bind=engine)  # Used to build the tables.
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session                                # Previously, this was 'yield db'
        finally:
            session.close()                              # Previously, this was 'db.close'
    app.dependency_overrides[get_db] = override_get_db   # This will swap / substitute get_db, this is used extensively through many files.
    yield TestClient(app)                                # yield is the same as return.

@pytest.fixture
def test_user(client):
    user_data = {"email": "hello123@gmail.com",
              "password": "password321"}
    res = client.post("/users", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "hello01@gmail.com",
              "password": "password321"}
    res = client.post("/users", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title"   : "first title",
        "content" : "first content",
        "owner_id": test_user['id']
    },{
        "title"   : "2nd title",
        "content" : "2nd content",
        "owner_id": test_user['id']
    },{
        "title"   : "3rd title",
        "content" : "3rd content",
        "owner_id": test_user['id']
    },{
        "title"   : "first title",
        "content" : "first content",
        "owner_id": test_user2['id']
    }]
    def create_post_model(post):
        return models.Post(**post)                 # Convert a dictionary into a post model

    post_map = map(create_post_model, posts_data)  # This maps (converts) from right-to-left (<<<)
    posts = list(post_map)                         # Convert to a list (from a map)
    session.add_all(posts)
    # Long-hand version:
    # session.add_all([models.Post(title="1st title", content="..", "owner_id"=test_user['id]), models.Post(title="2nd title", content="..", "owner_id"=test_user['id])])
    session.commit()
    posts = session.query(models.Post).all()
    return posts

