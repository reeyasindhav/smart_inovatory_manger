from fastapi import FastAPI

app = FastAPI(title="Smart Inventory Manager")

@app.get("/")
def health_check():
    return {"status": "running"}
