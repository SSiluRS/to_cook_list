from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import database, models, schemas_pantry, auth

router = APIRouter(prefix="/api/v1/products", tags=["products"])

@router.get("/", response_model=List[schemas_pantry.Product])
def get_products(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Product).all()

@router.post("/", response_model=schemas_pantry.Product)
def create_product(product: schemas_pantry.ProductCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    new_product = models.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product
