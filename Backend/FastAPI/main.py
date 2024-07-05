from fastapi import FastAPI
from routers import producs, users , jwt_auth_users , basic_auth_users
from fastapi.staticfiles import StaticFiles
 
app = FastAPI()

#routers
app.include_router(producs.router)
app.include_router(users.router)
app.include_router(jwt_auth_users.router)
app.include_router(basic_auth_users.router)



app.mount ("/static", StaticFiles(directory="static"), name="statico")

@app.get("/")
async def root():
    return "Hola FastAPI!"

@app.get("/url")
async def url():
    return {"url":"https://mouredev.com/python"}