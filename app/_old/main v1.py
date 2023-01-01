# v1 - before connecting to a database

from fastapi import FastAPI, Response, status, HTTPException #To use the Frameworke / library
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI() # To create an instance of it.

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating: Optional[int] = None


#Start the web server:
# uvicorn main:app --reload
# Test it in web site at: http://127.0.0.1:8000/

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if int(p['id']) == id:
            return i

my_posts = [{"title": "title of post 1", "content": "conent of post 1", "id": 1}, {"title": "favorite foods", "content": "i like pizza", "id": 2}]

@app.get("/") # a Path operation. A decorator, denoted by the apersend character. Paths correstponds to the url path.
def root(): 
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts} ##This will automatically convert the array to a serialised json.

# @app.post("/createposts")
# def create_posts(payloadx: dict = Body(...)):
#     print (payloadx) ##Outputs to the terminal
#     return {"new_post here": f"title is: {payloadx['titlex']}. content is: {payloadx['contentx']}"} #Output to postman

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # print(post.dict())
    post_dict = post.dict()
    post_dict['id'] = randrange(0,10000)
    my_posts.append(post_dict)
    return {"data": post_dict} #Output to postman

@app.get("/posts/{id}") #{id} = Path parameter
def get_post(id: int, reponse: Response):
    # print(id)
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id:{id} was not found.")
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int ):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data': post_dict}