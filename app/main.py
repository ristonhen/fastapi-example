from fastapi import FastAPI, Response,status,HTTPException, Depends
from fastapi.params import Body

from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models , schemas , utils
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

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

# ######### request Get method 
@app.get("/")
def read_root():
    return {"message": "wecome to my api"}

@app.get("/posts",response_model=List[schemas.Post])
def get_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return  posts

############### create posts
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate ,db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{id}",response_model=schemas.Post)
def get_post(id: str, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post whith id: {id} was not found")

    return post

# delete post
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post  = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query  = db.query(models.Post).filter(models.Post.id == str(id))
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):

    # hash the password - user.password
    hash_password = utils.hash(user.password)
    user.password = hash_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/users/{id}',response_model= schemas.UserOut)
def get_user(id: int ,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, 
                            detail=f"User with id: { id } does not exist")
    return user