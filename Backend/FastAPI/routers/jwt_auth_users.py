from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1  # Changed to 15 minutes for testing
SECRET = "supersecret"  # Replace with a secure secret key

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

pwd_context = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: bool

class UserDB(User):
    password: str

users_db = {
    "Santiago": {
        "username": "Santiago",
        "full_name": "Santigo Suarez",
        "email": "santi@gmail.com",
        "disable": False,
        "password": "$2a$12$DEIxgjxVY9eJ4SDZzCqbuusfRgN/xXs6ggTHwjQOLWpIS4RNKyWSm"
    },
    "Santiago1": {
        "username": "Santiago1",
        "full_name": "Santigo Suarez1",
        "email": "santi1@gmail.com",
        "disable": False,
        "password": "$2a$12$s4u/VEK9V85xjhc8rN8hleQ6B/1gY2tiHxaiZvkfeTwlR90gZw4q."
    },
    "Santiago2": {
        "username": "Santiago2",
        "full_name": "Santigo Suarez2",
        "email": "santi2@gmail.com",
        "disable": True,
        "password": "$2a$12$Myw4nCEp6Ox2QH6Zk1X9g.iUq9rP9HKUgELJrAJ4Ida92pG3NlPCG"
    }
}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str):
    if username in users_db:
        user_dict = users_db[username]
        return UserDB(**user_dict)

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is disabled",
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_DURATION)
    access_token = {
        "sub": user.username,
        "exp": datetime.utcnow() + access_token_expires
    }
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
