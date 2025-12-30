from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.insight_service import  get_all_insights


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/ai/insights", tags=["AI Insights"])

@router.get("/all")
def all_insights(db: Session = Depends(get_db)):
    return get_all_insights(db)