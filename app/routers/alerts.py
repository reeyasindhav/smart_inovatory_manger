from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.alert_service import get_low_stock_items

router = APIRouter(prefix="/alerts", tags=["Alerts"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/low-stock")
def low_stock_alerts(db: Session = Depends(get_db)):
    items = get_low_stock_items(db)
    return {
        "count": len(items),
        "items": [
            {
                "id": item.id,
                "name": item.name,
                "current_stock": item.current_stock,
                "reorder_level": item.reorder_level
            }
            for item in items
        ]
    }
