from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from .models import MealType, RequestStatus
from .schemas_pantry import Product

# Recipe Ingredient schemas
class RecipeIngredientBase(BaseModel):
    product_id: UUID
    weight_g: float

class RecipeIngredientCreate(RecipeIngredientBase):
    pass

class RecipeIngredient(RecipeIngredientBase):
    product: Product
    
    class Config:
        from_attributes = True

# Recipe schemas
class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None
    instruction: Optional[str] = None
    is_public: bool = True

class RecipeCreate(RecipeBase):
    ingredients: List[RecipeIngredientCreate]

class RecipeUpdate(RecipeBase):
    title: Optional[str] = None
    ingredients: Optional[List[RecipeIngredientCreate]] = None

# Custom response showing computed KBJU
class RecipeKBJU(BaseModel):
    calories: float
    proteins: float
    fats: float
    carbohydrates: float

class RecipeMatchIngredient(BaseModel):
    product_id: UUID
    product_name: str
    required_weight_g: float
    available_weight_g: float
    is_sufficient: bool
    missing_weight_g: float

class RecipeSmartMatch(BaseModel):
    can_cook: bool
    match_percentage: float
    ingredients: List[RecipeMatchIngredient]

class Recipe(RecipeBase):
    id: UUID
    author_id: UUID
    author_username: Optional[str] = None
    ingredients: List[RecipeIngredient] = []
    total_kbju: RecipeKBJU
    kbju_per_100g: RecipeKBJU
    smart_match: Optional[RecipeSmartMatch] = None

    class Config:
        from_attributes = True

# Menu schemas
class MenuBase(BaseModel):
    date: datetime
    meal_type: MealType
    recipe_id: UUID

class MenuCreate(MenuBase):
    pass

class Menu(BaseModel):
    id: UUID
    user_id: UUID
    date: datetime
    meal_type: MealType
    recipe_id: UUID
    recipe_title: Optional[str] = None
    recipe: Optional[Recipe] = None

    class Config:
        from_attributes = True

# Shared Access schemas
class SharedAccessBase(BaseModel):
    shared_with_username: str
    recipe_id: Optional[UUID] = None
    menu_id: Optional[UUID] = None

class SharedAccessCreate(SharedAccessBase):
    pass

class SharedAccess(BaseModel):
    id: UUID
    owner_id: UUID
    owner_username: str
    shared_with_id: UUID
    shared_with_username: str
    recipe_id: Optional[UUID] = None
    recipe_title: Optional[str] = None
    menu_id: Optional[UUID] = None

    class Config:
        from_attributes = True

# Cooking Request schemas
class CookingRequestBase(BaseModel):
    receiver_username: str
    recipe_id: Optional[UUID] = None
    menu_id: Optional[UUID] = None

class CookingRequestCreate(CookingRequestBase):
    pass

class CookingRequestUpdate(BaseModel):
    status: RequestStatus

class CookingRequest(BaseModel):
    id: UUID
    sender_id: UUID
    sender_username: str
    receiver_id: UUID
    receiver_username: str
    recipe_id: Optional[UUID] = None
    recipe_title: Optional[str] = None
    menu_id: Optional[UUID] = None
    status: RequestStatus

    class Config:
        from_attributes = True
