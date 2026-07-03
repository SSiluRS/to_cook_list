from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.auth import router as auth_router
from .routes.products import router as products_router
from .routes.pantry import router as pantry_router
from .routes.recipes import router as recipes_router
from .routes.menu import router as menu_router
from .routes.shares import router as shares_router
from .routes.cooking_requests import router as cooking_requests_router

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(products_router)
app.include_router(pantry_router)
app.include_router(recipes_router)
app.include_router(menu_router)
app.include_router(shares_router)
app.include_router(cooking_requests_router)

@app.get("/")
def read_root():
    return {"Hello": "Culinary Navigator"}
