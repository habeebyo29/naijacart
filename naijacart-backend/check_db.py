from app import app, db
from sqlalchemy import inspect


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