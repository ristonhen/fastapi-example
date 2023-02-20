from fastapi import FastAPI, Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

try:
    conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres', password='123')

my_posts = [
    {"title": "favorite foods 1", "contnet": "I like pizza","id": 1},
    {"title": "favorite foods 2", "contnet": "I like pizza","id": 2},
]

# find post
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

# find inex pos
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
# request Get method 
@app.get("/")
def read_root():
    return {"message": "wecome to my api"}

@app.get("/posts")
def get_post():
    return {"data": my_posts}

# @app.post("/createposts")
# # def create_post(payLoad: dict = Body(...)):
# def create_post(new_post: Post):
#     print(new_post.rating)
#     # print(post.dict())
#     #return {"new_post": f"{payload['title] content: {payload['content]}}"}
#     return {"data": "new_post"}


## create posts
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/lastest")
def get_lastest_post():
    post = my_posts[len(my_posts) -1]
    return {"detail": post}

@app.get("/posts/{id}")
def get_post(id: int):
# def get_post(id: int ,respone: Response):
    
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post whith id: {id} was not found")
        # respone.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post whith id: {id} was not found"}
    return {"post_ detail": post}

# delete post
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleteing post
    # find the inbox post
    index  = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")
    my_posts.pop(index)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index  = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}