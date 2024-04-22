from sqlalchemy import Column, Integer, String, Enum, Date, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.config.database import Base
from enum import Enum as UserEnum


class Role(UserEnum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(Enum(Role), default=Role.USER)


class MaterialPurchase(Base):
    __tablename__ = "material_purchase"

    id = Column(Integer, primary_key=True)
    purchase_date = Column(Date)
    document_number = Column(String)
    material_name = Column(String, ForeignKey("storage.material_name"))
    quantity = Column(Integer)
    price = Column(Float)
    total_price = Column(Float)

    storage = relationship("Storage", back_populates="purchase")


class MaterialExpenses(Base):
    __tablename__ = "material_expenses"

    id = Column(Integer, primary_key=True)
    product_id = Column(String)
    product_name = Column(String, ForeignKey("sales.product_id"))
    material_name = Column(String, ForeignKey("storage.material_name"))
    quantity = Column(Integer)
    total_material_price = Column(Float)

    purchase = relationship("Storage", back_populates="expenses")
    sales = relationship("Sales", back_populates="expenses_entry")


class Sales(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    document_number = Column(String)
    product_id = Column(String, unique=True)
    product_name = Column(String)
    quantity = Column(Integer)
    expenses = Column(Float)
    gain_percentage = Column(Integer)
    income = Column(Float)
    net_profit = Column(Float)

    expenses_entry = relationship("MaterialExpenses", back_populates="sales")


class Storage(Base):
    __tablename__ = "storage"

    id = Column(Integer, primary_key=True)
    material_name = Column(String, unique=True)
    total_quantity = Column(Integer)
    avg_price = Column(Float)
    remain = Column(Integer)

    purchase = relationship("MaterialPurchase", back_populates="storage")
    expenses = relationship("MaterialExpenses", back_populates="purchase")
