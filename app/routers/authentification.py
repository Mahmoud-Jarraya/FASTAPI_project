from fastapi import APIRouter, Depends, APIRouter, status, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserLogin, Token
from app.models import User
from app.utils import verify
from app.oauth2 import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
router = APIRouter(tags=["Authentification"])

@router.post("/login", response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    # create token
    access_token = create_access_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

    
