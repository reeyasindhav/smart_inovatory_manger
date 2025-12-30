from fastapi import FastAPI
from app.database import engine, Base

from app.models import inventory, menu, recipe, sales, transactions
from app.routers import chat, inventory, sales, menu, alerts, reports, recipe, purchase
from fastapi.middleware.cors import CORSMiddleware
from app.routers import ai_insights

app = FastAPI(title="Smart Inventory Manager")

Base.metadata.create_all(bind=engine)


# app = FastAPI(title="Smart Inventory Manager")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:3000",
#         "http://127.0.0.1:3000",
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(inventory.router)
app.include_router(menu.router)
app.include_router(sales.router)
app.include_router(alerts.router)
app.include_router(recipe.router)
app.include_router(purchase.router)
app.include_router(reports.router)
app.include_router(ai_insights.router)
app.include_router(chat.router)
@app.get("/")
def health_check():
    return {"status": "running"}
