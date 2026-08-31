from flask import Blueprint, request, jsonify, session

from models import db, Product, Order, OrderItem


# =========================================================
# ORDER BLUEPRINT
# =========================================================

order_bp = Blueprint(
    "order",
    __name__
)


# =========================================================
# CREATE ORDER
# =========================================================

@order_bp.route(
    "/api/orders",
    methods=["POST"]
)
def create_order():

    # -----------------------------------------------------
    # CHECK LOGIN
    # -----------------------------------------------------

    user_id = session.get("user_id")

    if not user_id:

        return jsonify({
            "success": False,
            "message": "Please sign in before placing an order."
        }), 401


    # -----------------------------------------------------
    # GET JSON DATA
    # -----------------------------------------------------

    data = request.get_json()

    if not data:

        return jsonify({
            "success": False,
            "message": "No order data was received."
        }), 400


    items = data.get("items", [])

    phone = str(
        data.get("phone", "")
    ).strip()

    address = str(
        data.get("address", "")
    ).strip()

    state = str(
        data.get("state", "")
    ).strip()

    city = str(
        data.get("city", "")
    ).strip()

    payment_method = str(
        data.get("payment_method", "")
    ).strip()


    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if not items:

        return jsonify({
            "success": False,
            "message": "Your cart is empty."
        }), 400


    if not phone:

        return jsonify({
            "success": False,
            "message": "Phone number is required."
        }), 400


    if not address:

        return jsonify({
            "success": False,
            "message": "Delivery address is required."
        }), 400


    if not state:

        return jsonify({
            "success": False,
            "message": "Please select your state."
        }), 400


    if not city:

        return jsonify({
            "success": False,
            "message": "City is required."
        }), 400


    if payment_method not in [
        "card",
        "bank",
        "delivery"
    ]:

        return jsonify({
            "success": False,
            "message": "Invalid payment method."
        }), 400


    # -----------------------------------------------------
    # BUILD FULL DELIVERY ADDRESS
    # -----------------------------------------------------

    delivery_address = (
        f"{address}, "
        f"{city}, "
        f"{state}"
    )


    # -----------------------------------------------------
    # CALCULATE ORDER TOTAL
    # -----------------------------------------------------

    subtotal = 0

    order_products = []


    for item in items:

        product_id = item.get("product_id")

        quantity = item.get("quantity", 1)


        try:

            product_id = int(product_id)
            quantity = int(quantity)

        except (
            TypeError,
            ValueError
        ):

            return jsonify({
                "success": False,
                "message": "Invalid product information."
            }), 400


        if quantity <= 0:

            return jsonify({
                "success": False,
                "message": "Invalid product quantity."
            }), 400


        # -------------------------------------------------
        # FIND PRODUCT IN DATABASE
        # -------------------------------------------------

        product = Product.query.get(
            product_id
        )


        if not product:

            return jsonify({
                "success": False,
                "message":
                    f"Product with ID {product_id} was not found."
            }), 404


        # -------------------------------------------------
        # CHECK STOCK
        # -------------------------------------------------

        if product.stock < quantity:

            return jsonify({
                "success": False,
                "message":
                    f"Only {product.stock} unit(s) of "
                    f"{product.name} are available."
            }), 400


        # -------------------------------------------------
        # CALCULATE
        # -------------------------------------------------

        item_total = (
            product.price * quantity
        )

        subtotal += item_total


        order_products.append({
            "product": product,
            "quantity": quantity,
            "price": product.price
        })


    # -----------------------------------------------------
    # DELIVERY FEE
    # -----------------------------------------------------

    if subtotal >= 50000:

        delivery_fee = 0

    else:

        delivery_fee = 2500


    total = (
        subtotal +
        delivery_fee
    )


    # -----------------------------------------------------
    # CREATE ORDER
    # -----------------------------------------------------

    order = Order(

        user_id=user_id,

        total=total,

        status="Pending",

        payment_ref=None,

        delivery_address=delivery_address,

        phone=phone

    )


    db.session.add(order)

    db.session.flush()


    # -----------------------------------------------------
    # CREATE ORDER ITEMS
    # -----------------------------------------------------

    for item in order_products:

        product = item["product"]

        quantity = item["quantity"]

        price = item["price"]


        order_item = OrderItem(

            order_id=order.id,

            product_id=product.id,

            quantity=quantity,

            price=price

        )


        db.session.add(order_item)


        # -------------------------------------------------
        # REDUCE STOCK
        # -------------------------------------------------

        product.stock -= quantity


    # -----------------------------------------------------
    # SAVE DATABASE
    # -----------------------------------------------------

    try:

        db.session.commit()

    except Exception as error:

        db.session.rollback()

        print(
            "Order creation error:",
            error
        )

        return jsonify({
            "success": False,
            "message":
                "Unable to create your order."
        }), 500


    # -----------------------------------------------------
    # ORDER NUMBER
    # -----------------------------------------------------

    order_number = (
        "NC-" +
        str(order.id).zfill(6)
    )


    # -----------------------------------------------------
    # SUCCESS
    # -----------------------------------------------------

    return jsonify({

        "success": True,

        "message":
            "Your order has been placed successfully.",

        "order_id":
            order.id,

        "order_number":
            order_number,

        "total":
            total,

        "payment_method":
            payment_method

    }), 201