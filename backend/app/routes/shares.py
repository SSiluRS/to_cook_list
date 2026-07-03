from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from .. import database, models, schemas_recipe, auth

router = APIRouter(prefix="/api/v1/shares", tags=["shares"])

@router.get("/", response_model=List[schemas_recipe.SharedAccess])
def get_shares(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Retrieve all shared items where user is either the owner or the recipient
    shares = db.query(models.SharedAccess).filter(
        or_(
            models.SharedAccess.owner_id == current_user.id,
            models.SharedAccess.shared_with_id == current_user.id
        )
    ).all()
    
    results = []
    for s in shares:
        results.append(schemas_recipe.SharedAccess(
            id=s.id,
            owner_id=s.owner_id,
            owner_username=s.owner.username,
            shared_with_id=s.shared_with_id,
            shared_with_username=s.shared_with.username,
            recipe_id=s.recipe_id,
            recipe_title=s.recipe.title if s.recipe else None,
            menu_id=s.menu_id
        ))
        
    return results

@router.post("/", response_model=schemas_recipe.SharedAccess)
def create_share(
    share_data: schemas_recipe.SharedAccessCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Find user to share with
    target_user = db.query(models.User).filter(
        or_(
            models.User.username == share_data.shared_with_username,
            models.User.email == share_data.shared_with_username
        )
    ).first()
    
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if target_user.id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot share with yourself")
        
    if not share_data.recipe_id and not share_data.menu_id:
        raise HTTPException(status_code=400, detail="You must specify recipe_id or menu_id to share")
        
    recipe_id_str = str(share_data.recipe_id) if share_data.recipe_id else None
    menu_id_str = str(share_data.menu_id) if share_data.menu_id else None
    
    # Check if target resource exists and belongs to current_user
    if recipe_id_str:
        recipe = db.query(models.Recipe).filter(
            models.Recipe.id == recipe_id_str,
            models.Recipe.author_id == current_user.id
        ).first()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found or you are not the owner")
            
        # Check if already shared
        existing_share = db.query(models.SharedAccess).filter(
            models.SharedAccess.owner_id == current_user.id,
            models.SharedAccess.shared_with_id == target_user.id,
            models.SharedAccess.recipe_id == recipe_id_str
        ).first()
        if existing_share:
            raise HTTPException(status_code=400, detail="Already shared with this user")
            
    if menu_id_str:
        menu = db.query(models.Menu).filter(
            models.Menu.id == menu_id_str,
            models.Menu.user_id == current_user.id
        ).first()
        if not menu:
            raise HTTPException(status_code=404, detail="Menu not found or you are not the owner")
            
        # Check if already shared
        existing_share = db.query(models.SharedAccess).filter(
            models.SharedAccess.owner_id == current_user.id,
            models.SharedAccess.shared_with_id == target_user.id,
            models.SharedAccess.menu_id == menu_id_str
        ).first()
        if existing_share:
            raise HTTPException(status_code=400, detail="Already shared with this user")
            
    # Create share access
    new_share = models.SharedAccess(
        owner_id=current_user.id,
        shared_with_id=target_user.id,
        recipe_id=recipe_id_str,
        menu_id=menu_id_str
    )
    db.add(new_share)
    db.commit()
    db.refresh(new_share)
    
    return schemas_recipe.SharedAccess(
        id=new_share.id,
        owner_id=new_share.owner_id,
        owner_username=new_share.owner.username,
        shared_with_id=new_share.shared_with_id,
        shared_with_username=new_share.shared_with.username,
        recipe_id=new_share.recipe_id,
        recipe_title=new_share.recipe.title if new_share.recipe else None,
        menu_id=new_share.menu_id
    )

@router.delete("/{share_id}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_share(
    share_id: str,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    share = db.query(models.SharedAccess).filter(models.SharedAccess.id == share_id).first()
    if not share:
        raise HTTPException(status_code=404, detail="Shared access not found")
        
    # Check if user is owner or recipient
    if share.owner_id != current_user.id and share.shared_with_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to revoke this share")
        
    db.delete(share)
    db.commit()
    return None
