from fastapi import FastAPI
from routers import producs, users
from fastapi.staticfiles import StaticFiles
 
app = FastAPI()

#routers
app.include_router(producs.router)
app.include_router(users.router)
app.mount ("/static", StaticFiles(directory="static"), name="statico")

@app.get("/")
async def root():
    return "Hola FastAPI!"

@app.get("/url")
async def url():
    return {"url":"https://mouredev.com/python"}