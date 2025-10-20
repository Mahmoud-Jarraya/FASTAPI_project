from fastapi import FastAPI
from app import models
from app.database import engine
from fastapi import FastAPI
from app.routers import user, post, authentification

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentification.router)

@app.get("/")
def root():
    return "Start page"
