from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
