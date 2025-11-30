from db import db
from sqlalchemy import func

class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    price = db.Column(db.DECIMAL(10,2))
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
    orders = db.relationship("Order", back_populates="customer", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Table {self.__tablename__}>"
    
    def list_orders(self):
        complete = []
        pending = []
        for order in self.orders:
            if order.completed != None:
                complete.append(order)
            else:
                pending.append(order)
        return [complete, pending]
    
class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=db.func.now())
    completed = db.Column(db.DateTime, nullable=True, default=None)
    amount = db.Column(db.DECIMAL(6,2), nullable=True, default=None)
    items = db.relationship("ProductOrder", back_populates="order")
    customer_id = db.Column(db.ForeignKey("customer.id"), nullable=False)
    customer = db.relationship("Customer", back_populates="orders")

    def estimate(self):
        total = 0
        for po in self.items:
          one = po.product.price * po.quantity
          total = total + one
        return total
    
    def complete(self):
        for po in self.items:
            if po.quantity <= po.product.inventory:
                po.product.inventory -= po.quantity
            else:
                raise ValueError("Not enough inventory")
        self.completed = db.func.now()
        self.amount = self.estimate()

class ProductOrder(db.Model):
    __tablename__ = "product_orders"

    product_id = db.mapped_column(db.ForeignKey("product.id"), primary_key=True)
    order_id = db.mapped_column(db.ForeignKey("orders.id"), primary_key=True)
    quantity = db.mapped_column(db.Integer, nullable=False)
    product = db.relationship("Product")
    order = db.relationship("Order", back_populates="items")

    def check(self):
        if self.quantity <= self.product.inventory:
            return self.quantity
        else:
            return f"{str(self.quantity)}, not enough stock to complete the order!"