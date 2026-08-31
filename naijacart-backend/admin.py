from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify
)

from models import (
    db,
    User,
    Product,
    Order,
    OrderItem
)

from functools import wraps


# =========================================================
# ADMIN BLUEPRINT
# =========================================================

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


# =========================================================
# ADMIN AUTHENTICATION
# =========================================================

def admin_required(function):

    @wraps(function)
    def decorated_function(*args, **kwargs):

        user_id = session.get("user_id")

        if not user_id:

            flash(
                "Please sign in as an administrator.",
                "error"
            )

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

        if not user.is_admin:

            flash(
                "Administrator access required.",
                "error"
            )

            return redirect(
                url_for("home")
            )

        return function(*args, **kwargs)

    return decorated_function


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@admin_bp.route("/")
@admin_required
def dashboard():

    total_users = User.query.count()

    total_products = Product.query.count()

    total_orders = Order.query.count()

    pending_orders = Order.query.filter(
        db.func.lower(Order.status) == "pending"
    ).count()

    paid_orders = Order.query.filter(
        db.func.lower(Order.status) == "paid"
    ).count()

    processing_orders = Order.query.filter(
        db.func.lower(Order.status) == "processing"
    ).count()

    shipped_orders = Order.query.filter(
        db.func.lower(Order.status) == "shipped"
    ).count()

    delivered_orders = Order.query.filter(
        db.func.lower(Order.status) == "delivered"
    ).count()

    cancelled_orders = Order.query.filter(
        db.func.lower(Order.status) == "cancelled"
    ).count()

    total_customers = User.query.filter_by(
        is_admin=False
    ).count()

    total_admins = User.query.filter_by(
        is_admin=True
    ).count()

    recent_orders = (
        Order.query
        .order_by(Order.created_at.desc())
        .limit(10)
        .all()
    )

    return render_template(
        "dashboard.html",

        total_users=total_users,

        total_products=total_products,

        total_orders=total_orders,

        pending_orders=pending_orders,

        paid_orders=paid_orders,

        processing_orders=processing_orders,

        shipped_orders=shipped_orders,

        delivered_orders=delivered_orders,

        cancelled_orders=cancelled_orders,

        total_customers=total_customers,

        total_admins=total_admins,

        recent_orders=recent_orders
    )


# =========================================================
# PRODUCTS PAGE
# =========================================================

@admin_bp.route("/products")
@admin_required
def products():

    return render_template(
        "products.html"
    )


# =========================================================
# PRODUCTS DATA
# =========================================================

@admin_bp.route("/products/data")
@admin_required
def products_data():

    products = Product.query.order_by(
        Product.id.desc()
    ).all()

    product_list = []

    for product in products:

        product_list.append({

            "id": product.id,

            "name": getattr(
                product,
                "name",
                ""
            ),

            "description": getattr(
                product,
                "description",
                ""
            ),

            "price": float(
                getattr(
                    product,
                    "price",
                    0
                ) or 0
            ),

            "category": getattr(
                product,
                "category",
                ""
            ),

            "brand": getattr(
                product,
                "brand",
                ""
            ),

            "old_price": float(
                getattr(
                    product,
                    "old_price",
                    0
                ) or 0
            ),

            "discount": float(
                getattr(
                    product,
                    "discount",
                    0
                ) or 0
            ),

            "image_url": getattr(
                product,
                "image_url",
                ""
            ),

            "stock": int(
                getattr(
                    product,
                    "stock",
                    0
                ) or 0
            )
        })

    return jsonify({

        "success": True,

        "products": product_list

    })


# =========================================================
# ADD PRODUCT
# =========================================================

@admin_bp.route(
    "/products/add",
    methods=["GET", "POST"]
)
@admin_required
def add_product():

    if request.method == "GET":

        return render_template(
            "add_product.html"
        )

    name = request.form.get(
        "name",
        ""
    ).strip()

    description = request.form.get(
        "description",
        ""
    ).strip()

    category = request.form.get(
        "category",
        ""
    ).strip()

    image_url = request.form.get(
        "image_url",
        ""
    ).strip()

    price = request.form.get(
        "price",
        "0"
    ).strip()

    stock = request.form.get(
        "stock",
        "0"
    ).strip()

    if not name:

        flash(
            "Product name is required.",
            "error"
        )

        return redirect(
            url_for("admin.add_product")
        )

    try:

        price = float(price)

        stock = int(stock)

    except ValueError:

        flash(
            "Please enter a valid price and stock quantity.",
            "error"
        )

        return redirect(
            url_for("admin.add_product")
        )

    if price < 0:

        flash(
            "Price cannot be negative.",
            "error"
        )

        return redirect(
            url_for("admin.add_product")
        )

    if stock < 0:

        flash(
            "Stock cannot be negative.",
            "error"
        )

        return redirect(
            url_for("admin.add_product")
        )

    product = Product(

        name=name,

        description=description,

        category=category,

        price=price,

        image_url=image_url,

        stock=stock
    )

    try:

        db.session.add(product)

        db.session.commit()

        flash(
            "Product added successfully.",
            "success"
        )

    except Exception as error:

        db.session.rollback()

        print(
            "ADD PRODUCT ERROR:",
            error
        )

        flash(
            "Unable to add product.",
            "error"
        )

    return redirect(
        url_for("admin.products")
    )


# =========================================================
# EDIT PRODUCT
# =========================================================

@admin_bp.route(
    "/products/edit/<int:product_id>",
    methods=["GET"]
)
@admin_required
def edit_product(product_id):

    product = db.session.get(
        Product,
        product_id
    )

    if not product:

        flash(
            "Product not found.",
            "error"
        )

        return redirect(
            url_for("admin.products")
        )

    return render_template(
        "edit_product.html",
        product=product
    )


# =========================================================
# EDIT PRODUCT DATA
# =========================================================

@admin_bp.route(
    "/products/edit/<int:product_id>/data",
    methods=["GET"]
)
@admin_required
def edit_product_data(product_id):

    product = db.session.get(
        Product,
        product_id
    )

    if not product:

        return jsonify({
            "success": False,
            "message": "Product not found."
        }), 404

    return jsonify({

        "success": True,

        "product": {

            "id": product.id,

            "name": getattr(
                product,
                "name",
                ""
            ),

            "brand": getattr(
                product,
                "brand",
                ""
            ),

            "description": getattr(
                product,
                "description",
                ""
            ),

            "price": float(
                getattr(
                    product,
                    "price",
                    0
                ) or 0
            ),

            "old_price": float(
                getattr(
                    product,
                    "old_price",
                    0
                ) or 0
            ),

            "discount": float(
                getattr(
                    product,
                    "discount",
                    0
                ) or 0
            ),

            "category": getattr(
                product,
                "category",
                ""
            ),

            "category_id": getattr(
                product,
                "category_id",
                None
            ),

            "image_url": getattr(
                product,
                "image_url",
                ""
            ),

            "stock": int(
                getattr(
                    product,
                    "stock",
                    0
                ) or 0
            )
        }
    })


# =========================================================
# UPDATE PRODUCT
# =========================================================

@admin_bp.route(
    "/products/edit/<int:product_id>/update",
    methods=["POST"]
)
@admin_required
def update_product(product_id):

    product = db.session.get(
        Product,
        product_id
    )

    if not product:

        return jsonify({
            "success": False,
            "message": "Product not found."
        }), 404

    data = request.get_json(
        silent=True
    )

    if not data:

        return jsonify({
            "success": False,
            "message": "No product data was received."
        }), 400

    name = str(
        data.get("name", "")
    ).strip()

    brand = str(
        data.get("brand", "")
    ).strip()

    description = str(
        data.get("description", "")
    ).strip()

    category = str(
        data.get("category", "")
    ).strip()

    image_url = str(
        data.get("image_url", "")
    ).strip()

    if not name:

        return jsonify({
            "success": False,
            "message": "Product name is required."
        }), 400

    if not brand:

        return jsonify({
            "success": False,
            "message": "Product brand is required."
        }), 400

    if not category:

        return jsonify({
            "success": False,
            "message": "Product category is required."
        }), 400

    try:

        price = float(
            data.get("price", 0)
        )

        stock = int(
            data.get("stock", 0)
        )

    except (
        TypeError,
        ValueError
    ):

        return jsonify({
            "success": False,
            "message": "Please enter a valid price and stock quantity."
        }), 400

    if price < 0:

        return jsonify({
            "success": False,
            "message": "Price cannot be negative."
        }), 400

    if stock < 0:

        return jsonify({
            "success": False,
            "message": "Stock cannot be negative."
        }), 400

    old_price = data.get(
        "old_price"
    )

    if old_price in (
        None,
        "",
        "null"
    ):

        old_price = None

    else:

        try:

            old_price = float(
                old_price
            )

        except (
            TypeError,
            ValueError
        ):

            return jsonify({
                "success": False,
                "message": "Please enter a valid old price."
            }), 400

        if old_price < 0:

            return jsonify({
                "success": False,
                "message": "Old price cannot be negative."
            }), 400

    discount = data.get(
        "discount"
    )

    if discount in (
        None,
        "",
        "null"
    ):

        discount = None

    else:

        try:

            discount = int(
                discount
            )

        except (
            TypeError,
            ValueError
        ):

            return jsonify({
                "success": False,
                "message": "Discount must be a whole number."
            }), 400

        if discount < 0 or discount > 100:

            return jsonify({
                "success": False,
                "message": "Discount must be between 0 and 100."
            }), 400

    try:

        product.name = name

        product.brand = brand

        product.description = description

        product.category = category

        product.price = price

        product.old_price = old_price

        product.discount = discount

        product.image_url = image_url

        product.stock = stock

        db.session.commit()

    except Exception as error:

        db.session.rollback()

        print(
            "UPDATE PRODUCT ERROR:",
            error
        )

        return jsonify({
            "success": False,
            "message": "Unable to update product."
        }), 500

    return jsonify({

        "success": True,

        "message": "Product updated successfully."

    })


# =========================================================
# ADMIN ORDERS PAGE
# =========================================================

@admin_bp.route("/orders")
@admin_required
def orders():

    return render_template(
        "admin_orders.html"
    )


# =========================================================
# ADMIN ORDERS DATA
# =========================================================

@admin_bp.route("/orders/data")
@admin_required
def orders_data():

    orders = (
        Order.query
        .order_by(Order.created_at.desc())
        .all()
    )

    order_list = []

    for order in orders:

        user = db.session.get(
            User,
            order.user_id
        )

        customer_name = (
            user.name
            if user
            else "Guest"
        )

        customer_email = (
            user.email
            if user
            else ""
        )

        customer_phone = (
            order.phone
            if order.phone
            else (
                getattr(user, "phone", "")
                if user
                else ""
            )
        )

        customer_state = (
            getattr(user, "state", "")
            if user
            else ""
        )

        customer_address = (
            order.delivery_address
            if order.delivery_address
            else (
                getattr(user, "address", "")
                if user
                else ""
            )
        )

        order_items = []

        for item in order.items:

            product = item.product

            order_items.append({

                "id": item.id,

                "product_id": item.product_id,

                "product_name": (
                    product.name
                    if product
                    else "Product"
                ),

                "quantity": int(
                    item.quantity or 0
                ),

                "price": float(
                    item.price or 0
                )

            })

        order_list.append({

            "id": order.id,

            "order_number":
                f"NC-{order.id:06d}",

            "user_id":
                order.user_id,

            "customer_name":
                customer_name,

            "customer_email":
                customer_email,

            "phone":
                customer_phone,

            "state":
                customer_state,

            "delivery_address":
                customer_address,

            "total":
                float(order.total or 0),

            "status":
                order.status or "Pending",

            "payment_ref":
                order.payment_ref or "",

            "created_at":
                (
                    order.created_at.isoformat()
                    if order.created_at
                    else ""
                ),

            "items":
                order_items

        })

    return jsonify({

        "success": True,

        "orders":
            order_list

    })


# =========================================================
# SINGLE ORDER DATA
# =========================================================

@admin_bp.route(
    "/orders/<int:order_id>/data"
)
@admin_required
def single_order_data(order_id):

    order = db.session.get(
        Order,
        order_id
    )

    if not order:

        return jsonify({

            "success": False,

            "message":
                "Order not found."

        }), 404

    user = db.session.get(
        User,
        order.user_id
    )

    customer_phone = (
        order.phone
        if order.phone
        else (
            getattr(user, "phone", "")
            if user
            else ""
        )
    )

    customer_state = (
        getattr(user, "state", "")
        if user
        else ""
    )

    customer_address = (
        order.delivery_address
        if order.delivery_address
        else (
            getattr(user, "address", "")
            if user
            else ""
        )
    )

    order_items = []

    for item in order.items:

        product = item.product

        order_items.append({

            "id":
                item.id,

            "product_id":
                item.product_id,

            "product_name":
                (
                    product.name
                    if product
                    else "Product"
                ),

            "quantity":
                int(item.quantity or 0),

            "price":
                float(item.price or 0)

        })

    return jsonify({

        "success": True,

        "order": {

            "id":
                order.id,

            "order_number":
                f"NC-{order.id:06d}",

            "customer_name":
                (
                    user.name
                    if user
                    else "Guest"
                ),

            "customer_email":
                (
                    user.email
                    if user
                    else ""
                ),

            "phone":
                customer_phone,

            "state":
                customer_state,

            "delivery_address":
                customer_address,

            "total":
                float(order.total or 0),

            "status":
                order.status or "Pending",

            "payment_ref":
                order.payment_ref or "",

            "created_at":
                (
                    order.created_at.isoformat()
                    if order.created_at
                    else ""
                ),

            "items":
                order_items

        }

    })


# =========================================================
# UPDATE ORDER STATUS
# =========================================================

@admin_bp.route(
    "/orders/<int:order_id>/status",
    methods=["POST"]
)
@admin_required
def update_order_status(order_id):

    order = db.session.get(
        Order,
        order_id
    )

    if not order:

        return jsonify({

            "success": False,

            "message":
                "Order not found."

        }), 404

    data = request.get_json(
        silent=True
    )

    if not data:

        return jsonify({

            "success": False,

            "message":
                "No status was received."

        }), 400

    requested_status = str(
        data.get(
            "status",
            ""
        )
    ).strip().lower()

    allowed_statuses = {

        "pending":
            "Pending",

        "paid":
            "Paid",

        "processing":
            "Processing",

        "shipped":
            "Shipped",

        "delivered":
            "Delivered",

        "cancelled":
            "Cancelled"
    }

    if requested_status not in allowed_statuses:

        return jsonify({

            "success": False,

            "message":
                "Invalid order status."

        }), 400

    new_status = allowed_statuses[
        requested_status
    ]

    current_status = str(
        order.status or "Pending"
    ).strip().lower()

    # -----------------------------------------------------
    # ALREADY CANCELLED
    # -----------------------------------------------------

    if current_status == "cancelled":

        return jsonify({

            "success": False,

            "message":
                "Cancelled orders cannot be changed."

        }), 400

    # -----------------------------------------------------
    # ALREADY DELIVERED
    # -----------------------------------------------------

    if current_status == "delivered":

        return jsonify({

            "success": False,

            "message":
                "Delivered orders cannot be changed."

        }), 400

    # -----------------------------------------------------
    # PREVENT MOVING BACKWARD
    # -----------------------------------------------------

    status_order = {

        "pending": 1,

        "paid": 2,

        "processing": 3,

        "shipped": 4,

        "delivered": 5
    }

    if (
        requested_status != "cancelled"
        and current_status in status_order
        and requested_status in status_order
        and status_order[requested_status]
        < status_order[current_status]
    ):

        return jsonify({

            "success": False,

            "message":
                "Order status cannot move backwards."

        }), 400

    # -----------------------------------------------------
    # CANCELLATION
    # -----------------------------------------------------

    if requested_status == "cancelled":

        if current_status in (
            "shipped",
            "delivered"
        ):

            return jsonify({

                "success": False,

                "message":
                    "This order can no longer be cancelled."

            }), 400

        try:

            # Restore stock only if it has already
            # been deducted.

            if current_status in (
                "paid",
                "processing"
            ):

                for item in order.items:

                    product = item.product

                    if product:

                        product.stock = (
                            int(product.stock or 0)
                            + int(item.quantity or 0)
                        )

            order.status = "Cancelled"

            db.session.commit()

        except Exception as error:

            db.session.rollback()

            print(
                "ADMIN CANCEL ORDER ERROR:",
                error
            )

            return jsonify({

                "success": False,

                "message":
                    "Unable to cancel order."

            }), 500

        return jsonify({

            "success": True,

            "message":
                "Order cancelled successfully.",

            "status":
                "Cancelled"

        })

    # -----------------------------------------------------
    # NORMAL STATUS UPDATE
    # -----------------------------------------------------

    try:

        order.status = new_status

        db.session.commit()

    except Exception as error:

        db.session.rollback()

        print(
            "UPDATE ORDER STATUS ERROR:",
            error
        )

        return jsonify({

            "success": False,

            "message":
                "Unable to update order status."

        }), 500

    return jsonify({

        "success": True,

        "message":
            f"Order status changed to {new_status}.",

        "status":
            new_status

    })


# =========================================================
# ADMIN CANCEL ORDER
# =========================================================

@admin_bp.route(
    "/orders/<int:order_id>/cancel",
    methods=["POST"]
)
@admin_required
def cancel_order(order_id):

    order = db.session.get(
        Order,
        order_id
    )

    if not order:

        return jsonify({

            "success": False,

            "message":
                "Order not found."

        }), 404

    current_status = (
        order.status or ""
    ).strip().lower()

    if current_status == "cancelled":

        return jsonify({

            "success": False,

            "message":
                "Order is already cancelled."

        }), 400

    if current_status in (
        "shipped",
        "delivered"
    ):

        return jsonify({

            "success": False,

            "message":
                "This order can no longer be cancelled."

        }), 400

    try:

        # -------------------------------------------------
        # RESTORE STOCK
        # -------------------------------------------------

        if current_status in (
            "paid",
            "processing"
        ):

            for item in order.items:

                product = item.product

                if product:

                    product.stock = (
                        int(product.stock or 0)
                        + int(item.quantity or 0)
                    )

        # -------------------------------------------------
        # CANCEL ORDER
        # -------------------------------------------------

        order.status = "Cancelled"

        db.session.commit()

    except Exception as error:

        db.session.rollback()

        print(
            "CANCEL ORDER ERROR:",
            error
        )

        return jsonify({

            "success": False,

            "message":
                "Unable to cancel order."

        }), 500

    return jsonify({

        "success": True,

        "message":
            "Order cancelled successfully.",

        "status":
            "Cancelled"

    })


# =========================================================
# USERS PAGE
# =========================================================

@admin_bp.route("/users")
@admin_required
def users():

    return render_template(
        "users.html"
    )


# =========================================================
# USERS DATA
# =========================================================

@admin_bp.route("/users/data")
@admin_required
def users_data():

    users = User.query.order_by(
        User.id.desc()
    ).all()

    user_list = []

    for user in users:

        user_list.append({

            "id":
                user.id,

            "first_name":
                getattr(
                    user,
                    "first_name",
                    ""
                ),

            "last_name":
                getattr(
                    user,
                    "last_name",
                    ""
                ),

            "name":
                getattr(
                    user,
                    "name",
                    ""
                ),

            "email":
                getattr(
                    user,
                    "email",
                    ""
                ),

            "phone":
                getattr(
                    user,
                    "phone",
                    ""
                ),

            "state":
                getattr(
                    user,
                    "state",
                    ""
                ),

            "address":
                getattr(
                    user,
                    "address",
                    ""
                ),

            "is_admin":
                bool(
                    user.is_admin
                ),

            "email_verified":
                bool(
                    getattr(
                        user,
                        "email_verified",
                        False
                    )
                ),

            "created_at":

                (
                    user.created_at.isoformat()
                    if user.created_at
                    else ""
                )

        })

    total_users = len(
        user_list
    )

    total_admins = sum(
        1
        for user in user_list
        if user["is_admin"]
    )

    total_customers = (
        total_users
        - total_admins
    )

    return jsonify({

        "success":
            True,

        "users":
            user_list,

        "statistics": {

            "total_users":
                total_users,

            "total_customers":
                total_customers,

            "total_admins":
                total_admins

        }

    })


# =========================================================
# PRODUCT CSS
# =========================================================

@admin_bp.route("/products.css")
@admin_required
def products_css():

    return redirect(
        "/naijacart-frontend/css/products.css"
    )


# =========================================================
# PRODUCT JAVASCRIPT
# =========================================================

@admin_bp.route("/products.js")
@admin_required
def products_js():

    return redirect(
        "/naijacart-frontend/js/products.js"
    )