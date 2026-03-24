from fastapi import FastAPI
from . import models
from .database import engine
from .routers import customers, products, transactions

# Create all database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Current Account and POS Management System API",
    description="Backend API for managing customers, products, and transactions.",
    version="1.0.0"
)

# Include routers
app.include_router(customers.router)
app.include_router(products.router)
app.include_router(transactions.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Current Account and POS Management System API"}
