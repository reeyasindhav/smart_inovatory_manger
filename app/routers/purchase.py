from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.purchase import PurchaseCreate
from app.services.purchase_service import purchase_inventory

router = APIRouter(prefix="/purchase", tags=["Purchase"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def purchase_item(
    purchase: PurchaseCreate,
    db: Session = Depends(get_db)
):
    try:
        item = purchase_inventory(
            db=db,
            inventory_item_id=purchase.inventory_item_id,
            quantity=purchase.quantity
        )
        return {
            "message": "Stock purchased successfully",
            "item": {
                "id": item.id,
                "name": item.name,
                "current_stock": item.current_stock
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
