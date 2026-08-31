from flask import (
    Blueprint,
    request,
    jsonify,
    session,
    render_template,
    redirect,
    url_for,
    flash
)

from models import (
    db,
    User,
    Product,
    Order,
    OrderItem
)

import os
import requests
import secrets
import hmac
import hashlib


# =========================================================
# ORDER BLUEPRINT
# =========================================================

orders_bp = Blueprint(
    "orders",
    __name__,
    url_prefix="/orders"
)


# =========================================================
# PAYSTACK
# =========================================================

PAYSTACK_SECRET_KEY = os.getenv(
    "PAYSTACK_SECRET_KEY",
    ""
).strip()

PAYSTACK_INITIALIZE_URL = (
    "https://api.paystack.co/transaction/initialize"
)

PAYSTACK_VERIFY_URL = (
    "https://api.paystack.co/transaction/verify/"
)


# =========================================================
# ORDER STATUSES
# =========================================================

ORDER_STATUSES = [
    "Pending",
    "Paid",
    "Processing",
    "Shipped",
    "Delivered",
    "Cancelled"
]


# =========================================================
# ADMIN STATUS FLOW
#
# Pending
#    ↓
# Paid
#    ↓
# Processing
#    ↓
# Shipped
#    ↓
# Delivered
#
# Cancellation is allowed before Shipped.
# =========================================================

STATUS_FLOW = {

    "Pending": [
        "Pending",
        "Paid",
        "Processing",
        "Cancelled"
    ],

    "Paid": [
        "Paid",
        "Processing",
        "Cancelled"
    ],

    "Processing": [
        "Processing",
        "Shipped",
        "Cancelled"
    ],

    "Shipped": [
        "Shipped",
        "Delivered"
    ],

    "Delivered": [
        "Delivered"
    ],

    "Cancelled": [
        "Cancelled"
    ]
}


# =========================================================
# CUSTOMER CANCELLABLE STATUSES
# =========================================================

CUSTOMER_CANCELLABLE_STATUSES = [
    "Pending",
    "Paid",
    "Processing"
]


# =========================================================
# ADMIN CANCELLABLE STATUSES
# =========================================================

ADMIN_CANCELLABLE_STATUSES = [
    "Pending",
    "Paid",
    "Processing"
]


# =========================================================
# HELPER — NORMALIZE STATUS
# =========================================================

def normalize_status(status):

    if not status:

        return "Pending"

    status = str(
        status
    ).strip().lower()

    status_map = {

        "pending": "Pending",

        "paid": "Paid",

        "processing": "Processing",

        "shipped": "Shipped",

        "delivered": "Delivered",

        "cancelled": "Cancelled",

        "canceled": "Cancelled",

        "completed": "Delivered"
    }

    return status_map.get(
        status,
        "Pending"
    )


# =========================================================
# HELPER — PAYSTACK HEADERS
# =========================================================

def paystack_headers():

    return {

        "Authorization":
            f"Bearer {PAYSTACK_SECRET_KEY}",

        "Content-Type":
            "application/json"
    }


# =========================================================
# HELPER — VERIFY PAYSTACK TRANSACTION
# =========================================================

def verify_paystack_transaction(reference):

    if not PAYSTACK_SECRET_KEY:

        return None, (
            "Paystack is not configured."
        )

    try:

        response = requests.get(

            PAYSTACK_VERIFY_URL + reference,

            headers=paystack_headers(),

            timeout=30
        )

        try:

            data = response.json()

        except ValueError:

            print(
                "PAYSTACK VERIFY INVALID RESPONSE:",
                response.text
            )

            return None, (
                "Paystack returned an invalid response."
            )

        if not response.ok:

            print(
                "PAYSTACK VERIFY HTTP ERROR:",
                data
            )

            return None, (
                "Unable to verify payment."
            )

        if not data.get("status"):

            print(
                "PAYSTACK VERIFY ERROR:",
                data
            )

            return None, data.get(
                "message",
                "Payment verification failed."
            )

        return data.get(
            "data",
            {}
        ), None

    except requests.RequestException as error:

        print(
            "PAYSTACK VERIFY CONNECTION ERROR:",
            error
        )

        return None, (
            "Unable to connect to Paystack."
        )


# =========================================================
# HELPER — COMPLETE PAID ORDER
# =========================================================

def complete_paid_order(
    order,
    payment_data
):

    # -----------------------------------------------------
    # CHECK PAYMENT STATUS
    # -----------------------------------------------------

    if payment_data.get("status") != "success":

        return False, (
            "Payment was not successful."
        )

    # -----------------------------------------------------
    # CHECK AMOUNT
    # -----------------------------------------------------

    expected_amount = int(
        round(
            float(order.total) * 100
        )
    )

    paid_amount = int(
        payment_data.get(
            "amount",
            0
        )
    )

    if paid_amount != expected_amount:

        print(
            "PAYMENT AMOUNT MISMATCH:",
            expected_amount,
            paid_amount
        )

        return False, (
            "Payment amount could not be verified."
        )

    # -----------------------------------------------------
    # NORMALIZE CURRENT STATUS
    # -----------------------------------------------------

    current_status = normalize_status(
        order.status
    )

    # -----------------------------------------------------
    # ALREADY PAID / PROCESSED
    # -----------------------------------------------------

    if current_status in [
        "Paid",
        "Processing",
        "Shipped",
        "Delivered"
    ]:

        return True, (
            "Order was already paid."
        )

    # -----------------------------------------------------
    # CANCELLED ORDER
    # -----------------------------------------------------

    if current_status == "Cancelled":

        return False, (
            "This order has already been cancelled."
        )

    # -----------------------------------------------------
    # CHECK STOCK
    # -----------------------------------------------------

    for item in order.items:

        product = item.product

        if not product:

            return False, (
                "A product in this order no longer exists."
            )

        if (
            int(product.stock or 0)
            < int(item.quantity or 0)
        ):

            return False, (
                f"Insufficient stock for "
                f"{product.name}."
            )

    # -----------------------------------------------------
    # MARK ORDER AS PAID
    # -----------------------------------------------------

    try:

        order.status = "Paid"

        # Deduct stock only once payment is confirmed.
        for item in order.items:

            if item.product:

                item.product.stock -= (
                    int(item.quantity or 0)
                )

        db.session.commit()

        return True, (
            "Payment confirmed."
        )

    except Exception as error:

        db.session.rollback()

        print(
            "COMPLETE PAID ORDER ERROR:",
            error
        )

        return False, (
            "Unable to complete the order."
        )


# =========================================================
# HELPER — DETERMINE IF STOCK WAS DEDUCTED
# =========================================================

def stock_was_deducted(order):

    """
    Determines whether stock has already been deducted.

    PAY ON DELIVERY:
        payment_ref is normally None.
        Stock is deducted when the order is created.

    ONLINE PAYMENT:
        payment_ref exists.
        Stock is deducted only after Paystack payment
        is successfully verified.

    Therefore:

        Pending + payment_ref exists
            = Online payment not yet completed
            = DO NOT restore stock

        Pending + no payment_ref
            = Pay on delivery
            = Stock WAS deducted
            = Restore stock

        Paid / Processing / Shipped / Delivered
            = Normally stock was deducted.
    """

    status = normalize_status(
        order.status
    )

    # Online order waiting for payment.
    if (
        status == "Pending"
        and order.payment_ref
    ):

        return False

    # Pay on delivery pending order.
    if (
        status == "Pending"
        and not order.payment_ref
    ):

        return True

    if status in [
        "Paid",
        "Processing",
        "Shipped",
        "Delivered"
    ]:

        return True

    return False


# =========================================================
# HELPER — RESTORE STOCK
# =========================================================

def restore_order_stock(order):

    """
    Restore product stock only if stock had already
    been deducted from this order.
    """

    if not stock_was_deducted(order):

        return

    for item in order.items:

        product = item.product

        if product:

            product.stock = (
                int(product.stock or 0)
                + int(item.quantity or 0)
            )


# =========================================================
# HELPER — CHECK LOGIN
# =========================================================

def get_logged_in_user():

    user_id = session.get(
        "user_id"
    )

    if not user_id:

        return None

    return db.session.get(
        User,
        user_id
    )


# =========================================================
# MY ORDERS
# =========================================================

@orders_bp.route("/")
def my_orders():

    user = get_logged_in_user()

    if not user:

        return redirect(
            url_for("login")
        )

    orders = (
        Order.query
        .filter_by(
            user_id=user.id
        )
        .order_by(
            Order.created_at.desc()
        )
        .all()
    )

    # Normalize statuses before sending them to template.
    for order in orders:

        order.status = normalize_status(
            order.status
        )

    return render_template(
        "orders.html",
        user=user,
        orders=orders,
        order_statuses=ORDER_STATUSES
    )


# =========================================================
# ORDER DETAILS
# =========================================================

@orders_bp.route(
    "/<int:order_id>"
)
def order_details(order_id):

    user = get_logged_in_user()

    if not user:

        return redirect(
            url_for("login")
        )

    order = (
        Order.query
        .filter_by(
            id=order_id,
            user_id=user.id
        )
        .first()
    )

    if not order:

        flash(
            "Order not found.",
            "error"
        )

        return redirect(
            url_for(
                "orders.my_orders"
            )
        )

    order.status = normalize_status(
        order.status
    )

    return render_template(
        "order_details.html",
        order=order
    )


# =========================================================
# CUSTOMER — CANCEL ORDER
# =========================================================

@orders_bp.route(
    "/<int:order_id>/cancel",
    methods=["POST"]
)
def cancel_order(order_id):

    user = get_logged_in_user()

    if not user:

        return jsonify({

            "success": False,

            "message":
                "Please sign in before cancelling an order."

        }), 401

    # -----------------------------------------------------
    # FIND CUSTOMER ORDER
    # -----------------------------------------------------

    order = (
        Order.query
        .filter_by(
            id=order_id,
            user_id=user.id
        )
        .first()
    )

    if not order:

        return jsonify({

            "success": False,

            "message":
                "Order not found."

        }), 404

    # -----------------------------------------------------
    # CURRENT STATUS
    # -----------------------------------------------------

    current_status = normalize_status(
        order.status
    )

    # -----------------------------------------------------
    # ALREADY CANCELLED
    # -----------------------------------------------------

    if current_status == "Cancelled":

        return jsonify({

            "success": False,

            "message":
                "This order is already cancelled."

        }), 400

    # -----------------------------------------------------
    # CHECK IF CUSTOMER CAN CANCEL
    # -----------------------------------------------------

    if (
        current_status
        not in CUSTOMER_CANCELLABLE_STATUSES
    ):

        return jsonify({

            "success": False,

            "message": (
                f"This order is currently "
                f"'{current_status}' and can "
                "no longer be cancelled."
            )

        }), 400

    # -----------------------------------------------------
    # CANCEL ORDER
    # -----------------------------------------------------

    try:

        # Restore stock only when it was actually deducted.
        restore_order_stock(
            order
        )

        order.status = "Cancelled"

        db.session.commit()

        return jsonify({

            "success": True,

            "message":
                "Your order has been cancelled successfully.",

            "order_id":
                order.id,

            "order_number":
                f"NC-{order.id:06d}",

            "status":
                "Cancelled"

        }), 200

    except Exception as error:

        db.session.rollback()

        print(
            "CUSTOMER CANCEL ORDER ERROR:",
            error
        )

        return jsonify({

            "success": False,

            "message":
                "Unable to cancel the order. "
                "Please try again."

        }), 500


# =========================================================
# ADMIN CHECK
# =========================================================

def admin_required():

    user = get_logged_in_user()

    if not user:

        return None, jsonify({

            "success": False,

            "message":
                "Please sign in."

        }), 401

    if not user.is_admin:

        return None, jsonify({

            "success": False,

            "message":
                "Administrator access required."

        }), 403

    return user, None, None


# =========================================================
# ADMIN — UPDATE ORDER STATUS
# =========================================================

@orders_bp.route(
    "/admin/<int:order_id>/status",
    methods=["POST"]
)
def admin_update_order_status(
    order_id
):

    admin, error_response, error_code = (
        admin_required()
    )

    if error_response:

        return (
            error_response,
            error_code
        )

    # -----------------------------------------------------
    # FIND ORDER
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # GET REQUEST DATA
    # -----------------------------------------------------

    data = request.get_json(
        silent=True
    ) or {}

    new_status = normalize_status(
        data.get(
            "status",
            ""
        )
    )

    # -----------------------------------------------------
    # VALIDATE STATUS
    # -----------------------------------------------------

    if new_status not in ORDER_STATUSES:

        return jsonify({

            "success": False,

            "message":
                "Invalid order status."

        }), 400

    # -----------------------------------------------------
    # CURRENT STATUS
    # -----------------------------------------------------

    current_status = normalize_status(
        order.status
    )

    # -----------------------------------------------------
    # CHECK STATUS FLOW
    # -----------------------------------------------------

    allowed_next_statuses = STATUS_FLOW.get(
        current_status,
        []
    )

    if new_status not in allowed_next_statuses:

        return jsonify({

            "success": False,

            "message": (
                f"Cannot change order from "
                f"{current_status} to "
                f"{new_status}."
            )

        }), 400

    # -----------------------------------------------------
    # NO CHANGE
    # -----------------------------------------------------

    if new_status == current_status:

        return jsonify({

            "success": True,

            "message":
                "Order status is already "
                f"{current_status}.",

            "order_id":
                order.id,

            "status":
                current_status

        }), 200

    # -----------------------------------------------------
    # ADMIN CANCELLATION
    # -----------------------------------------------------

    if new_status == "Cancelled":

        if (
            current_status
            not in ADMIN_CANCELLABLE_STATUSES
        ):

            return jsonify({

                "success": False,

                "message": (
                    f"Orders with status "
                    f"'{current_status}' "
                    "cannot be cancelled."
                )

            }), 400

        try:

            # Restore stock only if stock was deducted.
            restore_order_stock(
                order
            )

            order.status = "Cancelled"

            db.session.commit()

            return jsonify({

                "success": True,

                "message":
                    "Order cancelled successfully.",

                "order_id":
                    order.id,

                "order_number":
                    f"NC-{order.id:06d}",

                "status":
                    "Cancelled"

            }), 200

        except Exception as error:

            db.session.rollback()

            print(
                "ADMIN CANCEL ORDER ERROR:",
                error
            )

            return jsonify({

                "success": False,

                "message":
                    "Unable to cancel this order."

            }), 500

    # -----------------------------------------------------
    # NORMAL STATUS UPDATE
    # -----------------------------------------------------

    try:

        order.status = new_status

        db.session.commit()

        return jsonify({

            "success": True,

            "message": (
                f"Order status changed from "
                f"{current_status} to "
                f"{new_status}."
            ),

            "order_id":
                order.id,

            "order_number":
                f"NC-{order.id:06d}",

            "status":
                new_status

        }), 200

    except Exception as error:

        db.session.rollback()

        print(
            "ADMIN UPDATE ORDER STATUS ERROR:",
            error
        )

        return jsonify({

            "success": False,

            "message":
                "Unable to update order status."

        }), 500


# =========================================================
# CREATE ORDER
# =========================================================

@orders_bp.route(
    "/create",
    methods=["POST"]
)
def create_order():

    # =====================================================
    # CHECK LOGIN
    # =====================================================

    user_id = session.get(
        "user_id"
    )

    if not user_id:

        return jsonify({

            "success": False,

            "message":
                "Please sign in before placing an order."

        }), 401

    # =====================================================
    # GET USER
    # =====================================================

    user = db.session.get(
        User,
        user_id
    )

    if not user:

        session.clear()

        return jsonify({

            "success": False,

            "message":
                "Your session has expired. "
                "Please sign in again."

        }), 401

    # =====================================================
    # REQUEST DATA
    # =====================================================

    data = request.get_json(
        silent=True
    )

    if not data:

        return jsonify({

            "success": False,

            "message":
                "No order data was received."

        }), 400

    customer = data.get(
        "customer",
        {}
    )

    cart_items = data.get(
        "items",
        []
    )

    payment_method = data.get(
        "payment_method",
        "delivery"
    )

    # =====================================================
    # CHECK CART
    # =====================================================

    if (
        not isinstance(
            cart_items,
            list
        )
        or not cart_items
    ):

        return jsonify({

            "success": False,

            "message":
                "Your cart is empty."

        }), 400

    # =====================================================
    # CUSTOMER INFORMATION
    # =====================================================

    first_name = str(
        customer.get(
            "firstName",
            ""
        )
    ).strip()

    last_name = str(
        customer.get(
            "lastName",
            ""
        )
    ).strip()

    phone = str(
        customer.get(
            "phone",
            ""
        )
    ).strip()

    email = str(
        customer.get(
            "email",
            ""
        )
    ).strip().lower()

    address = str(
        customer.get(
            "address",
            ""
        )
    ).strip()

    state = str(
        customer.get(
            "state",
            ""
        )
    ).strip()

    city = str(
        customer.get(
            "city",
            ""
        )
    ).strip()

    # =====================================================
    # VALIDATION
    # =====================================================

    if not first_name:

        return jsonify({

            "success": False,

            "message":
                "First name is required."

        }), 400

    if not last_name:

        return jsonify({

            "success": False,

            "message":
                "Last name is required."

        }), 400

    if not phone:

        return jsonify({

            "success": False,

            "message":
                "Phone number is required."

        }), 400

    if not email:

        return jsonify({

            "success": False,

            "message":
                "Email address is required."

        }), 400

    if not address:

        return jsonify({

            "success": False,

            "message":
                "Delivery address is required."

        }), 400

    if not state:

        return jsonify({

            "success": False,

            "message":
                "Please select your state."

        }), 400

    if not city:

        return jsonify({

            "success": False,

            "message":
                "City is required."

        }), 400

    # =====================================================
    # PAYMENT METHOD
    # =====================================================

    allowed_payment_methods = [
        "card",
        "bank",
        "delivery"
    ]

    if payment_method not in allowed_payment_methods:

        return jsonify({

            "success": False,

            "message":
                "Invalid payment method."

        }), 400

    # =====================================================
    # DELIVERY ADDRESS
    # =====================================================

    delivery_address = (
        f"{address}, {city}, {state}, Nigeria"
    )

    # =====================================================
    # CALCULATE ORDER
    # =====================================================

    subtotal = 0

    order_products = []

    for item in cart_items:

        if not isinstance(
            item,
            dict
        ):

            return jsonify({

                "success": False,

                "message":
                    "Invalid cart item."

            }), 400

        product_name = str(
            item.get(
                "product_name",
                ""
            )
        ).strip()

        quantity = item.get(
            "quantity",
            1
        )

        if not product_name:

            return jsonify({

                "success": False,

                "message":
                    "A product name is missing "
                    "from your cart."

            }), 400

        try:

            quantity = int(
                quantity
            )

        except (
            TypeError,
            ValueError
        ):

            return jsonify({

                "success": False,

                "message":
                    "Invalid product quantity."

            }), 400

        if quantity <= 0:

            return jsonify({

                "success": False,

                "message":
                    "Invalid product quantity."

            }), 400

        # -------------------------------------------------
        # FIND PRODUCT
        # -------------------------------------------------

        product = (
            Product.query
            .filter(
                db.func.lower(
                    Product.name
                )
                ==
                product_name.lower()
            )
            .first()
        )

        if not product:

            return jsonify({

                "success": False,

                "message": (
                    f"{product_name} "
                    "could not be found."
                )

            }), 404

        # -------------------------------------------------
        # CHECK STOCK
        # -------------------------------------------------

        if (
            int(product.stock or 0)
            < quantity
        ):

            return jsonify({

                "success": False,

                "message": (
                    f"Only {product.stock} "
                    f"of {product.name} "
                    "is available."
                )

            }), 400

        # -------------------------------------------------
        # DATABASE PRICE
        # -------------------------------------------------

        price = float(
            product.price
        )

        item_total = (
            price * quantity
        )

        subtotal += item_total

        order_products.append({

            "product":
                product,

            "quantity":
                quantity,

            "price":
                price

        })

    # =====================================================
    # DELIVERY
    # =====================================================

    if subtotal >= 50000:

        delivery_fee = 0

    else:

        delivery_fee = 2500

    # =====================================================
    # TOTAL
    # =====================================================

    total = (
        subtotal
        + delivery_fee
    )

    # =====================================================
    # CREATE ORDER
    # =====================================================

    order = Order(

        user_id=user.id,

        total=total,

        status="Pending",

        payment_ref=None,

        delivery_address=
            delivery_address,

        phone=phone
    )

    try:

        db.session.add(
            order
        )

        db.session.flush()

        # =================================================
        # CREATE ORDER ITEMS
        # =================================================

        for item in order_products:

            order_item = OrderItem(

                order_id=
                    order.id,

                product_id=
                    item["product"].id,

                quantity=
                    item["quantity"],

                price=
                    item["price"]
            )

            db.session.add(
                order_item
            )

        # =================================================
        # PAY ON DELIVERY
        # =================================================

        if payment_method == "delivery":

            # Stock is deducted immediately because
            # the order has been successfully placed.
            for item in order_products:

                item["product"].stock -= (
                    item["quantity"]
                )

            order.status = "Pending"

            db.session.commit()

            return jsonify({

                "success": True,

                "payment_required":
                    False,

                "message":
                    "Order placed successfully.",

                "order_id":
                    order.id,

                "order_number":
                    f"NC-{order.id:06d}",

                "total":
                    total,

                "payment_method":
                    "delivery",

                "status":
                    "Pending"

            }), 201

        # =================================================
        # ONLINE PAYMENT
        # =================================================

        if not PAYSTACK_SECRET_KEY:

            db.session.rollback()

            return jsonify({

                "success": False,

                "message":
                    "Paystack is not configured "
                    "on the server."

            }), 500

        # =================================================
        # PAYSTACK AMOUNT
        # =================================================

        amount_kobo = int(
            round(
                total * 100
            )
        )

        # =================================================
        # CALLBACK URL
        # =================================================

        callback_url = url_for(

            "orders.payment_callback",

            _external=True
        )

        # =================================================
        # PAYMENT REFERENCE
        # =================================================

        reference = (

            f"NC-{order.id}-"
            f"{secrets.token_hex(8)}"

        )

        # =================================================
        # PAYSTACK PAYLOAD
        # =================================================

        payload = {

            "email":
                email,

            "amount":
                amount_kobo,

            "reference":
                reference,

            "callback_url":
                callback_url,

            "metadata": {

                "order_id":
                    order.id,

                "order_number":
                    f"NC-{order.id:06d}",

                "customer_name":
                    f"{first_name} {last_name}",

                "phone":
                    phone,

                "payment_method":
                    payment_method

            }
        }

        # =================================================
        # INITIALIZE PAYSTACK
        # =================================================

        paystack_response = requests.post(

            PAYSTACK_INITIALIZE_URL,

            json=payload,

            headers=paystack_headers(),

            timeout=30
        )

        try:

            paystack_data = (
                paystack_response.json()
            )

        except ValueError:

            db.session.rollback()

            print(
                "PAYSTACK INVALID RESPONSE:",
                paystack_response.text
            )

            return jsonify({

                "success": False,

                "message":
                    "Paystack returned an invalid response."

            }), 502

        # =================================================
        # PAYSTACK ERROR
        # =================================================

        if not paystack_response.ok:

            db.session.rollback()

            print(
                "PAYSTACK INITIALIZE ERROR:",
                paystack_data
            )

            return jsonify({

                "success": False,

                "message":
                    "Unable to initialize payment."

            }), 502

        if not paystack_data.get(
            "status"
        ):

            db.session.rollback()

            print(
                "PAYSTACK ERROR:",
                paystack_data
            )

            return jsonify({

                "success": False,

                "message":
                    paystack_data.get(
                        "message",
                        "Unable to initialize payment."
                    )

            }), 502

        # =================================================
        # PAYMENT DATA
        # =================================================

        payment_data = paystack_data.get(
            "data",
            {}
        )

        authorization_url = (
            payment_data.get(
                "authorization_url"
            )
        )

        returned_reference = (
            payment_data.get(
                "reference"
            )
        )

        if not authorization_url:

            db.session.rollback()

            return jsonify({

                "success": False,

                "message":
                    "Paystack did not return "
                    "a payment link."

            }), 502

        if not returned_reference:

            db.session.rollback()

            return jsonify({

                "success": False,

                "message":
                    "Paystack did not return "
                    "a payment reference."

            }), 502

        # =================================================
        # SAVE PAYMENT REFERENCE
        # =================================================

        order.payment_ref = (
            returned_reference
        )

        order.status = "Pending"

        db.session.commit()

        # =================================================
        # RETURN PAYSTACK URL
        # =================================================

        return jsonify({

            "success": True,

            "payment_required":
                True,

            "message":
                "Continue to Paystack to "
                "complete your payment.",

            "order_id":
                order.id,

            "order_number":
                f"NC-{order.id:06d}",

            "total":
                total,

            "payment_method":
                payment_method,

            "authorization_url":
                authorization_url,

            "reference":
                returned_reference,

            "status":
                "Pending"

        }), 201

    except requests.RequestException as error:

        db.session.rollback()

        print(
            "PAYSTACK CONNECTION ERROR:",
            error
        )

        return jsonify({

            "success": False,

            "message":
                "Unable to connect to Paystack. "
                "Please try again."

        }), 502

    except Exception as error:

        db.session.rollback()

        print(
            "ORDER CREATION ERROR:",
            error
        )

        return jsonify({

            "success": False,

            "message":
                "Unable to create your order."

        }), 500


# =========================================================
# PAYSTACK WEBHOOK
# =========================================================

@orders_bp.route(
    "/payment/webhook",
    methods=["POST"]
)
def payment_webhook():

    request_body = request.get_data()

    signature = request.headers.get(
        "x-paystack-signature",
        ""
    )

    if not signature:

        return jsonify({

            "success": False,

            "message":
                "Missing Paystack signature."

        }), 401

    if not PAYSTACK_SECRET_KEY:

        return jsonify({

            "success": False,

            "message":
                "Paystack is not configured."

        }), 500

    expected_signature = hmac.new(

        PAYSTACK_SECRET_KEY.encode(
            "utf-8"
        ),

        request_body,

        hashlib.sha512

    ).hexdigest()

    if not hmac.compare_digest(
        signature,
        expected_signature
    ):

        print(
            "INVALID PAYSTACK WEBHOOK SIGNATURE"
        )

        return jsonify({

            "success": False,

            "message":
                "Invalid signature."

        }), 401

    try:

        payload = request.get_json(
            silent=True
        )

    except Exception:

        payload = None

    if not payload:

        return jsonify({

            "success": False,

            "message":
                "Invalid webhook payload."

        }), 400

    event = payload.get(
        "event"
    )

    payment_data = payload.get(
        "data",
        {}
    )

    # Ignore events we don't need.
    if event != "charge.success":

        return jsonify({

            "success": True,

            "message":
                "Event received."

        }), 200

    reference = payment_data.get(
        "reference"
    )

    if not reference:

        return jsonify({

            "success": False,

            "message":
                "Payment reference missing."

        }), 400

    # =====================================================
    # VERIFY PAYMENT AGAIN
    # =====================================================

    verified_payment, error = (
        verify_paystack_transaction(
            reference
        )
    )

    if error:

        print(
            "WEBHOOK PAYMENT VERIFICATION ERROR:",
            error
        )

        return jsonify({

            "success": False,

            "message":
                error

        }), 502

    if not verified_payment:

        return jsonify({

            "success": False,

            "message":
                "Payment could not be verified."

        }), 400

    # =====================================================
    # FIND ORDER
    # =====================================================

    order = (
        Order.query
        .filter_by(
            payment_ref=reference
        )
        .first()
    )

    if not order:

        print(
            "WEBHOOK ORDER NOT FOUND:",
            reference
        )

        return jsonify({

            "success": False,

            "message":
                "Order not found."

        }), 404

    # =====================================================
    # COMPLETE ORDER
    # =====================================================

    success, message = (
        complete_paid_order(
            order,
            verified_payment
        )
    )

    if not success:

        print(
            "WEBHOOK ORDER ERROR:",
            message
        )

        return jsonify({

            "success": False,

            "message":
                message

        }), 400

    print(
        "PAYSTACK WEBHOOK SUCCESS:",
        reference,
        order.id
    )

    return jsonify({

        "success": True,

        "message":
            "Webhook processed successfully."

    }), 200


# =========================================================
# PAYSTACK CALLBACK
# =========================================================

@orders_bp.route(
    "/payment/callback"
)
def payment_callback():

    reference = request.args.get(
        "reference"
    )

    if not reference:

        return render_template(

            "payment_result.html",

            success=False,

            message=(
                "Payment reference was not received."
            )
        )

    if not PAYSTACK_SECRET_KEY:

        return render_template(

            "payment_result.html",

            success=False,

            message=(
                "Payment system is not configured."
            )
        )

    # =====================================================
    # VERIFY PAYMENT
    # =====================================================

    payment_data, error = (
        verify_paystack_transaction(
            reference
        )
    )

    if error:

        return render_template(

            "payment_result.html",

            success=False,

            message=error
        )

    if not payment_data:

        return render_template(

            "payment_result.html",

            success=False,

            message=(
                "Payment could not be verified."
            )
        )

    if payment_data.get(
        "status"
    ) != "success":

        return render_template(

            "payment_result.html",

            success=False,

            message=(
                "Your payment was not successful."
            )
        )

    # =====================================================
    # FIND ORDER
    # =====================================================

    order = (
        Order.query
        .filter_by(
            payment_ref=reference
        )
        .first()
    )

    if not order:

        return render_template(

            "payment_result.html",

            success=False,

            message=(
                "The order connected to this "
                "payment could not be found."
            )
        )

    # =====================================================
    # COMPLETE ORDER
    # =====================================================

    success, message = (
        complete_paid_order(
            order,
            payment_data
        )
    )

    if not success:

        return render_template(

            "payment_result.html",

            success=False,

            message=message
        )

    return render_template(

        "payment_result.html",

        success=True,

        order=order,

        order_number=
            f"NC-{order.id:06d}",

        payment_method=
            "Online Payment"
    )