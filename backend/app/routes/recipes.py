from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from .. import database, models, schemas_recipe, auth

router = APIRouter(prefix="/api/v1/recipes", tags=["recipes"])

def calculate_recipe_kbju(ingredients):
    calories = 0.0
    proteins = 0.0
    fats = 0.0
    carbohydrates = 0.0
    total_weight = 0.0
    
    for ing in ingredients:
        prod = ing.product
        weight = ing.weight_g
        total_weight += weight
        calories += (weight * (prod.calories or 0.0)) / 100.0
        proteins += (weight * (prod.proteins or 0.0)) / 100.0
        fats += (weight * (prod.fats or 0.0)) / 100.0
        carbohydrates += (weight * (prod.carbohydrates or 0.0)) / 100.0
        
    total_kbju = {
        "calories": round(calories, 2),
        "proteins": round(proteins, 2),
        "fats": round(fats, 2),
        "carbohydrates": round(carbohydrates, 2)
    }
    
    if total_weight > 0:
        kbju_per_100 = {
            "calories": round((calories / total_weight) * 100.0, 2),
            "proteins": round((proteins / total_weight) * 100.0, 2),
            "fats": round((fats / total_weight) * 100.0, 2),
            "carbohydrates": round((carbohydrates / total_weight) * 100.0, 2)
        }
    else:
        kbju_per_100 = {
            "calories": 0.0,
            "proteins": 0.0,
            "fats": 0.0,
            "carbohydrates": 0.0
        }
        
    return total_kbju, kbju_per_100

def get_smart_match_data(ingredients, user_pantry):
    pantry_dict = {str(item.product_id): item.weight_g for item in user_pantry}
    
    match_ingredients = []
    sufficient_count = 0
    
    for ing in ingredients:
        prod = ing.product
        required = ing.weight_g
        available = pantry_dict.get(str(ing.product_id), 0.0)
        
        is_sufficient = available >= required
        if is_sufficient:
            sufficient_count += 1
            
        missing = max(0.0, required - available)
        
        match_ingredients.append({
            "product_id": ing.product_id,
            "product_name": prod.name,
            "required_weight_g": required,
            "available_weight_g": available,
            "is_sufficient": is_sufficient,
            "missing_weight_g": missing
        })
        
    total_count = len(ingredients)
    pct = (sufficient_count / total_count * 100.0) if total_count > 0 else 100.0
    can_cook = sufficient_count == total_count
    
    return {
        "can_cook": can_cook,
        "match_percentage": round(pct, 2),
        "ingredients": match_ingredients
    }

def build_recipe_schema(recipe: models.Recipe, user_pantry, db: Session) -> schemas_recipe.Recipe:
    total_kbju, kbju_per_100g = calculate_recipe_kbju(recipe.ingredients)
    smart_match = get_smart_match_data(recipe.ingredients, user_pantry)
    
    author_username = recipe.author.username if recipe.author else None
    
    # We serialize the recipe ingredients manually to ensure product schemas are correctly built
    ingredients_list = []
    for ing in recipe.ingredients:
        ingredients_list.append({
            "product_id": ing.product_id,
            "weight_g": ing.weight_g,
            "product": ing.product
        })

    return schemas_recipe.Recipe(
        id=recipe.id,
        title=recipe.title,
        description=recipe.description,
        instruction=recipe.instruction,
        is_public=recipe.is_public,
        author_id=recipe.author_id,
        author_username=author_username,
        ingredients=ingredients_list,
        total_kbju=total_kbju,
        kbju_per_100g=kbju_per_100g,
        smart_match=smart_match
    )

@router.get("/", response_model=List[schemas_recipe.Recipe])
def get_recipes(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Query recipes: owned, public, shared with user, or requested from user
    recipes = db.query(models.Recipe).filter(
        or_(
            models.Recipe.is_public == True,
            models.Recipe.author_id == current_user.id,
            models.Recipe.id.in_(
                db.query(models.SharedAccess.recipe_id).filter(models.SharedAccess.shared_with_id == current_user.id)
            ),
            models.Recipe.id.in_(
                db.query(models.CookingRequest.recipe_id).filter(models.CookingRequest.receiver_id == current_user.id)
            )
        )
    ).all()
    
    user_pantry = db.query(models.Pantry).filter(models.Pantry.user_id == current_user.id).all()
    
    return [build_recipe_schema(r, user_pantry, db) for r in recipes]

@router.get("/{recipe_id}", response_model=schemas_recipe.Recipe)
def get_recipe(recipe_id: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
        
    # Check access permission
    if not recipe.is_public and recipe.author_id != current_user.id:
        has_share = db.query(models.SharedAccess).filter(
            models.SharedAccess.recipe_id == recipe_id,
            models.SharedAccess.shared_with_id == current_user.id
        ).first()
        
        has_request = db.query(models.CookingRequest).filter(
            models.CookingRequest.recipe_id == recipe_id,
            models.CookingRequest.receiver_id == current_user.id
        ).first()
        
        if not has_share and not has_request:
            raise HTTPException(status_code=403, detail="Access denied to this recipe")
            
    user_pantry = db.query(models.Pantry).filter(models.Pantry.user_id == current_user.id).all()
    return build_recipe_schema(recipe, user_pantry, db)

@router.post("/", response_model=schemas_recipe.Recipe)
def create_recipe(recipe_data: schemas_recipe.RecipeCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    new_recipe = models.Recipe(
        title=recipe_data.title,
        description=recipe_data.description,
        instruction=recipe_data.instruction,
        is_public=recipe_data.is_public,
        author_id=current_user.id
    )
    db.add(new_recipe)
    db.flush() # Flush to get new_recipe.id
    
    for ing in recipe_data.ingredients:
        # Verify product exists
        product = db.query(models.Product).filter(models.Product.id == str(ing.product_id)).first()
        if not product:
            raise HTTPException(status_code=400, detail=f"Product with id {ing.product_id} not found")
            
        recipe_ing = models.RecipeIngredient(
            recipe_id=new_recipe.id,
            product_id=str(ing.product_id),
            weight_g=ing.weight_g
        )
        db.add(recipe_ing)
        
    db.commit()
    db.refresh(new_recipe)
    
    user_pantry = db.query(models.Pantry).filter(models.Pantry.user_id == current_user.id).all()
    return build_recipe_schema(new_recipe, user_pantry, db)

@router.put("/{recipe_id}", response_model=schemas_recipe.Recipe)
def update_recipe(recipe_id: str, recipe_data: schemas_recipe.RecipeUpdate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
        
    if recipe.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to edit this recipe")
        
    if recipe_data.title is not None:
        recipe.title = recipe_data.title
    if recipe_data.description is not None:
        recipe.description = recipe_data.description
    if recipe_data.instruction is not None:
        recipe.instruction = recipe_data.instruction
    if recipe_data.is_public is not None:
        recipe.is_public = recipe_data.is_public
        
    if recipe_data.ingredients is not None:
        # Delete old ingredients
        db.query(models.RecipeIngredient).filter(models.RecipeIngredient.recipe_id == recipe_id).delete()
        
        # Add new ingredients
        for ing in recipe_data.ingredients:
            product = db.query(models.Product).filter(models.Product.id == str(ing.product_id)).first()
            if not product:
                raise HTTPException(status_code=400, detail=f"Product with id {ing.product_id} not found")
                
            recipe_ing = models.RecipeIngredient(
                recipe_id=recipe_id,
                product_id=str(ing.product_id),
                weight_g=ing.weight_g
            )
            db.add(recipe_ing)
            
    db.commit()
    db.refresh(recipe)
    
    user_pantry = db.query(models.Pantry).filter(models.Pantry.user_id == current_user.id).all()
    return build_recipe_schema(recipe, user_pantry, db)

@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(recipe_id: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
        
    if recipe.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this recipe")
        
    # Delete associated ingredients first
    db.query(models.RecipeIngredient).filter(models.RecipeIngredient.recipe_id == recipe_id).delete()
    # Delete sharing access
    db.query(models.SharedAccess).filter(models.SharedAccess.recipe_id == recipe_id).delete()
    # Delete cooking requests
    db.query(models.CookingRequest).filter(models.CookingRequest.recipe_id == recipe_id).delete()
    # Delete from menu
    db.query(models.Menu).filter(models.Menu.recipe_id == recipe_id).delete()
    
    db.delete(recipe)
    db.commit()
    return None

@router.get("/{recipe_id}/match", response_model=schemas_recipe.RecipeSmartMatch)
def match_recipe(recipe_id: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
        
    user_pantry = db.query(models.Pantry).filter(models.Pantry.user_id == current_user.id).all()
    return get_smart_match_data(recipe.ingredients, user_pantry)
