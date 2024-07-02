from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [
    User(id=1, name="santiago", surname="santaigo-sz", url="https://santiago-sz.com", age=27),
    User(id=2, name="jorge", surname="sago-sz", url="https://santisz.com", age=22),
    User(id=3, name="sSSSantiago", surname="igo-sz", url="https://sz.com", age=27)
]

@router.get("/")
async def get_users(): 
    return users_list

@router.get("/{name}")
async def get_user_by_name(name: str):
    users = filter(lambda user: user.name == name, users_list)
    user_list = list(users)
    if not user_list:
        raise HTTPException(status_code=404, detail="User not found")
    return user_list[0]

@router.get("/id/{id}")
async def get_user_by_id(id: int):
    user = buscar_usuario(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Search user helper function
def buscar_usuario(id: int):
    users = filter(lambda user: user.id == id, users_list)
    user_list = list(users)
    if not user_list:
        return None
    return user_list[0]

@router.post("/", response_model=User, status_code=201)
async def create_user(user: User): 
    if buscar_usuario(user.id):
        raise HTTPException(status_code=404, detail="User already exists")
    users_list.append(user)
    return user

@router.put("/")
async def update_user(user: User):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            return user
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/")
async def delete_user(id: int):
    for saved_user in users_list:
        if saved_user.id == id:
            users_list.remove(saved_user)
            return users_list
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/id/{id}")
async def delete_user_by_id(id: int):
    for saved_user in users_list:
        if saved_user.id == id:
            users_list.remove(saved_user)
            return users_list
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/user/")
async def delete_user_by_instance(user: User):
    for saved_user in users_list:
        if saved_user.id == user.id:
            users_list.remove(saved_user)
            return users_list
    raise HTTPException(status_code=404, detail="User not found")
