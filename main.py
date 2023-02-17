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

# request Get method 
@app.get("/")
def read_root():
    return {"message": "wecome to my api"}

@app.get("/posts")
def get_post():
    return {"data": "This is your API"}

@app.post("/createposts")
# def create_post(payLoad: dict = Body(...)):
def create_post(new_post: Post):
    print(new_post.rating)
    return {"data": "new_post"}

## title str , content str 