/* =====================================================
   NAIJACART — EMPTY CART
===================================================== */


/* =====================================================
   GET ELEMENTS
===================================================== */

const cartButton =
    document.getElementById("cartButton");

const cartCount =
    document.getElementById("cartCount");

const emptyCartMessage =
    document.getElementById("emptyCartMessage");

const closeEmptyCart =
    document.getElementById("closeEmptyCart");

const startShoppingBtn =
    document.getElementById("startShoppingBtn");


/* =====================================================
   ALWAYS KEEP CART COUNT AT 0
===================================================== */

function keepCartEmpty() {

    if (cartCount) {

        cartCount.textContent = "0";

    }

}


/* =====================================================
   SHOW EMPTY CART
===================================================== */

function showEmptyCart() {

    keepCartEmpty();

    if (!emptyCartMessage) {
        return;
    }

    emptyCartMessage.classList.add("show");

}


/* =====================================================
   CLOSE EMPTY CART
===================================================== */

function closeEmptyCartPopup() {

    if (!emptyCartMessage) {
        return;
    }

    emptyCartMessage.classList.remove("show");

}


/* =====================================================
   CART BUTTON CLICK
===================================================== */

if (cartButton) {

    cartButton.addEventListener(
        "click",
        function() {

            showEmptyCart();

        }
    );

}


/* =====================================================
   CLOSE BUTTON
===================================================== */

if (closeEmptyCart) {

    closeEmptyCart.addEventListener(
        "click",
        function() {

            closeEmptyCartPopup();

        }
    );

}


/* =====================================================
   START SHOPPING
===================================================== */

if (startShoppingBtn) {

    startShoppingBtn.addEventListener(
        "click",
        function() {

            window.location.href =
                "/naijacart-frontend/smartphones.html";

        }
    );

}


/* =====================================================
   CLICK OUTSIDE POPUP
===================================================== */

if (emptyCartMessage) {

    emptyCartMessage.addEventListener(
        "click",
        function(event) {

            if (
                event.target ===
                emptyCartMessage
            ) {

                closeEmptyCartPopup();

            }

        }
    );

}


/* =====================================================
   ESCAPE KEY
===================================================== */

document.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Escape"
        ) {

            closeEmptyCartPopup();

        }

    }
);


/* =====================================================
   INITIALIZE
===================================================== */

keepCartEmpty();