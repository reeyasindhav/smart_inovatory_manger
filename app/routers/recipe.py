from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.recipe import Recipe
from app.schemas.recipe import RecipeCreate

router = APIRouter(prefix="/recipes", tags=["Recipes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    new_recipe = Recipe(**recipe.dict())
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe

@router.get("/menu/{menu_item_id}")
def get_recipe_for_menu(menu_item_id: int, db: Session = Depends(get_db)):
    recipes = db.query(Recipe).filter(
        Recipe.menu_item_id == menu_item_id
    ).all()

    if not recipes:
        raise HTTPException(status_code=404, detail="No recipe defined")

    return recipes
