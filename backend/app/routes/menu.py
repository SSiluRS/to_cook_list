from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from datetime import datetime
from .. import database, models, schemas_recipe, auth

router = APIRouter(prefix="/api/v1/menu", tags=["menu"])

@router.get("/", response_model=List[schemas_recipe.Menu])
def get_menu(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    query = db.query(models.Menu).filter(models.Menu.user_id == current_user.id)
    if start_date:
        query = query.filter(models.Menu.date >= start_date)
    if end_date:
        query = query.filter(models.Menu.date <= end_date)
        
    menu_items = query.order_by(models.Menu.date.asc(), models.Menu.meal_type.asc()).all()
    
    # Pre-fetch user pantry to build recipe schema if needed
    user_pantry = db.query(models.Pantry).filter(models.Pantry.user_id == current_user.id).all()
    
    # We will build schemas manually because we need to include recipe details dynamically
    from .recipes import build_recipe_schema
    
    results = []
    for item in menu_items:
        recipe_details = None
        if item.recipe:
            recipe_details = build_recipe_schema(item.recipe, user_pantry, db)
            
        results.append(schemas_recipe.Menu(
            id=item.id,
            user_id=item.user_id,
            date=item.date,
            meal_type=item.meal_type,
            recipe_id=item.recipe_id,
            recipe_title=item.recipe.title if item.recipe else "Unknown Recipe",
            recipe=recipe_details
        ))
        
    return results

@router.post("/", response_model=schemas_recipe.Menu)
def add_menu_item(
    menu_data: schemas_recipe.MenuCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Verify recipe exists and user has access to it
    recipe = db.query(models.Recipe).filter(models.Recipe.id == str(menu_data.recipe_id)).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
        
    # Check access permission
    if not recipe.is_public and recipe.author_id != current_user.id:
        has_share = db.query(models.SharedAccess).filter(
            models.SharedAccess.recipe_id == str(menu_data.recipe_id),
            models.SharedAccess.shared_with_id == current_user.id
        ).first()
        
        has_request = db.query(models.CookingRequest).filter(
            models.CookingRequest.recipe_id == str(menu_data.recipe_id),
            models.CookingRequest.receiver_id == current_user.id
        ).first()
        
        if not has_share and not has_request:
            raise HTTPException(status_code=403, detail="No access to this recipe")
            
    new_menu = models.Menu(
        user_id=current_user.id,
        date=menu_data.date,
        meal_type=menu_data.meal_type,
        recipe_id=str(menu_data.recipe_id)
    )
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    
    # Build response schema
    user_pantry = db.query(models.Pantry).filter(models.Pantry.user_id == current_user.id).all()
    from .recipes import build_recipe_schema
    recipe_details = build_recipe_schema(new_menu.recipe, user_pantry, db) if new_menu.recipe else None
    
    return schemas_recipe.Menu(
        id=new_menu.id,
        user_id=new_menu.user_id,
        date=new_menu.date,
        meal_type=new_menu.meal_type,
        recipe_id=new_menu.recipe_id,
        recipe_title=new_menu.recipe.title if new_menu.recipe else "Unknown Recipe",
        recipe=recipe_details
    )

@router.delete("/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_menu_item(
    menu_id: str,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    menu_item = db.query(models.Menu).filter(
        models.Menu.id == menu_id,
        models.Menu.user_id == current_user.id
    ).first()
    
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
        
    db.delete(menu_item)
    db.commit()
    return None
