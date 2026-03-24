from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from .models import TransactionType

# Customer Schemas
class CustomerBase(BaseModel):
    full_name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    current_balance: float = 0.0

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    current_balance: Optional[float] = None

from pydantic import ConfigDict

class Customer(CustomerBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# Product Schemas
class ProductBase(BaseModel):
    name: str
    barcode: str
    price: float
    stock_quantity: int = 0

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    barcode: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None

class Product(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# Transaction Schemas
class TransactionBase(BaseModel):
    customer_id: int
    transaction_type: TransactionType
    amount: float
    description: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
