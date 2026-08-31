from sqlalchemy import inspect, text
from app import app
from models import db


# =========================================================
# MIGRATE USERS TABLE
# =========================================================

with app.app_context():

    inspector = inspect(db.engine)

    existing_columns = {
        column["name"]
        for column in inspector.get_columns("users")
    }

    print("\n========================================")
    print("N A I J A C A R T")
    print("Users Database Migration")
    print("========================================\n")

    print("Existing columns:")
    print(existing_columns)
    print()

    # -----------------------------------------------------
    # COLUMNS REQUIRED BY CURRENT USER MODEL
    # -----------------------------------------------------

    columns_to_add = {

        "first_name":
            "VARCHAR(50) NOT NULL DEFAULT ''",

        "last_name":
            "VARCHAR(50) NOT NULL DEFAULT ''",

        "phone":
            "VARCHAR(30)",

        "address":
            "TEXT",

        "state":
            "VARCHAR(100)",

        "email_verified":
            "BOOLEAN NOT NULL DEFAULT 0",

        "verification_code":
            "VARCHAR(6)",

        "verification_expires_at":
            "DATETIME",

        "updated_at":
            "DATETIME"

    }

    # -----------------------------------------------------
    # ADD MISSING COLUMNS
    # -----------------------------------------------------

    for column_name, column_definition in columns_to_add.items():

        if column_name not in existing_columns:

            print(
                f"Adding missing column: {column_name}"
            )

            db.session.execute(
                text(
                    f"""
                    ALTER TABLE users
                    ADD COLUMN {column_name}
                    {column_definition}
                    """
                )
            )

        else:

            print(
                f"Already exists: {column_name}"
            )

    # -----------------------------------------------------
    # SAVE CHANGES
    # -----------------------------------------------------

    db.session.commit()

    print("\nDatabase migration completed successfully.")

    # -----------------------------------------------------
    # UPDATE FIRST/LAST NAME FROM EXISTING NAME
    # -----------------------------------------------------

    try:

        users = db.session.execute(
            text(
                """
                SELECT id, name
                FROM users
                """
            )
        ).fetchall()

        for user_id, name in users:

            if name:

                parts = name.strip().split(
                    " ",
                    1
                )

                first_name = parts[0]

                last_name = (
                    parts[1]
                    if len(parts) > 1
                    else ""
                )

                db.session.execute(
                    text(
                        """
                        UPDATE users
                        SET
                            first_name = :first_name,
                            last_name = :last_name
                        WHERE id = :user_id
                        """
                    ),
                    {
                        "first_name": first_name,
                        "last_name": last_name,
                        "user_id": user_id
                    }
                )

        db.session.commit()

        print(
            "Existing names copied into first_name and last_name."
        )

    except Exception as error:

        db.session.rollback()

        print(
            "Name migration warning:",
            error
        )

    # -----------------------------------------------------
    # SHOW FINAL COLUMNS
    # -----------------------------------------------------

    inspector = inspect(db.engine)

    final_columns = [
        column["name"]
        for column in inspector.get_columns("users")
    ]

    print("\n========================================")
    print("Final users table columns:")
    print("========================================")

    for column in final_columns:

        print(
            f"✓ {column}"
        )

    print("\n========================================")
    print("Migration finished.")
    print("========================================\n")