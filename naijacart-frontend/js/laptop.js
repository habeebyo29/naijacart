let cart =
    JSON.parse(localStorage.getItem("naijacart_cart")) || [];

let currentBrand = "all";


/* =====================================================
   CART COUNT
===================================================== */

function updateCartCount() {

    const cartCount =
        document.getElementById("cartCount");

    if (!cartCount) return;

    const totalItems = cart.reduce(
        (total, item) => total + Number(item.quantity || 1),
        0
    );

    cartCount.textContent = totalItems;
}


/* =====================================================
   ADD TO CART
===================================================== */

function addToCart(name, brand, price, image) {

    const existingProduct = cart.find(
        item => item.name === name
    );


    if (existingProduct) {

        existingProduct.quantity =
            Number(existingProduct.quantity || 1) + 1;

    } else {

        cart.push({

            name: name,

            brand: brand,

            price: Number(price),

            image: image,

            quantity: 1

        });

    }


    localStorage.setItem(
        "naijacart_cart",
        JSON.stringify(cart)
    );


    updateCartCount();


    showCartMessage(
        `${name} added to your cart 🛒`
    );
}


/* =====================================================
   CART MESSAGE
===================================================== */

function showCartMessage(message) {

    const oldMessage =
        document.querySelector(".cart-message");

    if (oldMessage) {
        oldMessage.remove();
    }


    const notification =
        document.createElement("div");

    notification.className = "cart-message";

    notification.innerHTML = `
        <span>✓</span>
        <div>
            <strong>Added to cart</strong>
            <p>${message}</p>
        </div>

        <a href="cart.html">
            View Cart
        </a>
    `;


    document.body.appendChild(notification);


    setTimeout(() => {

        notification.classList.add("show");

    }, 10);


    setTimeout(() => {

        notification.classList.remove("show");

        setTimeout(() => {
            notification.remove();
        }, 300);

    }, 3500);
}


/* =====================================================
   SEARCH
===================================================== */

const searchInput =
    document.getElementById("searchInput");


searchInput.addEventListener(
    "input",
    filterProducts
);


function filterProducts() {

    const searchValue =
        searchInput.value
            .toLowerCase()
            .trim();


    const products =
        document.querySelectorAll(
            ".product-card"
        );


    let visible = 0;


    products.forEach(product => {

        const brand =
            product.dataset.brand.toLowerCase();

        const name =
            product.dataset.name.toLowerCase();


        const brandMatch =
            currentBrand === "all" ||
            brand === currentBrand;


        const searchMatch =
            name.includes(searchValue) ||
            brand.includes(searchValue);


        if (
            brandMatch &&
            searchMatch
        ) {

            product.style.display = "";

            visible++;

        } else {

            product.style.display = "none";

        }

    });


    document.getElementById(
        "noProducts"
    ).style.display =
        visible === 0
            ? "block"
            : "none";
}


/* =====================================================
   BRAND FILTER
===================================================== */

function filterBrand(brand, button) {

    currentBrand = brand;


    document
        .querySelectorAll(".brand")
        .forEach(btn => {

            btn.classList.remove("active");

        });


    button.classList.add("active");


    filterProducts();
}


/* =====================================================
   RESET FILTER
===================================================== */

function resetFilters() {

    currentBrand = "all";

    searchInput.value = "";


    document
        .querySelectorAll(".brand")
        .forEach(btn => {

            btn.classList.remove("active");

        });


    document
        .querySelector(".brand")
        .classList.add("active");


    filterProducts();
}


/* =====================================================
   SORT PRODUCTS
===================================================== */

function sortProducts() {

    const grid =
        document.getElementById("productsGrid");


    const products =
        Array.from(
            grid.querySelectorAll(".product-card")
        );


    const sort =
        document.getElementById("sortSelect").value;


    if (sort === "low") {

        products.sort(
            (a, b) =>
                Number(a.dataset.price) -
                Number(b.dataset.price)
        );

    }


    else if (sort === "high") {

        products.sort(
            (a, b) =>
                Number(b.dataset.price) -
                Number(a.dataset.price)
        );

    }


    else if (sort === "rating") {

        products.sort(
            (a, b) =>
                Number(b.dataset.rating) -
                Number(a.dataset.rating)
        );

    }


    products.forEach(product => {

        grid.appendChild(product);

    });


    filterProducts();
}


/* =====================================================
   WISHLIST HEART
===================================================== */

function toggleHeart(button) {

    button.classList.toggle("liked");


    button.textContent =
        button.classList.contains("liked")
            ? "♥"
            : "♡";
}


/* =====================================================
   WISHLIST
===================================================== */

function toggleWishlist() {

    alert(
        "Wishlist is coming soon ❤️"
    );
}


/* =====================================================
   COMPARE
===================================================== */

function showCompare() {

    alert(
        "Product comparison is coming soon ⚖️"
    );
}


/* =====================================================
   HERO SCROLL
===================================================== */

function scrollToProducts() {

    document
        .getElementById("products")
        .scrollIntoView({
            behavior: "smooth"
        });
}


/* =====================================================
   VIEW ALL BRANDS
===================================================== */

function showAllBrands(event) {

    event.preventDefault();

    resetFilters();
}


/* =====================================================
   NEWSLETTER
===================================================== */

function subscribeNewsletter(event) {

    event.preventDefault();


    const email =
        event.target
            .querySelector("input")
            .value;


    alert(
        "Thanks! " +
        email +
        " has been subscribed to NaijaCart updates 🎉"
    );


    event.target.reset();
}


/* =====================================================
   INITIALIZE
===================================================== */

updateCartCount();