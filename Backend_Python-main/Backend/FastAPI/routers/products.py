from fastapi import APIRouter

router = APIRouter(prefix="/products",
                   responses={404:{"message":"no encotrado"}},
                   tags=["products"])

products_list = ["producto 1", "producto 2"]

@router.get("/")
async def Products():
    return products_list

@router.get("/{id}")
async def Products(id:int):
    return products_list[id]

@router.get("/query/")
async def Products_query(id:int):
    return products_list[id]

