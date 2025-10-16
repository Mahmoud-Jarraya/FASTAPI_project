from pydantic import BaseModel
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
class PostResponse(PostCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True  # tells Pydantic to read data from SQLAlchemy objects
