/* =========================================================
   NAIJACART — SHARED CART
   PRODUCT NAME BASED CART
========================================================= */

const CART_KEY = "naijacart_cart";
const FREE_DELIVERY_LIMIT = 50000;
const DELIVERY_FEE = 2500;


/* =========================================================
   GET CART
========================================================= */

function getCart() {

    try {

        const cart = JSON.parse(
            localStorage.getItem(CART_KEY)
        );

        return Array.isArray(cart)
            ? cart
            : [];

    } catch (error) {

        console.error(
            "Unable to read cart:",
            error
        );

        return [];

    }

}


/* =========================================================
   SAVE CART
========================================================= */

function saveCart(cart) {

    localStorage.setItem(
        CART_KEY,
        JSON.stringify(cart)
    );

}


/* =========================================================
   FORMAT PRICE
========================================================= */

function formatPrice(price) {

    return "₦" +
        Number(price || 0).toLocaleString(
            "en-NG"
        );

}


/* =========================================================
   CART COUNT
========================================================= */

function getCartItemCount() {

    return getCart().reduce(
        (total, item) => {

            return total +
                (Number(item.quantity) || 1);

        },
        0
    );

}


function updateCartCount() {

    const cartCount =
        document.getElementById("cartCount");

    if (!cartCount) {
        return;
    }

    cartCount.textContent =
        getCartItemCount();

}


/* =========================================================
   ADD TO CART
========================================================= */

function addToCart(
    productName,
    price,
    image
) {

    const cart = getCart();

    const cleanName =
        String(productName || "").trim();

    const cleanPrice =
        Number(
            String(price || "")
                .replace(/[₦,]/g, "")
        ) || 0;


    if (!cleanName) {

        console.error(
            "Product name is missing."
        );

        return;

    }


    const existingProduct =
        cart.find(
            item =>
                String(item.name || "")
                    .trim()
                    .toLowerCase() ===
                cleanName.toLowerCase()
        );


    if (existingProduct) {

        existingProduct.quantity =
            (Number(existingProduct.quantity) || 1) + 1;

        existingProduct.price =
            cleanPrice;

        if (image) {

            existingProduct.image =
                image;

        }

    } else {

        cart.push({

            name:
                cleanName,

            price:
                cleanPrice,

            image:
                image || "",

            quantity:
                1

        });

    }


    saveCart(cart);

    updateCartCount();

    showCartMessage(cleanName);

}


/* =========================================================
   CART TOAST
========================================================= */

function showCartMessage(productName) {

    const oldToast =
        document.querySelector(".cart-toast");


    if (oldToast) {
        oldToast.remove();
    }


    const toast =
        document.createElement("div");


    toast.className =
        "cart-toast";


    toast.innerHTML = `

        <span>✓</span>

        <div>
            <strong>Added to cart</strong>
            <small>${escapeHTML(productName)}</small>
        </div>

        <a href="cart.html">
            View Cart
        </a>

    `;


    Object.assign(
        toast.style,
        {

            position: "fixed",
            right: "20px",
            bottom: "20px",
            zIndex: "99999",

            display: "flex",
            alignItems: "center",
            gap: "12px",

            padding: "14px 16px",

            background: "#ffffff",

            border: "1px solid #e5e7eb",

            borderRadius: "12px",

            boxShadow:
                "0 12px 35px rgba(0,0,0,.15)",

            color: "#17221d",

            transition: ".3s"

        }
    );


    const icon =
        toast.querySelector("span");


    Object.assign(
        icon.style,
        {

            width: "32px",
            height: "32px",

            borderRadius: "50%",

            background: "#eaf7f1",

            color: "#075c3f",

            display: "grid",
            placeItems: "center",

            fontWeight: "900"

        }
    );


    const small =
        toast.querySelector("small");


    Object.assign(
        small.style,
        {

            display: "block",

            color: "#6b7280",

            marginTop: "2px",

            fontSize: "11px"

        }
    );


    const link =
        toast.querySelector("a");


    Object.assign(
        link.style,
        {

            color: "#075c3f",

            fontSize: "12px",

            fontWeight: "800",

            marginLeft: "5px",

            textDecoration: "none"

        }
    );


    document.body.appendChild(toast);


    setTimeout(
        () => {

            toast.style.opacity =
                "0";

            toast.style.transform =
                "translateY(10px)";


            setTimeout(
                () => {

                    toast.remove();

                },
                300
            );

        },
        3000
    );

}


/* =========================================================
   ESCAPE HTML
========================================================= */

function escapeHTML(value) {

    return String(value || "")
        .replace(
            /[&<>"']/g,
            character => {

                const entities = {

                    "&": "&amp;",
                    "<": "&lt;",
                    ">": "&gt;",
                    '"': "&quot;",
                    "'": "&#039;"

                };

                return entities[character];

            }
        );

}


/* =========================================================
   RENDER CART
========================================================= */

function renderCart() {

    const cart =
        getCart();


    const cartItems =
        document.getElementById("cartItems");


    const cartLayout =
        document.getElementById("cartLayout");


    const emptyCart =
        document.getElementById("emptyCart");


    if (!cartItems) {
        return;
    }


    if (cart.length === 0) {

        cartItems.innerHTML = "";


        if (cartLayout) {

            cartLayout.style.display =
                "none";

        }


        if (emptyCart) {

            emptyCart.style.display =
                "block";

        }


        updateCartSummary();

        return;

    }


    if (cartLayout) {

        cartLayout.style.display =
            "grid";

    }


    if (emptyCart) {

        emptyCart.style.display =
            "none";

    }


    cartItems.innerHTML =
        cart.map(
            (item, index) => {

                const quantity =
                    Math.max(
                        Number(item.quantity) || 1,
                        1
                    );


                const price =
                    Number(item.price) || 0;


                const itemTotal =
                    price * quantity;


                const name =
                    escapeHTML(
                        item.name ||
                        "Product"
                    );


                const image =
                    escapeHTML(
                        item.image ||
                        ""
                    );


                return `

                    <article class="cart-item">

                        <div class="cart-item-image">

                            ${
                                image
                                    ? `
                                        <img
                                            src="${image}"
                                            alt="${name}"
                                            onerror="this.style.display='none'"
                                        >
                                      `
                                    : `
                                        <span
                                            style="
                                                font-size:28px;
                                                opacity:.35;
                                            "
                                        >
                                            📦
                                        </span>
                                      `
                            }

                        </div>


                        <div class="cart-item-info">

                            <h3>
                                ${name}
                            </h3>

                            <strong>
                                ${formatPrice(price)}
                            </strong>


                            <div class="cart-item-actions">

                                <div class="quantity-control">

                                    <button
                                        type="button"
                                        onclick="changeQuantity(${index}, -1)"
                                        aria-label="Decrease quantity"
                                    >
                                        −
                                    </button>

                                    <span>
                                        ${quantity}
                                    </span>

                                    <button
                                        type="button"
                                        onclick="changeQuantity(${index}, 1)"
                                        aria-label="Increase quantity"
                                    >
                                        +
                                    </button>

                                </div>


                                <button
                                    type="button"
                                    class="remove-item"
                                    onclick="removeFromCart(${index})"
                                >
                                    🗑 Remove
                                </button>

                            </div>

                        </div>


                        <div class="cart-item-total">

                            <strong>
                                ${formatPrice(itemTotal)}
                            </strong>

                        </div>

                    </article>

                `;

            }
        ).join("");


    updateCartSummary();

}


/* =========================================================
   CHANGE QUANTITY
========================================================= */

function changeQuantity(
    index,
    change
) {

    const cart =
        getCart();


    if (!cart[index]) {
        return;
    }


    let quantity =
        Number(cart[index].quantity) || 1;


    quantity += change;


    if (quantity <= 0) {

        cart.splice(
            index,
            1
        );

    } else {

        cart[index].quantity =
            quantity;

    }


    saveCart(cart);

    renderCart();

    updateCartCount();

}


/* =========================================================
   REMOVE PRODUCT
========================================================= */

function removeFromCart(index) {

    const cart =
        getCart();


    if (!cart[index]) {
        return;
    }


    const name =
        cart[index].name ||
        "Product";


    cart.splice(
        index,
        1
    );


    saveCart(cart);

    renderCart();

    updateCartCount();


    showCartMessage(
        `${name} removed`
    );

}


/* =========================================================
   CLEAR CART
========================================================= */

function clearCart() {

    const cart =
        getCart();


    if (cart.length === 0) {
        return;
    }


    const confirmed =
        confirm(
            "Are you sure you want to clear your cart?"
        );


    if (!confirmed) {
        return;
    }


    localStorage.removeItem(
        CART_KEY
    );


    renderCart();

    updateCartCount();

}


/* =========================================================
   SUBTOTAL
========================================================= */

function calculateSubtotal() {

    return getCart().reduce(
        (subtotal, item) => {

            const price =
                Number(item.price) || 0;

            const quantity =
                Number(item.quantity) || 1;


            return subtotal +
                (price * quantity);

        },
        0
    );

}


/* =========================================================
   DELIVERY
========================================================= */

function calculateDelivery(subtotal) {

    if (subtotal <= 0) {
        return 0;
    }


    if (
        subtotal >=
        FREE_DELIVERY_LIMIT
    ) {

        return 0;

    }


    return DELIVERY_FEE;

}


/* =========================================================
   UPDATE SUMMARY
========================================================= */

function updateCartSummary() {

    const cart =
        getCart();


    const subtotal =
        calculateSubtotal();


    const delivery =
        calculateDelivery(
            subtotal
        );


    const total =
        subtotal +
        delivery;


    const subtotalElement =
        document.getElementById("subtotal");


    const deliveryElement =
        document.getElementById("delivery");


    const totalElement =
        document.getElementById("total");


    if (subtotalElement) {

        subtotalElement.textContent =
            formatPrice(subtotal);

    }


    if (deliveryElement) {

        deliveryElement.textContent =
            delivery === 0
                ? "FREE"
                : formatPrice(delivery);

    }


    if (totalElement) {

        totalElement.textContent =
            formatPrice(total);

    }


    const itemCount =
        document.getElementById("itemCount");


    if (itemCount) {

        const count =
            getCartItemCount();


        itemCount.textContent =
            count === 1
                ? "1 item"
                : `${count} items`;

    }


    const subtitle =
        document.getElementById("cartSubtitle");


    if (subtitle) {

        const count =
            getCartItemCount();


        subtitle.textContent =
            count === 0
                ? "Your cart is currently empty."
                : `You have ${count} ${
                    count === 1
                        ? "item"
                        : "items"
                  } ready for checkout.`;

    }


    updateDeliveryProgress(
        subtotal
    );


    const checkoutButton =
        document.getElementById(
            "checkoutButton"
        );


    if (checkoutButton) {

        checkoutButton.disabled =
            cart.length === 0;

    }

}


/* =========================================================
   DELIVERY PROGRESS
========================================================= */

function updateDeliveryProgress(subtotal) {

    const progress =
        document.getElementById(
            "deliveryProgress"
        );


    const progressText =
        document.getElementById(
            "deliveryProgressText"
        );


    if (
        !progress ||
        !progressText
    ) {

        return;

    }


    if (
        subtotal >=
        FREE_DELIVERY_LIMIT
    ) {

        progress.style.width =
            "100%";


        progressText.textContent =
            "✓ You qualify for FREE delivery";


        return;

    }


    const percentage =
        Math.min(
            (
                subtotal /
                FREE_DELIVERY_LIMIT
            ) * 100,
            100
        );


    progress.style.width =
        percentage + "%";


    const remaining =
        FREE_DELIVERY_LIMIT -
        subtotal;


    progressText.textContent =
        `${formatPrice(remaining)} for FREE delivery`;

}


/* =========================================================
   SEARCH
========================================================= */

function searchProducts() {

    const input =
        document.getElementById(
            "searchInput"
        );


    const searchTerm =
        input
            ? input.value
                .trim()
                .toLowerCase()
            : "";


    const items =
        document.querySelectorAll(
            ".cart-item"
        );


    const searchMessage =
        document.getElementById(
            "searchMessage"
        );


    if (
        !searchTerm ||
        items.length === 0
    ) {

        items.forEach(
            item => {

                item.style.display =
                    "";

            }
        );


        if (searchMessage) {

            searchMessage.style.display =
                "none";

        }

        return;

    }


    let matches = 0;


    items.forEach(
        item => {

            const name =
                item
                    .querySelector("h3")
                    ?.textContent
                    .toLowerCase() || "";


            const match =
                name.includes(
                    searchTerm
                );


            item.style.display =
                match
                    ? ""
                    : "none";


            if (match) {
                matches++;
            }

        }
    );


    if (searchMessage) {

        searchMessage.style.display =
            matches === 0
                ? "block"
                : "none";

    }

}


/* =========================================================
   OPEN CHECKOUT
========================================================= */

function openCheckout() {

    const cart =
        getCart();


    if (cart.length === 0) {

        alert(
            "Your cart is empty. Please add a product first."
        );

        return;

    }


    const modal =
        document.getElementById(
            "checkoutModal"
        );


    if (!modal) {

        console.error(
            "checkoutModal was not found."
        );

        return;

    }


    const checkoutContent =
        document.getElementById(
            "checkoutContent"
        );


    const orderSuccess =
        document.getElementById(
            "orderSuccess"
        );


    if (checkoutContent) {

        checkoutContent.style.display =
            "block";

    }


    if (orderSuccess) {

        orderSuccess.style.display =
            "none";

    }


    modal.style.display =
        "flex";


    modal.setAttribute(
        "aria-hidden",
        "false"
    );


    document.body.classList.add(
        "checkout-open"
    );


    updateCheckout();

    togglePaymentFields();

}


/* =========================================================
   CLOSE CHECKOUT
========================================================= */

function closeCheckout() {

    const modal =
        document.getElementById(
            "checkoutModal"
        );


    if (!modal) {
        return;
    }


    modal.style.display =
        "none";


    modal.setAttribute(
        "aria-hidden",
        "true"
    );


    document.body.classList.remove(
        "checkout-open"
    );

}


/* =========================================================
   UPDATE CHECKOUT
========================================================= */

function updateCheckout() {

    const cart =
        getCart();


    const subtotal =
        calculateSubtotal();


    const delivery =
        calculateDelivery(
            subtotal
        );


    const total =
        subtotal +
        delivery;


    const checkoutProducts =
        document.getElementById(
            "checkoutProducts"
        );


    if (checkoutProducts) {

        checkoutProducts.innerHTML =
            cart.map(
                item => {

                    const quantity =
                        Number(item.quantity) || 1;


                    const price =
                        Number(item.price) || 0;


                    const name =
                        escapeHTML(
                            item.name ||
                            "Product"
                        );


                    return `

                        <div class="checkout-product">

                            <div>

                                <strong>
                                    ${name}
                                </strong>

                                <span>
                                    Qty: ${quantity}
                                </span>

                            </div>

                            <strong>
                                ${formatPrice(
                                    price * quantity
                                )}
                            </strong>

                        </div>

                    `;

                }
            ).join("");

    }


    const checkoutItemCount =
        document.getElementById(
            "checkoutItemCount"
        );


    if (checkoutItemCount) {

        const count =
            getCartItemCount();


        checkoutItemCount.textContent =
            count === 1
                ? "1 item"
                : `${count} items`;

    }


    const checkoutSubtotal =
        document.getElementById(
            "checkoutSubtotal"
        );


    const checkoutDelivery =
        document.getElementById(
            "checkoutDelivery"
        );


    const checkoutTotal =
        document.getElementById(
            "checkoutTotal"
        );


    const placeOrderAmount =
        document.getElementById(
            "placeOrderAmount"
        );


    if (checkoutSubtotal) {

        checkoutSubtotal.textContent =
            formatPrice(subtotal);

    }


    if (checkoutDelivery) {

        checkoutDelivery.textContent =
            delivery === 0
                ? "FREE"
                : formatPrice(delivery);

    }


    if (checkoutTotal) {

        checkoutTotal.textContent =
            formatPrice(total);

    }


    if (placeOrderAmount) {

        placeOrderAmount.textContent =
            formatPrice(total);

    }

}


/* =========================================================
   PAYMENT FIELDS
========================================================= */

function togglePaymentFields() {

    const selected =
        document.querySelector(
            'input[name="paymentMethod"]:checked'
        );


    const cardFields =
        document.getElementById(
            "cardFields"
        );


    const bankFields =
        document.getElementById(
            "bankFields"
        );


    const deliveryFields =
        document.getElementById(
            "deliveryFields"
        );


    if (!selected) {
        return;
    }


    if (cardFields) {

        cardFields.style.display =
            selected.value === "card"
                ? "flex"
                : "none";

    }


    if (bankFields) {

        bankFields.style.display =
            selected.value === "bank"
                ? "flex"
                : "none";

    }


    if (deliveryFields) {

        deliveryFields.style.display =
            selected.value === "delivery"
                ? "flex"
                : "none";

    }

}


/* =========================================================
   PLACE ORDER
========================================================= */

async function placeOrder(event) {

    event.preventDefault();


    const cart =
        getCart();


    if (cart.length === 0) {

        alert(
            "Your cart is empty."
        );

        return;

    }


    const form =
        document.getElementById(
            "checkoutForm"
        );


    if (!form) {

        alert(
            "Checkout form was not found."
        );

        return;

    }


    if (!form.checkValidity()) {

        form.reportValidity();

        return;

    }


    const payment =
        document.querySelector(
            'input[name="paymentMethod"]:checked'
        );


    const paymentMethod =
        payment
            ? payment.value
            : "delivery";


    /* =====================================================
       PREPARE ITEMS
    ===================================================== */

    const items =
        cart.map(
            item => ({

                product_name:
                    String(
                        item.name || ""
                    ).trim(),

                quantity:
                    Math.max(
                        Number(
                            item.quantity
                        ) || 1,
                        1
                    )

            })
        );


    const invalidItem =
        items.find(
            item =>
                !item.product_name
        );


    if (invalidItem) {

        alert(
            "One of the products in your cart is invalid. Please remove it and add the product again."
        );

        return;

    }


    /* =====================================================
       CUSTOMER
    ===================================================== */

    const customer = {

        firstName:
            document
                .getElementById("firstName")
                .value
                .trim(),

        lastName:
            document
                .getElementById("lastName")
                .value
                .trim(),

        phone:
            document
                .getElementById("phone")
                .value
                .trim(),

        email:
            document
                .getElementById("email")
                .value
                .trim(),

        address:
            document
                .getElementById("address")
                .value
                .trim(),

        state:
            document
                .getElementById("state")
                .value
                .trim(),

        city:
            document
                .getElementById("city")
                .value
                .trim()

    };


    /* =====================================================
       BUTTON
    ===================================================== */

    const placeOrderButton =
        form.querySelector(
            ".place-order-btn"
        );


    if (placeOrderButton) {

        placeOrderButton.disabled =
            true;

        placeOrderButton.style.opacity =
            ".6";

        placeOrderButton.style.cursor =
            "not-allowed";

    }


    try {

        /* =================================================
           SEND ORDER TO FLASK
        ================================================= */

        const response =
            await fetch(
                "/orders/create",
                {

                    method:
                        "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body:
                        JSON.stringify({

                            customer:
                                customer,

                            items:
                                items,

                            payment_method:
                                paymentMethod

                        })

                }
            );


        let data;


        try {

            data =
                await response.json();

        } catch {

            data = {};

        }


        console.log(
            "Order response:",
            data
        );


        /* =================================================
           LOGIN REQUIRED
        ================================================= */

        if (
            response.status ===
            401
        ) {

            alert(
                "Please sign in before placing your order."
            );


            window.location.href =
                "/login";


            return;

        }


        /* =================================================
           BACKEND ERROR
        ================================================= */

        if (
            !response.ok ||
            !data.success
        ) {

            alert(
                data.message ||
                "Unable to place your order."
            );

            return;

        }


        /* =================================================
           PAYSTACK PAYMENT
        ================================================= */

        if (
            data.payment_required &&
            data.authorization_url
        ) {

            /*
             * The Flask backend has successfully
             * initialized the Paystack transaction.
             *
             * Redirect the customer to Paystack's
             * secure hosted payment page.
             */

            window.location.href =
                data.authorization_url;

            return;

        }


        /* =================================================
           PAY ON DELIVERY SUCCESS
        ================================================= */

        const orderNumberElement =
            document.getElementById(
                "orderNumber"
            );


        const successPayment =
            document.getElementById(
                "successPayment"
            );


        const successTotal =
            document.getElementById(
                "successTotal"
            );


        if (orderNumberElement) {

            orderNumberElement.textContent =
                data.order_number ||
                "NC-" +
                Date.now();

        }


        if (successPayment) {

            const paymentLabels = {

                card:
                    "Debit / Credit Card",

                bank:
                    "Bank Transfer",

                delivery:
                    "Pay on Delivery"

            };


            successPayment.textContent =
                paymentLabels[
                    paymentMethod
                ] ||
                "Payment";

        }


        if (successTotal) {

            const serverTotal =
                Number(data.total);


            const finalTotal =
                Number.isFinite(serverTotal)
                    ? serverTotal
                    : (
                        calculateSubtotal() +
                        calculateDelivery(
                            calculateSubtotal()
                        )
                    );


            successTotal.textContent =
                formatPrice(
                    finalTotal
                );

        }


        /* =================================================
           SHOW SUCCESS
        ================================================= */

        const checkoutContent =
            document.getElementById(
                "checkoutContent"
            );


        const orderSuccess =
            document.getElementById(
                "orderSuccess"
            );


        if (checkoutContent) {

            checkoutContent.style.display =
                "none";

        }


        if (orderSuccess) {

            orderSuccess.style.display =
                "block";

        }


        /* =================================================
           CLEAR CART
        ================================================= */

        localStorage.removeItem(
            CART_KEY
        );


        updateCartCount();

        renderCart();


    } catch (error) {

        console.error(
            "ORDER ERROR:",
            error
        );


        alert(
            "Unable to connect to the server. Please make sure Flask is running."
        );


    } finally {

        /*
         * If the customer was redirected to Paystack,
         * the page normally leaves before this matters.
         *
         * For normal errors or Pay on Delivery,
         * restore the button.
         */

        if (placeOrderButton) {

            placeOrderButton.disabled =
                false;

            placeOrderButton.style.opacity =
                "";

            placeOrderButton.style.cursor =
                "";

        }

    }

}


/* =========================================================
   FINISH ORDER
========================================================= */

function finishOrder() {

    window.location.href =
        "index.html";

}


/* =========================================================
   NEWSLETTER
========================================================= */

function subscribeNewsletter(event) {

    event.preventDefault();


    alert(
        "Thank you for subscribing to NaijaCart!"
    );

}


/* =========================================================
   KEYBOARD
========================================================= */

document.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key ===
            "Escape"
        ) {

            closeCheckout();

        }

    }
);


/* =========================================================
   INITIALIZE
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function() {

        updateCartCount();

        renderCart();

        togglePaymentFields();


        const searchInput =
            document.getElementById(
                "searchInput"
            );


        if (searchInput) {

            searchInput.addEventListener(
                "input",
                searchProducts
            );

        }


        /*
         * Update payment fields whenever
         * the customer changes payment method.
         */

        const paymentMethods =
            document.querySelectorAll(
                'input[name="paymentMethod"]'
            );


        paymentMethods.forEach(
            radio => {

                radio.addEventListener(
                    "change",
                    togglePaymentFields
                );

            }
        );

    }
);


/* =========================================================
   UPDATE FROM ANOTHER TAB
========================================================= */

window.addEventListener(
    "storage",
    function(event) {

        if (
            event.key ===
            CART_KEY
        ) {

            updateCartCount();

            renderCart();

        }

    }
);