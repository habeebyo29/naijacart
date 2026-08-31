/* =========================================================
   NAIJACART AUDIO PAGE JAVASCRIPT
========================================================= */


/* =========================================================
   UNIVERSAL CART
========================================================= */

const CART_KEY = "naijacart_cart";

let cart = JSON.parse(
    localStorage.getItem(CART_KEY)
) || [];


/* =========================================================
   SAVE CART
========================================================= */

function saveCart() {

    localStorage.setItem(
        CART_KEY,
        JSON.stringify(cart)
    );

}


/* =========================================================
   FORMAT PRICE
========================================================= */

function formatPrice(price) {

    return "₦" + Number(price).toLocaleString("en-NG");

}


/* =========================================================
   CART COUNT
========================================================= */

function updateCartCount() {

    const cartCount =
        document.getElementById("cartCount");

    if (!cartCount) {
        return;
    }

    const totalItems = cart.reduce(
        (total, item) =>
            total + (Number(item.quantity) || 1),
        0
    );

    cartCount.textContent = totalItems;

}


/* =========================================================
   ADD PRODUCT TO CART
========================================================= */

function addToCart(product) {

    /*
       Supports:

       addToCart({
           name: "AirPods Pro",
           price: 250000,
           image: "image.jpg"
       })

       It also supports older:

       addToCart("AirPods Pro")
    */


    if (typeof product === "string") {

        product = {
            name: product
        };

    }


    const name =
        product.name;


    const price =
        Number(product.price) || 0;


    const image =
        product.image || "";


    if (!name) {

        console.error(
            "Cannot add product: product name is missing."
        );

        return;

    }


    /* Find existing product */

    const existingProduct =
        cart.find(
            item => item.name === name
        );


    /* Increase quantity */

    if (existingProduct) {

        existingProduct.quantity =
            (Number(existingProduct.quantity) || 1) + 1;

    }


    /* Add new product */

    else {

        cart.push({

            name: name,

            price: price,

            image: image,

            quantity: 1

        });

    }


    saveCart();

    updateCartCount();

    showCartNotification(name);

}


/* =========================================================
   ADD PRODUCT FROM CARD
========================================================= */

function addProductFromCard(button) {

    const card =
        button.closest(".product-card");


    if (!card) {

        console.error(
            "Product card not found."
        );

        return;

    }


    /* PRODUCT NAME */

    const name =
        card.dataset.name ||
        card.querySelector(".product-name")?.textContent.trim();


    /* PRODUCT PRICE */

    let price =
        card.dataset.price;


    if (!price) {

        const priceElement =
            card.querySelector(".product-price");


        if (priceElement) {

            price =
                priceElement.textContent
                    .replace(/[₦,\s]/g, "")
                    .trim();

        }

    }


    /* PRODUCT IMAGE */

    const image =
        card.dataset.image ||
        card.querySelector("img")?.src ||
        "";


    addToCart({

        name: name,

        price: Number(price) || 0,

        image: image

    });

}


/* =========================================================
   GO TO CART
========================================================= */

function showCart() {

    window.location.href =
        "cart.html";

}


/* =========================================================
   CART NOTIFICATION
========================================================= */

function showCartNotification(productName) {

    let notification =
        document.querySelector(
            ".cart-notification"
        );


    /* Create notification */

    if (!notification) {

        notification =
            document.createElement("div");


        notification.className =
            "cart-notification";


        notification.innerHTML = `

            <span>✓</span>

            <strong></strong>

        `;


        document.body.appendChild(
            notification
        );

    }


    const message =
        notification.querySelector(
            "strong"
        );


    message.textContent =
        `${productName} added to cart`;


    notification.classList.add(
        "show"
    );


    clearTimeout(
        notification.hideTimer
    );


    notification.hideTimer =
        setTimeout(() => {

            notification.classList.remove(
                "show"
            );

        }, 2500);

}


/* =========================================================
   SIMPLE TOAST
========================================================= */

function showToast(message) {

    const oldToast =
        document.querySelector(
            ".cart-toast"
        );


    if (oldToast) {
        oldToast.remove();
    }


    const toast =
        document.createElement("div");


    toast.className =
        "cart-toast";


    toast.textContent =
        message;


    Object.assign(
        toast.style,
        {

            position: "fixed",

            bottom: "25px",

            right: "25px",

            background: "#075c3f",

            color: "#fff",

            padding: "13px 18px",

            borderRadius: "10px",

            fontSize: "13px",

            fontWeight: "700",

            boxShadow:
                "0 12px 30px rgba(0,0,0,.18)",

            zIndex: "9999",

            transform:
                "translateY(20px)",

            opacity: "0",

            transition:
                ".25s ease"

        }
    );


    document.body.appendChild(
        toast
    );


    requestAnimationFrame(() => {

        toast.style.transform =
            "translateY(0)";

        toast.style.opacity =
            "1";

    });


    setTimeout(() => {

        toast.style.opacity =
            "0";

        toast.style.transform =
            "translateY(20px)";


        setTimeout(() => {

            toast.remove();

        }, 250);

    }, 2200);

}


/* =========================================================
   SEARCH + CATEGORY FILTER
========================================================= */

function filterProducts() {

    const searchInput =
        document.getElementById(
            "searchInput"
        );


    const categorySelect =
        document.getElementById(
            "categorySelect"
        );


    const searchTerm =
        searchInput
            ? searchInput.value
                .trim()
                .toLowerCase()
            : "";


    const category =
        categorySelect
            ? categorySelect.value
            : "all";


    const products =
        document.querySelectorAll(
            ".product-card"
        );


    let visibleProducts = 0;


    products.forEach(product => {

        const name =
            (
                product.dataset.name ||
                ""
            ).toLowerCase();


        const brand =
            (
                product.dataset.brand ||
                ""
            ).toLowerCase();


        const productCategory =
            (
                product.dataset.category ||
                ""
            ).toLowerCase();


        const matchesSearch =
            name.includes(searchTerm) ||
            brand.includes(searchTerm);


        const matchesCategory =
            category === "all" ||
            productCategory ===
            category.toLowerCase();


        if (
            matchesSearch &&
            matchesCategory
        ) {

            product.style.display =
                "";

            visibleProducts++;

        }

        else {

            product.style.display =
                "none";

        }

    });


    showNoProducts(
        visibleProducts
    );

}


/* =========================================================
   SEARCH WHILE TYPING
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const searchInput =
            document.getElementById(
                "searchInput"
            );


        if (searchInput) {

            searchInput.addEventListener(
                "input",
                filterProducts
            );

        }


        const categorySelect =
            document.getElementById(
                "categorySelect"
            );


        if (categorySelect) {

            categorySelect.addEventListener(
                "change",
                filterProducts
            );

        }


        updateCartCount();

    }
);


/* =========================================================
   BRAND FILTER
========================================================= */

function filterBrand(
    brand,
    button
) {

    const products =
        document.querySelectorAll(
            ".product-card"
        );


    document
        .querySelectorAll(".brand")
        .forEach(btn => {

            btn.classList.remove(
                "active"
            );

        });


    if (button) {

        button.classList.add(
            "active"
        );

    }


    let visibleProducts = 0;


    products.forEach(product => {

        const productBrand =
            product.dataset.brand ||
            "";


        if (
            brand === "all" ||
            productBrand === brand
        ) {

            product.style.display =
                "";

            visibleProducts++;

        }

        else {

            product.style.display =
                "none";

        }

    });


    showNoProducts(
        visibleProducts
    );

}


/* =========================================================
   SHOW ALL BRANDS
========================================================= */

function showAllBrands(event) {

    if (event) {
        event.preventDefault();
    }


    const allButton =
        document.querySelector(
            ".brand"
        );


    filterBrand(
        "all",
        allButton
    );

}


/* =========================================================
   NO PRODUCTS MESSAGE
========================================================= */

function showNoProducts(count) {

    const noProducts =
        document.getElementById(
            "noProducts"
        );


    const grid =
        document.getElementById(
            "productsGrid"
        );


    if (!noProducts || !grid) {
        return;
    }


    if (count === 0) {

        grid.style.display =
            "none";

        noProducts.style.display =
            "block";

    }

    else {

        grid.style.display =
            "grid";

        noProducts.style.display =
            "none";

    }

}


/* =========================================================
   RESET FILTERS
========================================================= */

function resetFilters() {

    const searchInput =
        document.getElementById(
            "searchInput"
        );


    const categorySelect =
        document.getElementById(
            "categorySelect"
        );


    if (searchInput) {

        searchInput.value =
            "";

    }


    if (categorySelect) {

        categorySelect.value =
            "all";

    }


    const allButton =
        document.querySelector(
            ".brand"
        );


    filterBrand(
        "all",
        allButton
    );

}


/* =========================================================
   SORT PRODUCTS
========================================================= */

function sortProducts() {

    const sortSelect =
        document.getElementById(
            "sortSelect"
        );


    const grid =
        document.getElementById(
            "productsGrid"
        );


    if (!sortSelect || !grid) {
        return;
    }


    const sortValue =
        sortSelect.value;


    const products =
        Array.from(
            grid.querySelectorAll(
                ".product-card"
            )
        );


    if (sortValue === "low") {

        products.sort(
            (a, b) =>
                Number(
                    a.dataset.price
                ) -
                Number(
                    b.dataset.price
                )
        );

    }


    else if (sortValue === "high") {

        products.sort(
            (a, b) =>
                Number(
                    b.dataset.price
                ) -
                Number(
                    a.dataset.price
                )
        );

    }


    else if (sortValue === "rating") {

        products.sort(
            (a, b) =>
                Number(
                    b.dataset.rating
                ) -
                Number(
                    a.dataset.rating
                )
        );

    }


    products.forEach(
        product => {

            grid.appendChild(
                product
            );

        }
    );

}


/* =========================================================
   HEART / WISHLIST
========================================================= */

function toggleHeart(button) {

    if (!button) {
        return;
    }


    button.classList.toggle(
        "liked"
    );


    if (
        button.classList.contains(
            "liked"
        )
    ) {

        button.textContent =
            "♥";


        showToast(
            "Added to wishlist ♡"
        );

    }

    else {

        button.textContent =
            "♡";

    }

}


/* =========================================================
   WISHLIST
========================================================= */

function toggleWishlist() {

    showToast(
        "Wishlist is coming soon ♡"
    );

}


/* =========================================================
   COMPARE
========================================================= */

function showCompare() {

    showToast(
        "Compare feature is coming soon ⇄"
    );

}


/* =========================================================
   SCROLL TO PRODUCTS
========================================================= */

function scrollToProducts() {

    const products =
        document.getElementById(
            "products"
        );


    if (products) {

        products.scrollIntoView({
            behavior: "smooth"
        });

    }

}


/* =========================================================
   NEWSLETTER
========================================================= */

function subscribeNewsletter(event) {

    event.preventDefault();


    const input =
        event.target.querySelector(
            "input"
        );


    if (!input) {
        return;
    }


    const email =
        input.value.trim();


    if (!email) {
        return;
    }


    showToast(
        "Thanks! You're subscribed 🎧"
    );


    event.target.reset();

}


/* =========================================================
   INITIALIZE CART COUNT
========================================================= */

updateCartCount();