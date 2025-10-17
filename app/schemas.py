from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # default value

class Post(PostBase):
    id: int
    created_at: datetime
    
# Request body model
class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass
  
# Response model
class PostResponse(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True  # tells Pydantic to read data from SQLAlchemy objects


class UserBase():
    pass

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at : datetime
    class Config:
        orm_mode = True  # tells Pydantic to read data from SQLAlchemy objects


class UserCreate(BaseModel):
    email: EmailStr
    password: str 

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str