from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models
from app.database import engine, get_db
from fastapi import FastAPI, Response, status, HTTPException, Depends
from app.schemas import  PostCreate, PostUpdate, PostResponse
from app.models import Post


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/posts", response_model=list[PostResponse]) 
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts

@app.get("/posts/{id}", response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post
    
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)): 
    new_post = Post(**post.dict()) # unpacking
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found"
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model=PostResponse)
def update_post(id: int, post: PostUpdate, db: Session = Depends(get_db)):
    post_query = db.query(Post).filter(Post.id == id)
    post_to_update = post_query.first()

    if post_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found"
        )

    # ✅ Only include fields actually sent by the client
    update_data = post.dict(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )

    post_query.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(post_to_update)
    return post_to_update


    