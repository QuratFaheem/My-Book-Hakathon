from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from datetime import timedelta
from .auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

# For development purposes, a simple user database
fake_users_db = {
    "user1": {
        "username": "user1",
        "full_name": "Test User 1",
        "email": "user1@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6LruGCKDV5TkwfCq",  # hashed 'secret'
        "disabled": False,
    },
    "user2": {
        "username": "user2",
        "full_name": "Test User 2",
        "email": "user2@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6LruGCKDV5TkwfCq",  # hashed 'secret'
        "disabled": False,
    }
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=User)
async def read_users_me(username: str = Depends(oauth2_scheme)):
    # In a real implementation, we would decode the token and get user details
    # For now, just returning a placeholder
    user = fake_users_db.get(username.split(":")[0] if ":" in username else username.split()[1])
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return User(username=user["username"], email=user["email"], full_name=user["full_name"])