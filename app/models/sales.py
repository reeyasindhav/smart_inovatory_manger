from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    sold_at = Column(DateTime, server_default=func.now())
