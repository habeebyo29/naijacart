from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


# =========================================================
# USER MODEL
# =========================================================

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # -----------------------------------------------------
    # PERSONAL INFORMATION
    # -----------------------------------------------------

    first_name = db.Column(
        db.String(50),
        nullable=False
    )

    last_name = db.Column(
        db.String(50),
        nullable=False
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    # -----------------------------------------------------
    # CONTACT INFORMATION
    # -----------------------------------------------------

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False,
        index=True
    )

    phone = db.Column(
        db.String(30),
        nullable=True
    )

    # -----------------------------------------------------
    # DELIVERY INFORMATION
    # -----------------------------------------------------

    address = db.Column(
        db.Text,
        nullable=True
    )

    state = db.Column(
        db.String(100),
        nullable=True
    )

    # -----------------------------------------------------
    # PASSWORD
    # -----------------------------------------------------

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    # -----------------------------------------------------
    # ACCOUNT / ADMIN
    # -----------------------------------------------------

    is_admin = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    token = db.Column(
        db.String(255),
        nullable=True
    )

    # -----------------------------------------------------
    # EMAIL VERIFICATION
    # -----------------------------------------------------

    email_verified = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    verification_code = db.Column(
        db.String(6),
        nullable=True
    )

    verification_expires_at = db.Column(
        db.DateTime,
        nullable=True
    )

    # -----------------------------------------------------
    # DATES
    # -----------------------------------------------------

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now(),
        nullable=False
    )

    # -----------------------------------------------------
    # RELATIONSHIPS
    # -----------------------------------------------------

    cart = db.relationship(
        "Cart",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    orders = db.relationship(
        "Order",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    wishlist = db.relationship(
        "Wishlist",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    reviews = db.relationship(
        "Review",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # -----------------------------------------------------
    # PASSWORD METHODS
    # -----------------------------------------------------

    def set_password(self, password):

        self.password_hash = generate_password_hash(
            password
        )

    def check_password(self, password):

        return check_password_hash(
            self.password_hash,
            password
        )

    # -----------------------------------------------------
    # FULL NAME
    # -----------------------------------------------------

    def update_full_name(self):

        self.name = (
            f"{self.first_name} {self.last_name}"
        ).strip()

    # -----------------------------------------------------
    # REPRESENTATION
    # -----------------------------------------------------

    def __repr__(self):

        return f"<User {self.email}>"


# =========================================================
# CATEGORY MODEL
# =========================================================

class Category(db.Model):

    __tablename__ = "categories"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    image_url = db.Column(
        db.String(500),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # -----------------------------------------------------
    # RELATIONSHIPS
    # -----------------------------------------------------

    products = db.relationship(
        "Product",
        back_populates="category_relation"
    )

    # -----------------------------------------------------
    # REPRESENTATION
    # -----------------------------------------------------

    def __repr__(self):

        return f"<Category {self.name}>"


# =========================================================
# PRODUCT MODEL
# =========================================================

class Product(db.Model):

    __tablename__ = "products"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(200),
        nullable=False
    )

    brand = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    old_price = db.Column(
        db.Float,
        nullable=True
    )

    discount = db.Column(
        db.Integer,
        nullable=True
    )

    rating = db.Column(
        db.Float,
        nullable=True
    )

    # -----------------------------------------------------
    # CATEGORY
    # -----------------------------------------------------

    category = db.Column(
        db.String(100),
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=True
    )

    # -----------------------------------------------------
    # PRODUCT IMAGE
    # -----------------------------------------------------

    image_url = db.Column(
        db.String(500),
        nullable=True
    )

    # -----------------------------------------------------
    # STOCK
    # -----------------------------------------------------

    stock = db.Column(
        db.Integer,
        default=10,
        nullable=False
    )

    # -----------------------------------------------------
    # DATE
    # -----------------------------------------------------

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # -----------------------------------------------------
    # RELATIONSHIPS
    # -----------------------------------------------------

    category_relation = db.relationship(
        "Category",
        back_populates="products"
    )

    cart_items = db.relationship(
        "CartItem",
        back_populates="product",
        cascade="all, delete-orphan"
    )

    order_items = db.relationship(
        "OrderItem",
        back_populates="product"
    )

    wishlist_items = db.relationship(
        "Wishlist",
        back_populates="product",
        cascade="all, delete-orphan"
    )

    reviews = db.relationship(
        "Review",
        back_populates="product",
        cascade="all, delete-orphan"
    )

    # -----------------------------------------------------
    # REPRESENTATION
    # -----------------------------------------------------

    def __repr__(self):

        return f"<Product {self.name}>"


# =========================================================
# CART MODEL
# =========================================================

class Cart(db.Model):

    __tablename__ = "cart"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    # -----------------------------------------------------
    # RELATIONSHIPS
    # -----------------------------------------------------

    user = db.relationship(
        "User",
        back_populates="cart"
    )

    items = db.relationship(
        "CartItem",
        back_populates="cart",
        cascade="all, delete-orphan"
    )

    # -----------------------------------------------------
    # REPRESENTATION
    # -----------------------------------------------------

    def __repr__(self):

        return f"<Cart {self.id}>"


# =========================================================
# CART ITEM MODEL
# =========================================================

class CartItem(db.Model):

    __tablename__ = "cart_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    cart_id = db.Column(
        db.Integer,
        db.ForeignKey("cart.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        default=1,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # -----------------------------------------------------
    # RELATIONSHIPS
    # -----------------------------------------------------

    cart = db.relationship(
        "Cart",
        back_populates="items"
    )

    product = db.relationship(
        "Product",
        back_populates="cart_items"
    )

    # -----------------------------------------------------
    # REPRESENTATION
    # -----------------------------------------------------

    def __repr__(self):

        return f"<CartItem {self.id}>"


# =========================================================
# ORDER MODEL
# =========================================================

class Order(db.Model):

    __tablename__ = "orders"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    total = db.Column(
        db.Float,
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default="Pending",
        nullable=False
    )

    # -----------------------------------------------------
    # PAYMENT
    # -----------------------------------------------------

    payment_ref = db.Column(
        db.String(255),
        nullable=True
    )

    # -----------------------------------------------------
    # DELIVERY
    # -----------------------------------------------------

    delivery_address = db.Column(
        db.Text,
        nullable=False
    )

    phone = db.Column(
        db.String(30),
        nullable=False
    )

    # -----------------------------------------------------
    # DATE
    # -----------------------------------------------------

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # -----------------------------------------------------
    # RELATIONSHIPS
    # -----------------------------------------------------

    user = db.relationship(
        "User",
        back_populates="orders"
    )

    items = db.relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )

    # -----------------------------------------------------
    # REPRESENTATION
    # -----------------------------------------------------

    def __repr__(self):

        return f"<Order {self.id}>"


# =========================================================
# ORDER ITEM MODEL
# =========================================================

class OrderItem(db.Model):

    __tablename__ = "order_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    # Price at the time the order was placed
    price = db.Column(
        db.Float,
        nullable=False
    )

    # -----------------------------------------------------
    # RELATIONSHIPS
    # -----------------------------------------------------

    order = db.relationship(
        "Order",
        back_populates="items"
    )

    product = db.relationship(
        "Product",
        back_populates="order_items"
    )

    # -----------------------------------------------------
    # REPRESENTATION
    # -----------------------------------------------------

    def __repr__(self):

        return f"<OrderItem {self.id}>"


# =========================================================
# WISHLIST MODEL
# =========================================================

class Wishlist(db.Model):

    __tablename__ = "wishlist"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # -----------------------------------------------------
    # RELATIONSHIPS
    # -----------------------------------------------------

    user = db.relationship(
        "User",
        back_populates="wishlist"
    )

    product = db.relationship(
        "Product",
        back_populates="wishlist_items"
    )

    # -----------------------------------------------------
    # PREVENT DUPLICATE WISHLIST ITEMS
    # -----------------------------------------------------

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "product_id",
            name="unique_user_product_wishlist"
        ),
    )

    # -----------------------------------------------------
    # REPRESENTATION
    # -----------------------------------------------------

    def __repr__(self):

        return f"<Wishlist {self.id}>"


# =========================================================
# REVIEW MODEL
# =========================================================

class Review(db.Model):

    __tablename__ = "reviews"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # Store the name used when review was created
    user_name = db.Column(
        db.String(100),
        nullable=False
    )

    rating = db.Column(
        db.Integer,
        nullable=False
    )

    comment = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # -----------------------------------------------------
    # RELATIONSHIPS
    # -----------------------------------------------------

    product = db.relationship(
        "Product",
        back_populates="reviews"
    )

    user = db.relationship(
        "User",
        back_populates="reviews"
    )

    # -----------------------------------------------------
    # ONE REVIEW PER USER PER PRODUCT
    # -----------------------------------------------------

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "product_id",
            name="unique_user_product_review"
        ),
    )

    # -----------------------------------------------------
    # REPRESENTATION
    # -----------------------------------------------------

    def __repr__(self):

        return f"<Review {self.id}>"