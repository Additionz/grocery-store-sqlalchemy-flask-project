import csv
import sys
from models import Product, Category, Customer, Order, ProductOrder
from sqlalchemy import select, text, func
from app import app
from db import db
from random import randint
from datetime import datetime as dt
from datetime import timedelta



def main(query: str) -> None:
    match query.lower():
        case "create":
            create_database()
        case "drop":
            drop_database()
        case "import":
            import_data()
        case "order":
            num = input("Enter the amount of customers: ")
            order_num = input("Enter the amount of orders for that customer: ")
            create_order(num, order_num)
        case _:
            print("Enter a valid CLI. (Create/Drop/Import)")

def drop_database() -> None:
    try:
        app.app_context().push()
        db.drop_all()
        db.session.commit()
        print("All tables dropped!")
    except(Exception) as err:
        print(err)
    

def create_database() -> None:
    try:
        app.app_context().push()
        db.create_all()
        db.session.commit()
        print("Created all tables!")
    except(Exception) as err:
        print(err)

def import_data() -> None:
    # Importing products.csv file
    with open("products.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        app.app_context().push()
        for row in csv_reader:
            if line_count==0 : line_count+=1
            else:
                [name, price, inventory, category] = row
                statement = db.select(Category).where(Category.name == category)
                possible_category = db.session.execute(statement).scalar()

                if not possible_category:
                    category_obj = Category(name=category)
                    db.session.add(category_obj)
                else:
                    category_obj = possible_category

                product = Product(name=name, price=price, inventory=inventory, category=category_obj)
                db.session.add(product)

                line_count+=1
        db.session.commit()
        print(
            f"Product & Category session committed!\n"
            f"Added {line_count-1} rows to Product table."
        )

    # Importing customers.csv file
    with open("customers.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        app.app_context().push()
        for row in csv_reader:
            if line_count == 0 : line_count += 1
            else:
                [name, phone_number] = row
                customer = Customer(name=name, phone_number=phone_number)
                db.session.add(customer)
                line_count+=1
        db.session.commit()
        print(f"Customer session committed!\n"
            f"Added {line_count-1} rows to Customer table."
        )

def create_order(number, order_num):
    app.app_context().push()
    for i in range(int(number)):
        #dt.now(): current date and time
        # the date generated will be randomly generated in the past:
        # most recent = 1 day ago
        # oldest = 10 days, 15 hours and 45 minutes ago
        generate_date = dt.now() - timedelta(days=randint(1, 10), hours=randint(0, 15), minutes=randint(0, 45))

        # Gets a random customer from the database and create a customer
        stmt = db.select(Customer).order_by(func.random())
        random_customer = db.session.execute(stmt).scalar()
        my_order = Order(customer=random_customer, created=generate_date)
        db.session.add(my_order)

        # Gets a specified amount of products based on "order_num" from the database
        num_products = int(order_num)
        stmt = db.select(Product).order_by(func.random()).limit(num_products)
        random_products = db.session.execute(stmt).scalars().all()
        quantity_products = randint(1, 10)

        for i in range(num_products):
            create_pos = ProductOrder(product=random_products[i], quantity=quantity_products, order=my_order)
            db.session.add(create_pos)
    db.session.commit()
    print(f"Generated {order_num} order(s) for {number} customer(s)!")
        
if __name__ == "__main__":
    main(sys.argv[1])

"""Print all product objects from database"""
# session = Session()
# statement = select(Product)
# results = session.execute(statement)
# scalars() for multiple, scalar() for single
# for prod in results.scalars(): 
#     print(prod)

"""Print all product objects that are out of stock"""
# statement = select(Product).where(Product.inventory < 1)
# results = session.execute(statement)
# for prod in results.scalars():
#     print(prod.name)

