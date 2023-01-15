from app import schemas
from .database import client, session

def test_root(client, session):
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