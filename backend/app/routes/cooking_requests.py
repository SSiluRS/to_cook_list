from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from .. import database, models, schemas_recipe, auth

router = APIRouter(prefix="/api/v1/cooking-requests", tags=["cooking-requests"])

@router.get("/", response_model=List[schemas_recipe.CookingRequest])
def get_cooking_requests(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Retrieve all cooking requests where user is either sender or receiver
    requests = db.query(models.CookingRequest).filter(
        or_(
            models.CookingRequest.sender_id == current_user.id,
            models.CookingRequest.receiver_id == current_user.id
        )
    ).all()
    
    results = []
    for r in requests:
        results.append(schemas_recipe.CookingRequest(
            id=r.id,
            sender_id=r.sender_id,
            sender_username=r.sender.username,
            receiver_id=r.receiver_id,
            receiver_username=r.receiver.username,
            recipe_id=r.recipe_id,
            recipe_title=r.recipe.title if r.recipe else None,
            menu_id=r.menu_id,
            status=r.status
        ))
        
    return results

@router.post("/", response_model=schemas_recipe.CookingRequest)
def create_cooking_request(
    request_data: schemas_recipe.CookingRequestCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Find receiver user
    receiver = db.query(models.User).filter(
        or_(
            models.User.username == request_data.receiver_username,
            models.User.email == request_data.receiver_username
        )
    ).first()
    
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver user not found")
        
    if receiver.id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot send cooking requests to yourself")
        
    if not request_data.recipe_id and not request_data.menu_id:
        raise HTTPException(status_code=400, detail="You must specify recipe_id or menu_id")
        
    recipe_id_str = str(request_data.recipe_id) if request_data.recipe_id else None
    menu_id_str = str(request_data.menu_id) if request_data.menu_id else None
    
    # Check if target resource exists and belongs to current_user (sender)
    if recipe_id_str:
        recipe = db.query(models.Recipe).filter(
            models.Recipe.id == recipe_id_str,
            models.Recipe.author_id == current_user.id
        ).first()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found or you are not the owner")
            
    if menu_id_str:
        menu = db.query(models.Menu).filter(
            models.Menu.id == menu_id_str,
            models.Menu.user_id == current_user.id
        ).first()
        if not menu:
            raise HTTPException(status_code=404, detail="Menu not found or you are not the owner")
            
    # Check if there is already a pending request for the same resource to the same user
    existing_request = db.query(models.CookingRequest).filter(
        models.CookingRequest.sender_id == current_user.id,
        models.CookingRequest.receiver_id == receiver.id,
        models.CookingRequest.recipe_id == recipe_id_str,
        models.CookingRequest.menu_id == menu_id_str,
        models.CookingRequest.status == models.RequestStatus.pending
    ).first()
    
    if existing_request:
        raise HTTPException(status_code=400, detail="A pending request already exists for this item")
        
    # Create request
    new_request = models.CookingRequest(
        sender_id=current_user.id,
        receiver_id=receiver.id,
        recipe_id=recipe_id_str,
        menu_id=menu_id_str,
        status=models.RequestStatus.pending
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    
    return schemas_recipe.CookingRequest(
        id=new_request.id,
        sender_id=new_request.sender_id,
        sender_username=new_request.sender.username,
        receiver_id=new_request.receiver_id,
        receiver_username=new_request.receiver.username,
        recipe_id=new_request.recipe_id,
        recipe_title=new_request.recipe.title if new_request.recipe else None,
        menu_id=new_request.menu_id,
        status=new_request.status
    )

@router.patch("/{request_id}", response_model=schemas_recipe.CookingRequest)
def update_cooking_request_status(
    request_id: str,
    status_data: schemas_recipe.CookingRequestUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    request = db.query(models.CookingRequest).filter(models.CookingRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Cooking request not found")
        
    # Only the receiver can accept/decline the request
    if request.receiver_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the recipient can respond to cooking requests")
        
    if request.status != models.RequestStatus.pending:
        raise HTTPException(status_code=400, detail="This request has already been processed")
        
    request.status = status_data.status
    db.commit()
    db.refresh(request)
    
    return schemas_recipe.CookingRequest(
        id=request.id,
        sender_id=request.sender_id,
        sender_username=request.sender.username,
        receiver_id=request.receiver_id,
        receiver_username=request.receiver.username,
        recipe_id=request.recipe_id,
        recipe_title=request.recipe.title if request.recipe else None,
        menu_id=request.menu_id,
        status=request.status
    )
