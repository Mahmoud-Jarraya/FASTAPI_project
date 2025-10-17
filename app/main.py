from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models
from app.database import engine, get_db
from fastapi import FastAPI, Response, status, HTTPException, Depends
from app.schemas import  PostCreate, PostUpdate, PostResponse, UserResponse, UserCreate, UserUpdate
from app.models import Post, User
from app.utils import hash
from app.routers import user, post

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)




@app.get("/")
def root():
    return "Start page"
