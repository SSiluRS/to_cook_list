from fastapi import FastAPI
from .routes.auth import router as auth_router
from .routes.products import router as products_router
from .routes.pantry import router as pantry_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(products_router)
app.include_router(pantry_router)

@app.get("/")
def read_root():
    return {"Hello": "Culinary Navigator"}
