from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import urllib.request
import urllib.parse
import json
from .. import database, models, schemas_pantry, auth

router = APIRouter(prefix="/api/v1/products", tags=["products"])

@router.get("/search-external")
def search_external_products(query: str, current_user: models.User = Depends(auth.get_current_user)):
    if not query or len(query.strip()) < 2:
        return []
    
    try:
        encoded_query = urllib.parse.quote(query.strip())
        url = f"https://ru.openfoodfacts.org/cgi/search.pl?search_terms={encoded_query}&search_simple=1&action=process&json=1&page_size=20"
        
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'CulinaryNavigator/1.0 (contact: localtest@example.com)'}
        )
        
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status != 200:
                return []
            
            data = json.loads(response.read().decode('utf-8'))
            products = data.get("products", [])
            results = []
            
            for prod in products:
                name = prod.get("product_name_ru") or prod.get("product_name")
                if not name:
                    continue
                
                # Extract nutriments
                nutriments = prod.get("nutriments", {})
                
                # Get energy/calories per 100g
                calories = nutriments.get("energy-kcal_100g")
                if calories is None:
                    energy_100g = nutriments.get("energy_100g")
                    if energy_100g is not None:
                        try:
                            calories = float(energy_100g) / 4.184
                        except (ValueError, TypeError):
                            calories = 0.0
                    else:
                        calories = 0.0
                
                proteins = nutriments.get("proteins_100g") or 0.0
                fats = nutriments.get("fat_100g") or nutriments.get("fats_100g") or 0.0
                carbohydrates = nutriments.get("carbohydrates_100g") or 0.0
                
                try:
                    results.append({
                        "name": str(name)[:100],
                        "calories": round(float(calories), 1),
                        "proteins": round(float(proteins), 1),
                        "fats": round(float(fats), 1),
                        "carbohydrates": round(float(carbohydrates), 1)
                    })
                except (ValueError, TypeError):
                    continue
                
            return results
    except Exception as e:
        print(f"External search failed: {e}")
        return []

@router.get("/", response_model=List[schemas_pantry.Product])
def get_products(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Product).all()

@router.post("/", response_model=schemas_pantry.Product)
def create_product(product: schemas_pantry.ProductCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    new_product = models.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product
