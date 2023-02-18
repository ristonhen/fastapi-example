from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
my_post = [
    {"title": "title of post 1", "contnet": "content of post 1","id": 1},
    {"title": "favorite foods", "contnet": "I like pizza","id": 2},
]
# request Get method 
@app.get("/")
def read_root():
    return {"message": "wecome to my api"}

@app.get("/posts")
def get_post():
    return {"data": my_post}

# @app.post("/createposts")
# # def create_post(payLoad: dict = Body(...)):
# def create_post(new_post: Post):
#     print(new_post.rating)
#     # print(post.dict())
#     #return {"new_post": f"{payload['title] content: {payload['content]}}"}
#     return {"data": "new_post"}

@app.post("/posts")
def create_posts(post: Post):
    print(post)
    print(post.dict())
    return {"data": post}

## title str , content str 