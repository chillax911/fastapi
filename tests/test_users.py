import pytest
from app import schemas
from jose import jwt
from app.config import settings

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
    res = client.post("/login", data={"username": test_user['email'],
                                      "password": test_user['password']  })
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=settings.algorithm)
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, passowrd, status_code", [
    ('wrongemail@gmail.com', 'password321'  , 403), 
    ('hello123@gmail.com'  , 'wrongpassword', 403), 
    ('wrongemail@gmail.com', 'wrongpassword', 403), 
    (None                  , 'password321'  , 422), 
    ('hello123@gmail.com'  , None           , 422)
])
# def test_incorrect_login(client, test_user, email, passowrd, status_code):
def test_incorrect_login(client,  email, passowrd, status_code):
    res = client.post("/login", data={"username": email,
                                      "password": passowrd     })
    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'