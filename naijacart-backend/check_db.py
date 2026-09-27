from app import app, db
from sqlalchemy import inspect, text


with app.app_context():

    inspector = inspect(db.engine)

    print("\nTABLES")
    print("=" * 40)

    for table in inspector.get_table_names():
        print(table)

    print("\nPRODUCT COLUMNS")
    print("=" * 40)

    for column in inspector.get_columns("products"):
        print(column["name"])

    print("\nDATA COUNTS")
    print("=" * 40)

    tables = [
        "users",
        "products",
        "categories",
        "orders",
        "order_items",
        "reviews",
        "cart",
        "cart_items",
        "wishlist"
    ]

    for table in tables:
        result = db.session.execute(
            text(f"SELECT COUNT(*) FROM {table}")
        ).scalar()

        print(f"{table}: {result}")