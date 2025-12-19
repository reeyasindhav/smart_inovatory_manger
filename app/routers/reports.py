from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.report_service import ingredient_usage_report, sales_summary_report, purchase_summary_report

router = APIRouter(prefix="/reports", tags=["Reports"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/ingredient-usage")
def ingredient_usage(days: int = 7, db: Session = Depends(get_db)):
    data = ingredient_usage_report(db, days)
    return [
        {
            "ingredient": row.name,
            "used_quantity": row.used_quantity
        }
        for row in data
    ]


@router.get("/sales-summary")
def sales_summary(days: int = 7, db: Session = Depends(get_db)):
    data = sales_summary_report(db, days)
    return [
        {
            "menu_item": row.name,
            "quantity_sold": row.total_quantity,
            "revenue": row.total_revenue
        }
        for row in data
    ]


@router.get("/purchase-summary")
def purchase_summary(days: int = 7, db: Session = Depends(get_db)):
    data = purchase_summary_report(db, days)
    return [
        {
            "ingredient": row.name,
            "purchased_quantity": row.purchased_quantity
        }
        for row in data
    ]
