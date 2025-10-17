from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models
from app.database import engine, get_db
from fastapi import FastAPI, Response, status, HTTPException, Depends
from app.schemas import  PostCreate, PostUpdate, PostResponse, UserResponse, UserCreate, UserUpdate
from app.models import Post, User
from app.utils import hash


router = APIRouter(
    prefix="/users",
    tags=["Users"]

)

# Users routes
@router.get("/", response_model=list[UserResponse])
def create_user(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} was not found")
    return user
    

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash(user.password)
    user.password=hashed_password
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user_query = db.query(User).filter(User.id == id)
    user = user_query.first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found"
        )

    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=UserResponse)
def update_post(id: int, user: UserUpdate, db: Session = Depends(get_db)):
    user_query = db.query(User).filter(User.id == id)
    user_to_update = user_query.first()

    if user_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found"
        )

    update_data = user.dict(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )

    user_query.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(user_to_update)
    return user_to_update

