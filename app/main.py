from fastapi import FastAPI, Response,status,HTTPException, Depends
from fastapi.params import Body
# from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from sqlalchemy.orm import Session
from . import models , schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()




# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
#     # rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user='postgres', 
            password='123',
            cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfully!")
        break
    except Exception as error:
        print("Connection to database error")  
        print("Error:", error)  
        time.sleep(2)


# my_posts = [
#     {"title": "favorite foods 1", "contnet": "I like pizza","id": 1},
#     {"title": "favorite foods 2", "contnet": "I like pizza","id": 2},
# ]


######### find post
# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# ########### find inex pos
# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

# #########request Get method 
@app.get("/")
def read_root():
    return {"message": "wecome to my api"}

@app.get("/posts")
def get_post(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts;""")
    # post = cursor.fetchall()
    # print(post)
    posts = db.query(models.Post).all()
    # return  {"data": posts}
    return  posts

# @app.post("/createposts")
# # def create_post(payLoad: dict = Body(...)):
# def create_post(new_post: Post):
#     print(new_post.rating)
#     # print(post.dict())
#     #return {"new_post": f"{payload['title] content: {payload['content]}}"}
#     return {"data": "new_post"}


############### create posts
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_description= schemas.Post)
def create_posts(post: schemas.PostCreate ,db: Session = Depends(get_db)):
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 1000000)
    # my_posts.append(post_dict)
    # return {"data": post_dict}
    ## ############################
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """,
    #     (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit() 
    # ###############################################
    # print(**post.dict())
    # new_post = models.Post(title = post.title, content = post.content, published = post.published)
    new_post = models.Post(**post.dict())
    print(new_post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# @app.get("/posts/lastest")
# def get_lastest_post():
#     post = my_posts[len(my_posts) -1]
#     return {"detail": post}

@app.get("/posts/{id}")
def get_post(id: str, db: Session = Depends(get_db)):
# def get_post(id: int ,respone: Response):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id)))
    # post = cursor.fetchone()
    # post = find_post(id)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post whith id: {id} was not found")
        # respone.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post whith id: {id} was not found"}
    return post

# delete post
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning * """,(str(id)))
    # delete_post = cursor.fetchone()
    # conn.commit()
    post  = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # print(post.title)
    # cursor.execute(
    #     """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;""",
    #     (post.title,post.content,post.published,str(id))
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query  = db.query(models.Post).filter(models.Post.id == str(id))
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()