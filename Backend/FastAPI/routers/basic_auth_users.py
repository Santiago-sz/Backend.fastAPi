from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: bool
    
class UserDB(User):
    password: str

users_db = {
    "Santiago":{ 
        "username": "Santiago",
        "full_name": "Santigo Suarez",
        "email": "santi@gmail.com",
        "disable": False,
        "password": "123456"
    },
    "Santiago1":{ 
        "username": "Santiago1",
        "full_name": "Santigo Suarez1",
        "email": "santi1@gmail.com",
        "disable": False,
        "password": "222222"
    },
    "Santiago2":{ 
        "username": "Santiago2",
        "full_name": "Santigo Suarez2",
        "email": "santi2@gmail.com",
        "disable": True,
        "password": "111111"
    }
}

def search_user(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user_dv(username: str):
    if username in users_db:
        return User(**users_db[username])

print(search_user("Santiago"))

async def current_user(token: str = Depends(oauth2)):
    user = search_user_dv(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales no válidas", 
            headers={"WWW-Authenticate": "Bearer"}
        )
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario deshabilitado"
        )
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es válido")
    
    user = search_user(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es válida")
    
    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
