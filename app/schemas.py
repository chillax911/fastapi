from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic import conint
#uvicorn app.main:app --reload

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass # pass through the definition from PostBase

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True # Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, but an ORM model (or any other arbitrary object with attributes).  https://fastapi.tiangolo.com/tutorial/sql-databases/

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut # You need to make sure this UserOut class is above this class otherwise you'll get a syntax error.

    class Config:
        orm_mode = True # Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, but an ORM model (or any other arbitrary object with attributes).  https://fastapi.tiangolo.com/tutorial/sql-databases/

# class PostForPostOut(PostBase):
#     id: int
#     created_at: datetime
#     owner_id: int
#     # owner: UserOut # You need to make sure this UserOut class is above this class otherwise you'll get a syntax error.

#     class Config:
#         orm_mode = True # Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, but an ORM model (or any other arbitrary object with attributes).  https://fastapi.tiangolo.com/tutorial/sql-databases/

# class PostOut(PostBase):
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True # Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, but an ORM model (or any other arbitrary object with attributes).  https://fastapi.tiangolo.com/tutorial/sql-databases/

class UserCreate(BaseModel):
    email: EmailStr #https://docs.pydantic.dev/usage/types/#pydantic-types do pip freeze and verify that email-validator==1.3.0 is already installed
    password: str


class UserLogin(BaseModel):    
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # This ensures that the number is a) an integer and b) either zero or 1 (less than 1). Unfortunately it can be a negative number!