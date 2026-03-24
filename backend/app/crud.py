from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from . import models, schemas

# Customer CRUD
def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_customer_by_email(db: Session, email: str):
    return db.query(models.Customer).filter(models.Customer.email == email).first()

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).offset(skip).limit(limit).all()

def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    try:
        db.commit()
        db.refresh(db_customer)
    except IntegrityError:
        db.rollback()
        raise ValueError("Customer with this email might already exist")
    return db_customer

def update_customer(db: Session, customer_id: int, customer: schemas.CustomerUpdate):
    db_customer = get_customer(db, customer_id)
    if db_customer:
        update_data = customer.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_customer, key, value)
        try:
            db.commit()
            db.refresh(db_customer)
        except IntegrityError:
            db.rollback()
            raise ValueError("Integrity Error while updating customer")
    return db_customer

def delete_customer(db: Session, customer_id: int):
    db_customer = get_customer(db, customer_id)
    if db_customer:
        db.delete(db_customer)
        db.commit()
    return db_customer


# Product CRUD
def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_product_by_barcode(db: Session, barcode: str):
    return db.query(models.Product).filter(models.Product.barcode == barcode).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    try:
        db.commit()
        db.refresh(db_product)
    except IntegrityError:
        db.rollback()
        raise ValueError("Product with this barcode already exists")
    return db_product

def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    db_product = get_product(db, product_id)
    if db_product:
        update_data = product.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        try:
            db.commit()
            db.refresh(db_product)
        except IntegrityError:
            db.rollback()
            raise ValueError("Integrity Error while updating product")
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product

# Transaction CRUD
def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_customer = get_customer(db, transaction.customer_id)
    if not db_customer:
        raise ValueError("Customer not found")

    # Start an explicit database transaction context
    # Usually SQLAlchemy sessions wrap things in transactions, but just being explicit on logic
    try:
        # Create transaction record
        db_transaction = models.Transaction(**transaction.model_dump())
        db.add(db_transaction)

        # Update customer balance
        # Depending on business logic:
        # debt: means customer owes money (increases balance if balance represents debt, or decreases if balance is positive credits)
        # Let's assume current_balance is positive when the customer has a credit with us, negative when they owe us.
        # Or: current_balance is their "debt" balance (positive means they owe us).
        # We need to make an assumption. Let's assume:
        # Debt -> increases current_balance (they owe more)
        # Credit -> decreases current_balance (they pay us)
        # Sale -> increases current_balance (they owe more, assuming they bought on credit. If paid in full, might be combined with a credit transaction or handled differently).
        # In typical setups, balance > 0 means they owe us.
        if transaction.transaction_type in [models.TransactionType.debt, models.TransactionType.sale]:
            db_customer.current_balance += transaction.amount
        elif transaction.transaction_type == models.TransactionType.credit:
            db_customer.current_balance -= transaction.amount

        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to process transaction: {str(e)}")
