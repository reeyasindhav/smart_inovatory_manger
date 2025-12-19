from pydantic import BaseModel
from typing import Optional

class MenuCreate(BaseModel):
    name: str
    price: float

class MenuUpdate(BaseModel):
    price: Optional[float] = None
    is_active: Optional[bool] = None

class MenuResponse(BaseModel):
    id: int
    name: str
    price: float
    is_active: bool

    class Config:
        orm_mode = True
