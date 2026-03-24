from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# CORS Configuration for the React applications
origins = [
    "http://localhost:5173", # Admin Panel
    "http://localhost:5174", # POS Panel
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(customers.router)
app.include_router(products.router)
app.include_router(transactions.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Current Account and POS Management System API"}
