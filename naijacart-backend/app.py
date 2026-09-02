from dotenv import load_dotenv

load_dotenv()


from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from models import (
    db,
    User,
    Product,
    Order,
)

from orders import orders_bp
from admin import admin_bp

import os
import secrets
import requests

from datetime import datetime, timedelta


# =========================================================
# PROJECT PATHS
# =========================================================

BACKEND_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_DIR = os.path.dirname(
    BACKEND_DIR
)

FRONTEND_DIR = os.path.join(
    PROJECT_DIR,
    "naijacart-frontend"
)

DATABASE_DIR = os.path.join(
    BACKEND_DIR,
    "database"
)

DATABASE_PATH = os.path.join(
    DATABASE_DIR,
    "naijacart.db"
)


# =========================================================
# CREATE DATABASE FOLDER
# =========================================================

os.makedirs(
    DATABASE_DIR,
    exist_ok=True
)


# =========================================================
# LOAD .ENV
# =========================================================

ENV_FILE = os.path.join(
    BACKEND_DIR,
    ".env"
)


def load_env_file():

    if not os.path.exists(ENV_FILE):

        print(".env file not found.")

        return

    try:

        with open(
            ENV_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:

                line = line.strip()

                if not line:
                    continue

                if line.startswith("#"):
                    continue

                if "=" not in line:
                    continue

                key, value = line.split(
                    "=",
                    1
                )

                key = key.strip()
                value = value.strip()

                if (
                    len(value) >= 2
                    and value[0] == '"'
                    and value[-1] == '"'
                ):

                    value = value[1:-1]

                if (
                    len(value) >= 2
                    and value[0] == "'"
                    and value[-1] == "'"
                ):

                    value = value[1:-1]

                os.environ.setdefault(
                    key,
                    value
                )

        print(".env loaded successfully.")

    except Exception as error:

        print(
            "Could not load .env file:",
            error
        )


load_env_file()


# =========================================================
# FLASK APP
# =========================================================

app = Flask(
    __name__,
    template_folder=FRONTEND_DIR,
    static_folder=FRONTEND_DIR,
    static_url_path="/naijacart-frontend"
)


# =========================================================
# FLASK CONFIGURATION
# =========================================================

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "naijacart-secret-key-2026"
)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///" + DATABASE_PATH
)

app.config[
    "SQLALCHEMY_TRACK_MODIFICATIONS"
] = False


# =========================================================
# BREVO API CONFIGURATION
# =========================================================

BREVO_API_KEY = os.getenv(
    "BREVO_API_KEY",
    ""
)

MAIL_FROM = os.getenv(
    "MAIL_FROM",
    ""
)

MAIL_FROM_NAME = os.getenv(
    "MAIL_FROM_NAME",
    "NaijaCart"
)


# =========================================================
# PAYSTACK CONFIGURATION
# =========================================================

PAYSTACK_SECRET_KEY = os.getenv(
    "PAYSTACK_SECRET_KEY",
    ""
)

PAYSTACK_PUBLIC_KEY = os.getenv(
    "PAYSTACK_PUBLIC_KEY",
    ""
)


# =========================================================
# DATABASE
# =========================================================

db.init_app(app)


# =========================================================
# BLUEPRINTS
# =========================================================

app.register_blueprint(
    orders_bp
)

app.register_blueprint(
    admin_bp
)


# =========================================================
# CREATE DATABASE TABLES + ADMIN SETUP
# =========================================================

with app.app_context():

    db.create_all()

    print(
        "NaijaCart database connected successfully!"
    )

    print(
        "DATABASE LOCATION:"
    )

    print(
        os.path.abspath(
            DATABASE_PATH
        )
    )


    # =====================================================
    # AUTOMATIC ADMIN SETUP
    # =====================================================

    admin_email = os.getenv(
        "ADMIN_EMAIL",
        ""
    ).strip().lower()


    if admin_email:

        admin_user = User.query.filter_by(
            email=admin_email
        ).first()


        if admin_user:

            if not admin_user.is_admin:

                admin_user.is_admin = True

                try:

                    db.session.commit()

                    print(
                        f"ADMIN SETUP: {admin_email} is now an admin."
                    )

                except Exception as error:

                    db.session.rollback()

                    print(
                        "ADMIN SETUP ERROR:",
                        error
                    )

            else:

                print(
                    f"ADMIN SETUP: {admin_email} is already an admin."
                )


        else:

            print(
                f"ADMIN SETUP: No user found for {admin_email}."
            )


    else:

        print(
            "ADMIN SETUP: ADMIN_EMAIL is not configured."
        )


# =========================================================
# SEND VERIFICATION EMAIL USING BREVO API
# =========================================================

def send_verification_email(
    recipient_email,
    verification_code
):

    # -----------------------------------------------------
    # CHECK BREVO API KEY
    # -----------------------------------------------------

    if not BREVO_API_KEY:

        print(
            "EMAIL ERROR: BREVO_API_KEY is missing."
        )

        return False


    # -----------------------------------------------------
    # CHECK SENDER EMAIL
    # -----------------------------------------------------

    if not MAIL_FROM:

        print(
            "EMAIL ERROR: MAIL_FROM is missing."
        )

        return False


    # -----------------------------------------------------
    # BREVO API URL
    # -----------------------------------------------------

    brevo_url = (
        "https://api.brevo.com/v3/smtp/email"
    )


    # -----------------------------------------------------
    # REQUEST HEADERS
    # -----------------------------------------------------

    headers = {

        "accept": "application/json",

        "api-key": BREVO_API_KEY,

        "content-type": "application/json"
    }


    # -----------------------------------------------------
    # EMAIL DATA
    # -----------------------------------------------------

    data = {

        "sender": {

            "name": MAIL_FROM_NAME,

            "email": MAIL_FROM
        },

        "to": [

            {
                "email": recipient_email
            }

        ],

        "subject":
            "Verify your NaijaCart account",

        "textContent": f"""
Hello,

Thank you for creating a NaijaCart account.

Your email verification code is:

{verification_code}

This code will expire in 10 minutes.

If you did not create a NaijaCart account, you can ignore this email.

Regards,

{MAIL_FROM_NAME}
Tech you want. Prices you'll love.
"""
    }


    # -----------------------------------------------------
    # SEND EMAIL
    # -----------------------------------------------------

    try:

        response = requests.post(
            brevo_url,
            headers=headers,
            json=data,
            timeout=15
        )


        # -------------------------------------------------
        # SUCCESS
        # -------------------------------------------------

        if response.status_code in [200, 201, 202]:

            print(
                "Verification email sent to:",
                recipient_email
            )

            return True


        # -------------------------------------------------
        # BREVO ERROR
        # -------------------------------------------------

        print(
            "BREVO EMAIL ERROR:"
        )

        print(
            "Status:",
            response.status_code
        )

        print(
            "Response:",
            response.text
        )

        return False


    except requests.exceptions.Timeout:

        print(
            "EMAIL ERROR: Brevo API request timed out."
        )

        return False


    except requests.exceptions.RequestException as error:

        print(
            "EMAIL ERROR:",
            error
        )

        return False


    except Exception as error:

        print(
            "EMAIL ERROR:",
            error
        )

        return False


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# CART
# =========================================================

@app.route("/cart")
def cart():

    return render_template(
        "cart.html"
    )


# =========================================================
# CHECKOUT
# =========================================================

@app.route("/checkout")
def checkout():

    return render_template(
        "checkout.html"
    )


# =========================================================
# REGISTER
# =========================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    # -----------------------------------------------------
    # SHOW REGISTER PAGE
    # -----------------------------------------------------

    if request.method == "GET":

        return render_template(
            "register.html"
        )


    # -----------------------------------------------------
    # GET FORM DATA
    # -----------------------------------------------------

    first_name = request.form.get(
        "first_name",
        ""
    ).strip()

    last_name = request.form.get(
        "last_name",
        ""
    ).strip()

    email = request.form.get(
        "email",
        ""
    ).strip().lower()

    phone = request.form.get(
        "phone",
        ""
    ).strip()

    state = request.form.get(
        "state",
        ""
    ).strip()

    address = request.form.get(
        "address",
        ""
    ).strip()

    password = request.form.get(
        "password",
        ""
    )

    confirm_password = request.form.get(
        "confirm_password",
        ""
    )


    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if not first_name:

        flash(
            "Please enter your first name.",
            "error"
        )

        return redirect(
            url_for("register")
        )


    if not last_name:

        flash(
            "Please enter your last name.",
            "error"
        )

        return redirect(
            url_for("register")
        )


    if not email:

        flash(
            "Please enter your email.",
            "error"
        )

        return redirect(
            url_for("register")
        )


    if not phone:

        flash(
            "Please enter your phone number.",
            "error"
        )

        return redirect(
            url_for("register")
        )


    if not state:

        flash(
            "Please select your state.",
            "error"
        )

        return redirect(
            url_for("register")
        )


    if not address:

        flash(
            "Please enter your delivery address.",
            "error"
        )

        return redirect(
            url_for("register")
        )


    if len(password) < 6:

        flash(
            "Password must be at least 6 characters.",
            "error"
        )

        return redirect(
            url_for("register")
        )


    if password != confirm_password:

        flash(
            "Passwords do not match.",
            "error"
        )

        return redirect(
            url_for("register")
        )


    # -----------------------------------------------------
    # CHECK EXISTING USER
    # -----------------------------------------------------

    existing_user = User.query.filter_by(
        email=email
    ).first()


    if existing_user:

        # -------------------------------------------------
        # EXISTING BUT NOT VERIFIED
        # -------------------------------------------------

        if not existing_user.email_verified:

            verification_code = (
                f"{secrets.randbelow(1000000):06d}"
            )


            existing_user.first_name = (
                first_name
            )

            existing_user.last_name = (
                last_name
            )

            existing_user.name = (
                f"{first_name} {last_name}"
            ).strip()

            existing_user.phone = (
                phone
            )

            existing_user.state = (
                state
            )

            existing_user.address = (
                address
            )

            existing_user.set_password(
                password
            )

            existing_user.verification_code = (
                verification_code
            )

            existing_user.verification_expires_at = (
                datetime.utcnow()
                + timedelta(minutes=10)
            )


            try:

                db.session.commit()

            except Exception as error:

                db.session.rollback()

                print(
                    "Verification update error:",
                    error
                )

                flash(
                    "Unable to update your account. Please try again.",
                    "error"
                )

                return redirect(
                    url_for("register")
                )


            email_sent = send_verification_email(
                existing_user.email,
                verification_code
            )


            if not email_sent:

                flash(
                    "Your account exists, but we could not send the verification email.",
                    "error"
                )

                return redirect(
                    url_for("register")
                )


            session["verification_user_id"] = (
                existing_user.id
            )


            flash(
                "A new verification code has been sent to your email.",
                "success"
            )


            return redirect(
                url_for("verify_email")
            )


        # -------------------------------------------------
        # EXISTING AND VERIFIED
        # -------------------------------------------------

        flash(
            "An account with this email already exists. Please sign in.",
            "error"
        )

        return redirect(
            url_for("login")
        )


    # -----------------------------------------------------
    # CREATE FULL NAME
    # -----------------------------------------------------

    full_name = (
        f"{first_name} {last_name}"
    ).strip()


    # -----------------------------------------------------
    # CREATE VERIFICATION CODE
    # -----------------------------------------------------

    verification_code = (
        f"{secrets.randbelow(1000000):06d}"
    )


    # -----------------------------------------------------
    # CREATE USER
    # -----------------------------------------------------

    user = User(

        first_name=first_name,

        last_name=last_name,

        name=full_name,

        email=email,

        phone=phone,

        state=state,

        address=address,

        is_admin=False,

        email_verified=False,

        verification_code=verification_code,

        verification_expires_at=(
            datetime.utcnow()
            + timedelta(minutes=10)
        )
    )


    # -----------------------------------------------------
    # HASH PASSWORD
    # -----------------------------------------------------

    user.set_password(
        password
    )


    # -----------------------------------------------------
    # SAVE USER TO DATABASE
    # -----------------------------------------------------

    try:

        db.session.add(
            user
        )

        db.session.commit()

        print(
            "========================================"
        )

        print(
            "NEW USER REGISTERED"
        )

        print(
            "USER ID:",
            user.id
        )

        print(
            "NAME:",
            user.name
        )

        print(
            "EMAIL:",
            user.email
        )

        print(
            "PHONE:",
            user.phone
        )

        print(
            "STATE:",
            user.state
        )

        print(
            "========================================"
        )


    except Exception as error:

        db.session.rollback()

        print(
            "Registration error:",
            error
        )

        flash(
            "Unable to create your account. Please try again.",
            "error"
        )

        return redirect(
            url_for("register")
        )


    # -----------------------------------------------------
    # SAVE VERIFICATION USER IN SESSION
    # -----------------------------------------------------

    session["verification_user_id"] = (
        user.id
    )


    # -----------------------------------------------------
    # SEND VERIFICATION EMAIL
    # -----------------------------------------------------

    email_sent = send_verification_email(
        email,
        verification_code
    )


    if not email_sent:

        flash(
            "Your account was created, but we could not send the verification email.",
            "error"
        )

        return redirect(
            url_for("verify_email")
        )


    # -----------------------------------------------------
    # SUCCESS
    # -----------------------------------------------------

    flash(
        "A verification code has been sent to your email.",
        "success"
    )


    return redirect(
        url_for("verify_email")
    )


# =========================================================
# VERIFY EMAIL
# =========================================================

@app.route(
    "/verify-email",
    methods=["GET", "POST"]
)
def verify_email():

    user_id = session.get(
        "verification_user_id"
    )


    if not user_id:

        flash(
            "Please register an account first.",
            "error"
        )

        return redirect(
            url_for("register")
        )


    user = db.session.get(
        User,
        user_id
    )


    if not user:

        session.pop(
            "verification_user_id",
            None
        )

        flash(
            "Verification session expired. Please register again.",
            "error"
        )

        return redirect(
            url_for("register")
        )


    if user.email_verified:

        session.pop(
            "verification_user_id",
            None
        )

        flash(
            "Your email is already verified. Please sign in.",
            "success"
        )

        return redirect(
            url_for("login")
        )


    if request.method == "GET":

        return render_template(
            "verify_email.html",
            email=user.email
        )


    code = request.form.get(
        "verification_code",
        ""
    ).strip()


    if not code:

        flash(
            "Please enter your verification code.",
            "error"
        )

        return redirect(
            url_for("verify_email")
        )


    if len(code) != 6 or not code.isdigit():

        flash(
            "Please enter the 6-digit verification code.",
            "error"
        )

        return redirect(
            url_for("verify_email")
        )


    if not user.verification_expires_at:

        flash(
            "Your verification code has expired. Please request a new one.",
            "error"
        )

        return redirect(
            url_for("verify_email")
        )


    if datetime.utcnow() > user.verification_expires_at:

        user.verification_code = None

        user.verification_expires_at = None


        try:

            db.session.commit()

        except Exception:

            db.session.rollback()


        flash(
            "Your verification code has expired. Please request a new one.",
            "error"
        )

        return redirect(
            url_for("verify_email")
        )


    if code != user.verification_code:

        flash(
            "Incorrect verification code.",
            "error"
        )

        return redirect(
            url_for("verify_email")
        )


    # -----------------------------------------------------
    # VERIFY USER
    # -----------------------------------------------------

    user.email_verified = True

    user.verification_code = None

    user.verification_expires_at = None


    try:

        db.session.commit()

    except Exception as error:

        db.session.rollback()

        print(
            "Email verification error:",
            error
        )

        flash(
            "Unable to verify your email. Please try again.",
            "error"
        )

        return redirect(
            url_for("verify_email")
        )


    session.pop(
        "verification_user_id",
        None
    )


    flash(
        "Email verified successfully! You can now sign in.",
        "success"
    )


    return redirect(
        url_for("login")
    )


# =========================================================
# RESEND VERIFICATION
# =========================================================

@app.route(
    "/resend-verification",
    methods=["POST"]
)
def resend_verification():

    user_id = session.get(
        "verification_user_id"
    )


    if not user_id:

        flash(
            "Please register first.",
            "error"
        )

        return redirect(
            url_for("register")
        )


    user = db.session.get(
        User,
        user_id
    )


    if not user:

        session.pop(
            "verification_user_id",
            None
        )

        flash(
            "User not found. Please register again.",
            "error"
        )

        return redirect(
            url_for("register")
        )


    if user.email_verified:

        session.pop(
            "verification_user_id",
            None
        )

        flash(
            "Your email is already verified.",
            "success"
        )

        return redirect(
            url_for("login")
        )


    verification_code = (
        f"{secrets.randbelow(1000000):06d}"
    )


    user.verification_code = (
        verification_code
    )

    user.verification_expires_at = (
        datetime.utcnow()
        + timedelta(minutes=10)
    )


    try:

        db.session.commit()

    except Exception as error:

        db.session.rollback()

        print(
            "Resend verification error:",
            error
        )

        flash(
            "Unable to generate a new verification code.",
            "error"
        )

        return redirect(
            url_for("verify_email")
        )


    email_sent = send_verification_email(
        user.email,
        verification_code
    )


    if not email_sent:

        flash(
            "We could not send the verification email.",
            "error"
        )

        return redirect(
            url_for("verify_email")
        )


    flash(
        "A new verification code has been sent.",
        "success"
    )


    return redirect(
        url_for("verify_email")
    )


# =========================================================
# LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "GET":

        return render_template(
            "signin.html"
        )


    email = request.form.get(
        "email",
        ""
    ).strip().lower()

    password = request.form.get(
        "password",
        ""
    )


    if not email or not password:

        flash(
            "Please enter your email and password.",
            "error"
        )

        return redirect(
            url_for("login")
        )


    user = User.query.filter_by(
        email=email
    ).first()


    if not user:

        flash(
            "Invalid email or password.",
            "error"
        )

        return redirect(
            url_for("login")
        )


    if not user.check_password(
        password
    ):

        flash(
            "Invalid email or password.",
            "error"
        )

        return redirect(
            url_for("login")
        )


    if not user.email_verified:

        if user.verification_code:

            session["verification_user_id"] = (
                user.id
            )

            flash(
                "Please verify your email before signing in.",
                "error"
            )

            return redirect(
                url_for("verify_email")
            )


    # -----------------------------------------------------
    # CREATE LOGIN SESSION
    # -----------------------------------------------------

    session["user_id"] = user.id

    session["user_name"] = user.name

    session["user_email"] = user.email

    session["is_admin"] = user.is_admin


    flash(
        f"Welcome back, {user.name}!",
        "success"
    )


    # -----------------------------------------------------
    # ADMIN REDIRECT
    # -----------------------------------------------------

    if user.is_admin:

        return redirect(
            url_for("admin.dashboard")
        )


    # -----------------------------------------------------
    # CUSTOMER REDIRECT
    # -----------------------------------------------------

    return redirect(
        url_for("home")
    )


# =========================================================
# MY ACCOUNT
# =========================================================

@app.route("/account")
def account():

    user_id = session.get(
        "user_id"
    )


    if not user_id:

        return redirect(
            url_for("login")
        )


    user = db.session.get(
        User,
        user_id
    )


    if not user:

        session.clear()

        flash(
            "Your session has expired. Please sign in again.",
            "error"
        )

        return redirect(
            url_for("login")
        )


    orders = Order.query.filter_by(
        user_id=user.id
    ).all()


    total_orders = len(
        orders
    )


    pending_orders = sum(
        1
        for order in orders
        if order.status.lower() == "pending"
    )


    completed_orders = sum(
        1
        for order in orders
        if order.status.lower() == "completed"
    )


    return render_template(
        "account.html",
        user=user,
        orders=orders,
        total_orders=total_orders,
        pending_orders=pending_orders,
        completed_orders=completed_orders
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(
        url_for("login")
    )


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )