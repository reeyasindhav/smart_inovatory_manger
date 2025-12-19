from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.menu import MenuItem
from app.schemas.menu import MenuCreate, MenuUpdate

router = APIRouter(prefix="/menu", tags=["Menu"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_menu(item: MenuCreate, db: Session = Depends(get_db)):
    menu = MenuItem(**item.dict())
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu

@router.get("/")
def list_menu(db: Session = Depends(get_db)):
    return db.query(MenuItem).all()

@router.put("/{menu_id}")
def update_menu(
    menu_id: int,
    item: MenuUpdate,
    db: Session = Depends(get_db)
):
    menu = db.query(MenuItem).filter(MenuItem.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu item not found")

    for key, value in item.dict(exclude_unset=True).items():
        setattr(menu, key, value)

    db.commit()
    return menu

@router.delete("/{menu_id}")
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = db.query(MenuItem).filter(MenuItem.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu item not found")

    db.delete(menu)
    db.commit()
    return {"message": "Menu item deleted"}
