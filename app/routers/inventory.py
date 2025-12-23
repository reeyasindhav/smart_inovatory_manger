from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.inventory import InventoryItem
from app.schemas.inventory import (
    InventoryCreate,
    InventoryUpdate
)
from app.services.waste_service import auto_expire_inventory

router = APIRouter(prefix="/inventory", tags=["Inventory"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_inventory(item: InventoryCreate, db: Session = Depends(get_db)):
    inventory = InventoryItem(**item.dict())
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory

@router.get("/")
def list_inventory(db: Session = Depends(get_db)):
    return db.query(InventoryItem).all()

@router.put("/{item_id}")
def update_inventory(
    item_id: int,
    item: InventoryUpdate,
    db: Session = Depends(get_db)
):
    inventory = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Item not found")

    for key, value in item.dict(exclude_unset=True).items():
        setattr(inventory, key, value)

    db.commit()
    return inventory

@router.delete("/{item_id}")
def delete_inventory(item_id: int, db: Session = Depends(get_db)):
    inventory = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(inventory)
    db.commit()
    return {"message": "Inventory item deleted"}

@router.post("/auto-expire")
def auto_expire(db: Session = Depends(get_db)):
    return auto_expire_inventory(db)
