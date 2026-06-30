from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import database, models, schemas_pantry, auth

router = APIRouter(prefix="/api/v1/pantry", tags=["pantry"])

@router.get("/", response_model=List[schemas_pantry.Pantry])
def get_pantry(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Pantry).filter(models.Pantry.user_id == current_user.id).all()

@router.put("/", response_model=schemas_pantry.Pantry)
def update_pantry_item(item: schemas_pantry.PantryCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Check if item exists
    pantry_item = db.query(models.Pantry).filter(
        models.Pantry.user_id == current_user.id,
        models.Pantry.product_id == item.product_id
    ).first()
    
    if pantry_item:
        pantry_item.weight_g = item.weight_g
    else:
        pantry_item = models.Pantry(user_id=current_user.id, **item.dict())
        db.add(pantry_item)
    
    db.commit()
    db.refresh(pantry_item)
    return pantry_item
