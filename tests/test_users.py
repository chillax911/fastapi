import pytest
from app import schemas
from .database import client, session

@pytest.fixture
def test_user(client):
    user_data = {"email": "hello123@gmail.com", 
              "password": "password321"}
    res = client.post("/users", json=user_data)
    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

def test_root(client, session):
    res = client.get("/")
    assert res.json().get('message') == 'Hello World! Welcome to the New Year!!!'
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users", json={"email": "hello123X@gmail.com", "password": "password321"})
    new_user = schemas.UserOut(**res.json())  # This will have the structure of the schemas.UserOut pydantic model. Now we can test that the structure is correct. 
    assert new_user.email == "hello123X@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user["email"],
                                      "password": test_user["password"]  })
    assert res.status_code == 200