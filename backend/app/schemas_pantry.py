from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class ProductBase(BaseModel):
    name: str
    calories: float
    proteins: float
    fats: float
    carbohydrates: float
    is_public: bool = True

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: UUID
    class Config:
        from_attributes = True

class PantryBase(BaseModel):
    product_id: UUID
    weight_g: float

class PantryCreate(PantryBase):
    pass

class Pantry(PantryBase):
    id: UUID
    user_id: UUID
    product: Optional[Product] = None
    class Config:
        from_attributes = True
