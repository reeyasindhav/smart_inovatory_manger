from fastapi import FastAPI
from app.database import engine, Base

from app.models import (
    inventory,
    menu,
    recipe,
    sales,
    transactions
)

app = FastAPI(title="Smart Inventory Manager")

Base.metadata.create_all(bind=engine)

@app.get("/")
def health_check():
    return {"status": "running"}
