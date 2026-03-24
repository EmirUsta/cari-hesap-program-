from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, text
from sqlalchemy.orm import relationship
import enum
from .database import Base
from datetime import datetime, timezone

class TransactionType(str, enum.Enum):
    debt = "debt"
    credit = "credit"
    sale = "sale"

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True, nullable=False)
    phone = Column(String, index=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
    current_balance = Column(Float, default=0.0, nullable=False)

    transactions = relationship("Transaction", back_populates="customer")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    barcode = Column(String, unique=True, index=True, nullable=False)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0, nullable=False)

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    customer = relationship("Customer", back_populates="transactions")
