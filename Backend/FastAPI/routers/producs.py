from fastapi import APIRouter

router = APIRouter(prefix="/producs",
                   tags=["producs"],
                   responses={404: {"message": "no encontrado"}})


producs_list = ["productos1","producto2","producto3","producto4","producto5"]


@router.get("/")
async def products():
    return producs_list



@router.get("/{id}")
async def products(id: int):
    return producs_list [id]


@router.get("/")
async def products(id: int):
    return producs_list [id]