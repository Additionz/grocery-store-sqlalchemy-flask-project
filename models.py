from db import db

class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    price = db.Column(db.Numeric(10,2))
    inventory = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    category = db.relationship("Category", back_populates="products")

    def __repr__(self):
        return f"<Table {self.__tablename__}>"

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    products = db.relationship("Product", back_populates="category")

    def __repr__(self):
        return f"<Table {self.__tablename__}>"

class Customer(db.Model):
    __tablename__ = "customer"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone_number = db.Column(db.String(100))

    def __repr__(self):
        return f"<Table {self.__tablename__}>"