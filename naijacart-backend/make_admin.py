from app import app
from models import db, User


with app.app_context():

    email = input("Enter your admin email: ").strip().lower()

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:

        print("User not found.")

    else:

        user.is_admin = True

        db.session.commit()

        print(
            f"{user.email} is now an admin!"
        )