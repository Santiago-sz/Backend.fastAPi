from fastapi import FastAPI 
from routers import products
from routers import users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#routers
app.include_router(products.router)
app.include_router(users.router)
app.mount("/static",StaticFiles(directory="static"), name="static")

@app.get("/")

async def root():
    return "Hello world"

@app.get("/url")      
async def url():
    return{"url":"https://luchito.com/python"}
    