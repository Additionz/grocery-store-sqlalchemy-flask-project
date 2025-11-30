from pathlib import Path
from flask import Flask, redirect, render_template, request, url_for
from models import Product, Category, Customer
from sqlalchemy import select, text
from db import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"

app.instance_path = Path(".").resolve()

db.init_app(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/products")
def product():
    stmt = db.select(Product)
    product = db.session.execute(stmt).scalars()
    return render_template("products.html", products=product)


@app.route("/categories")
def category():
    stmt = db.select(Category)
    category = db.session.execute(stmt).scalars()
    return render_template("categories.html", categories=category)

@app.route("/categories/<string:name>")
def category_detail(name):
    stmt = db.select(Category).where(Category.name == name)
    cat = db.session.execute(stmt).scalar()
    stmt2 = db.select(Product).where(Product.category.has(Category.id == cat.id))
    product = db.session.execute(stmt2).scalars()
    return render_template("products.html", products=product)

@app.route("/customers", methods=["GET", "POST"])
def customer():
    if request.method == "POST":
        id = request.form['id']
        return redirect(url_for('customer_detail', id=id))
    
    stmt = db.select(Customer)
    customer = db.session.execute(stmt).scalars()
    return render_template("customers.html", customers=customer)

@app.route("/customers/<int:id>", methods=["GET"])
def customer_detail(id):
    stmt = db.select(Customer).where(Customer.id == id)
    customer = db.session.execute(stmt).scalars()
    return render_template("customers.html", customers=customer)
    
if __name__ == "__main__":
    app.run(debug=True, port=8888)