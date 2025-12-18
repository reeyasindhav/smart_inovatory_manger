from sqlalchemy import Column, Integer, Float, ForeignKey
from app.database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
    inventory_item_id = Column(Integer, ForeignKey("inventory_items.id"))
    quantity_used = Column(Float, nullable=False)
