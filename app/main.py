from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# import os
# path = os.getenv("MY_DB_URL")
# print (path) 
# models.Base.metadata.create_all(bind=engine) # Not needed any more. This is SQLAlchemy to create table (if not exist), but we use alembic now.

app = FastAPI() # To create an instance of it.

# Start the web server: uvicorn app.main:app --reload
# Test it in web site at: http://127.0.0.1:8000/  ExitSkySql

origins = ["*"] # What domains can talk to the api
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Can restrict post, get, delete requests
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root(): 
    return {"message": "Hello World"}
