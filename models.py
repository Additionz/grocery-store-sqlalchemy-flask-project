from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship
from sqlalchemy import String, DECIMAL, Integer, ForeignKey

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "product"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    price = mapped_column(DECIMAL(10, 2))
    inventory = mapped_column(Integer, default=0)
    category_id = mapped_column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")

class Category(Base):
    __tablename__ = "categories"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    products = relationship("Product", back_populates="category")

class Customer(Base):
    __tablename__ = "customer"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    phone_number = mapped_column(String)