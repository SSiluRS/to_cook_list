from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import urllib.request
import urllib.parse
import json
from .. import database, models, schemas_pantry, auth
from ..services.external_product_search import search_products

router = APIRouter(prefix="/api/v1/products", tags=["products"])

@router.get("/search-external")
def search_external_products(query: str, current_user: models.User = Depends(auth.get_current_user)):
    """Search external product databases using fallback providers.
    Returns a list of product dicts with fields: name, calories, proteins, fats, carbohydrates.
    """
    if not query or len(query.strip()) < 2:
        return []
    return search_products(query)

from sqlalchemy import or_

@router.get("/", response_model=List[schemas_pantry.Product])
def get_products(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Product).filter(
        or_(
            models.Product.author_id == current_user.id,
            models.Product.author_id == None
        )
    ).all()

@router.post("/", response_model=schemas_pantry.Product)
def create_product(product: schemas_pantry.ProductCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    new_product = models.Product(author_id=current_user.id, **product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.put("/{product_id}", response_model=schemas_pantry.Product)
def update_product(product_id: str, product_data: schemas_pantry.ProductCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if db_product.author_id and db_product.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нельзя редактировать продукты, созданные другими пользователями")
    
    db_product.name = product_data.name
    db_product.calories = product_data.calories
    db_product.proteins = product_data.proteins
    db_product.fats = product_data.fats
    db_product.carbohydrates = product_data.carbohydrates
    db_product.is_public = product_data.is_public
    
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if db_product.author_id and db_product.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нельзя удалять продукты, созданные другими пользователями")
    
    try:
        db.delete(db_product)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Невозможно удалить продукт, так как он используется в кладовой или в рецептах.")
    return None
