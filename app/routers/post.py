from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, oauth2
from app.database import engine, get_db
from fastapi import FastAPI, Response, status, HTTPException, Depends
from app.schemas import  PostCreate, PostUpdate, PostResponse, UserResponse, UserCreate, UserUpdate
from app.models import Post, User
from app.utils import hash
from typing import Optional



router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=list[PostResponse]) 
def get_posts(
            db: Session = Depends(get_db), 
            current_user =  Depends(oauth2.get_current_user),
            limit : int =10,
            skip :int = 0,
            search : Optional[str] = ""):
    return db.query(Post).filter((Post.owner_id == current_user.id)&(Post.title.contains(search))).limit(limit).offset(skip).all()
     

@router.get("/{id}", response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user =  Depends(oauth2.get_current_user)):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Not authorized to perform requested action")
    return post
    
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostCreate, 
                db: Session = Depends(get_db), 
                current_user =  Depends(oauth2.get_current_user)): 
    
    new_post = Post(owner_id=current_user.id,**post.dict()) # unpacking
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user =  Depends(oauth2.get_current_user)):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found"
        )
    print("//////////////////////////////////////")
    print("//////////////////////////////////////")
    print("//////////////////////////////////////")

    print(post.owner_id)
    print(current_user.id)
    print("//////////////////////////////////////")
    print("//////////////////////////////////////")
    print("//////////////////////////////////////")


    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=PostResponse)
def update_post(id: int, post: PostUpdate, 
                db: Session = Depends(get_db), 
                current_user =  Depends(oauth2.get_current_user)):
    post_query = db.query(Post).filter(Post.id == id)
    post_to_update = post_query.first()

    if post_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found"
        )

    update_data = post.dict(exclude_unset=True)
    
    if post_to_update.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Not authorized to perform requested action")
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )

    post_query.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(post_to_update)
    return post_to_update
