from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
import uuid
import datetime
from .database import Base
import enum

class User(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password_hash = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    recipes = relationship("Recipe", back_populates="author")
    pantry_items = relationship("Pantry", back_populates="user")

class Product(Base):
    __tablename__ = "products"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), unique=True, index=True)
    calories = Column(Float)
    proteins = Column(Float)
    fats = Column(Float)
    carbohydrates = Column(Float)
    is_public = Column(Boolean, default=False)
    author_id = Column(String(36), ForeignKey("users.id"), nullable=True)

class Pantry(Base):
    __tablename__ = "pantry"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"))
    product_id = Column(String(36), ForeignKey("products.id"))
    weight_g = Column(Float)

    user = relationship("User", back_populates="pantry_items")
    product = relationship("Product")

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255))
    description = Column(String(1000))
    instruction = Column(String(5000))
    author_id = Column(String(36), ForeignKey("users.id"))
    is_public = Column(Boolean, default=True)

    author = relationship("User", back_populates="recipes")
    ingredients = relationship("RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan")

class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"
    recipe_id = Column(String(36), ForeignKey("recipes.id"), primary_key=True)
    product_id = Column(String(36), ForeignKey("products.id"), primary_key=True)
    weight_g = Column(Float)

    recipe = relationship("Recipe", back_populates="ingredients")
    product = relationship("Product")

class MealType(enum.Enum):
    breakfast = "Breakfast"
    lunch = "Lunch"
    dinner = "Dinner"
    snack = "Snack"

class Menu(Base):
    __tablename__ = "menu"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"))
    date = Column(DateTime)
    meal_type = Column(Enum(MealType))
    recipe_id = Column(String(36), ForeignKey("recipes.id"))

    user = relationship("User")
    recipe = relationship("Recipe")

class SharedAccess(Base):
    __tablename__ = "shared_access"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(String(36), ForeignKey("users.id"))
    shared_with_id = Column(String(36), ForeignKey("users.id"))
    recipe_id = Column(String(36), ForeignKey("recipes.id"), nullable=True)
    menu_id = Column(String(36), ForeignKey("menu.id"), nullable=True)

    owner = relationship("User", foreign_keys=[owner_id])
    shared_with = relationship("User", foreign_keys=[shared_with_id])
    recipe = relationship("Recipe")
    menu = relationship("Menu")

class RequestStatus(enum.Enum):
    pending = "Pending"
    accepted = "Accepted"
    declined = "Declined"

class CookingRequest(Base):
    __tablename__ = "cooking_requests"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sender_id = Column(String(36), ForeignKey("users.id"))
    receiver_id = Column(String(36), ForeignKey("users.id"))
    recipe_id = Column(String(36), ForeignKey("recipes.id"), nullable=True)
    menu_id = Column(String(36), ForeignKey("menu.id"), nullable=True)
    status = Column(Enum(RequestStatus), default=RequestStatus.pending)

    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])
    recipe = relationship("Recipe")
    menu = relationship("Menu")
