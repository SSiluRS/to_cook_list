from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import User, Product, Pantry, Recipe, RecipeIngredient, Menu, SharedAccess, CookingRequest

def cleanup():
    db = SessionLocal()
    try:
        # 1. Find all test users (starts with user_)
        test_users = db.query(User).filter(
            User.username.like("user_%")
        ).all()
        
        user_ids = [u.id for u in test_users]
        print(f"Found {len(test_users)} test users to clean up: {[u.username for u in test_users]}")
        
        if user_ids:
            # Delete dependent relations for test users
            # A. Cooking requests
            db.query(CookingRequest).filter(
                (CookingRequest.sender_id.in_(user_ids)) | (CookingRequest.receiver_id.in_(user_ids))
            ).delete(synchronize_session=False)
            
            # B. Shared Access
            db.query(SharedAccess).filter(
                (SharedAccess.owner_id.in_(user_ids)) | (SharedAccess.shared_with_id.in_(user_ids))
            ).delete(synchronize_session=False)
            
            # C. Menu items
            db.query(Menu).filter(Menu.user_id.in_(user_ids)).delete(synchronize_session=False)
            
            # D. Pantry items
            db.query(Pantry).filter(Pantry.user_id.in_(user_ids)).delete(synchronize_session=False)
            
            # E. Recipe Ingredients and Recipes
            recipes = db.query(Recipe).filter(Recipe.author_id.in_(user_ids)).all()
            recipe_ids = [r.id for r in recipes]
            if recipe_ids:
                db.query(RecipeIngredient).filter(RecipeIngredient.recipe_id.in_(recipe_ids)).delete(synchronize_session=False)
                db.query(Recipe).filter(Recipe.id.in_(recipe_ids)).delete(synchronize_session=False)
            
            # F. Users
            db.query(User).filter(User.id.in_(user_ids)).delete(synchronize_session=False)
            db.commit()
            print("Users and associated user data cleaned up successfully.")
            
        # 2. Clean up test products
        deleted_products = db.query(Product).filter(
            (Product.name.like("Тестовый Продукт%")) | 
            (Product.name.like("Импорт Курица%")) | 
            (Product.name.like("Тестовый Банан%")) | 
            (Product.name.like("Супер Ингредиент%"))
        ).delete(synchronize_session=False)
        
        db.commit()
        print(f"Cleaned up {deleted_products} test products.")
        
    except Exception as e:
        db.rollback()
        print(f"Error during cleanup: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    cleanup()
