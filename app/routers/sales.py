from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.sales import SaleCreate
from app.services.sales_service import record_sale

router = APIRouter(prefix="/sales", tags=["Sales"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_sale(
    sale: SaleCreate,
    db: Session = Depends(get_db)
):
    try:
        record_sale(
            db=db,
            menu_item_id=sale.menu_item_id,
            quantity=sale.quantity
        )
        return {"message": "Sale recorded successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
