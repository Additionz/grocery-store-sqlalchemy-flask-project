import csv
import sys
from database import Session, engine
from models import Product, Base, Category, Customer
from sqlalchemy import select


def main(query: str):
    match query.lower():
        case "create":
            create_database()
        case "drop":
            drop_database()
        case "import":
            import_data()
        case _:
            print("Enter a valid CLI. (Create/Drop/Import)")

def drop_database():
    try: 
        Base.metadata.drop_all(engine)
        print("All tables dropped!")
    except(Exception) as err:
        print(err)
    

def create_database():
    try:
        Base.metadata.create_all(engine)
        print("Created all tables!")
    except(Exception) as err:
        print(err)

def import_data():
    # Importing products.csv file
    with open("products.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        session = Session()
        for row in csv_reader:
            if line_count==0 : line_count+=1
            else:
                [name, price, inventory, category] = row
                possible_category = session.execute(select(Category).where(Category.name == category)).scalar()

                if not possible_category:
                    category_obj = Category(name=category)
                    session.add(category_obj)
                else:
                    category_obj = possible_category

                product = Product(name=name, price=price, inventory=inventory, category=category_obj)
                session.add(product)
                line_count+=1
        session.commit()
        print(
            f"Product & Category session committed!\n"
            f"Added {line_count-1} rows to Product table."
        )

    # Importing customers.csv file
    with open("customers.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        session = Session()
        for row in csv_reader:
            if line_count == 0 : line_count += 1
            else:
                [name, phone_number] = row
                customer = Customer(name=name, phone_number=phone_number)
                session.add(customer)
                line_count+=1
        session.commit()
        print(f"Customer session committed!\n"
            f"Added {line_count-1} rows to Customer table."
        )
        

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

