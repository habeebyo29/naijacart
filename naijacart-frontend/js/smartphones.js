/* =====================================================
   NAIJACART — SMARTPHONES PAGE
===================================================== */


/* =====================================================
   CART
===================================================== */

const CART_KEY = "naijacart_cart";


function getCart() {

    return JSON.parse(
        localStorage.getItem(CART_KEY)
    ) || [];

}


function saveCart(cart) {

    localStorage.setItem(
        CART_KEY,
        JSON.stringify(cart)
    );

}


/* =====================================================
   CART COUNT
===================================================== */

function updateCartCount() {

    const cart = getCart();

    const cartCount =
        document.getElementById("cartCount");

    if (!cartCount) {
        return;
    }

    let total = 0;

    cart.forEach(item => {

        total +=
            Number(item.quantity) || 1;

    });

    cartCount.textContent = total;

}


/* =====================================================
   ADD TO CART
   NO PRODUCT ID
===================================================== */

function addToCart(
    productName,
    price,
    image
) {

    const cart = getCart();

    const existingProduct =
        cart.find(
            item =>
                item.name === productName
        );


    if (existingProduct) {

        existingProduct.quantity =
            (Number(
                existingProduct.quantity
            ) || 1) + 1;

    } else {

        cart.push({

            name: productName,

            price: Number(
                String(price)
                    .replace(/[₦,]/g, "")
            ),

            image: image,

            quantity: 1

        });

    }


    saveCart(cart);

    updateCartCount();

    showCartMessage(productName);

}


/* =====================================================
   CART MESSAGE
===================================================== */

function showCartMessage(productName) {

    const oldMessage =
        document.querySelector(
            ".cart-toast"
        );

    if (oldMessage) {
        oldMessage.remove();
    }


    const toast =
        document.createElement("div");

    toast.className =
        "cart-toast";


    toast.innerHTML = `
        <span>✓</span>

        <div>
            <strong>
                Added to cart
            </strong>

            <small>
                ${productName}
            </small>
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
            zIndex: "9999",
            display: "flex",
            alignItems: "center",
            gap: "12px",
            padding: "14px 16px",
            background: "#ffffff",
            border: "1px solid #e5e7eb",
            borderRadius: "12px",
            boxShadow:
                "0 12px 35px rgba(0,0,0,.15)",
            color: "#17221d"
        }
    );


    toast.querySelector("span").style.cssText = `
        width:32px;
        height:32px;
        border-radius:50%;
        background:#eaf7f1;
        color:#075c3f;
        display:grid;
        place-items:center;
        font-weight:900;
    `;


    toast.querySelector("small").style.cssText = `
        display:block;
        color:#6b7280;
        margin-top:2px;
        font-size:11px;
    `;


    toast.querySelector("a").style.cssText = `
        color:#075c3f;
        font-size:12px;
        font-weight:800;
        margin-left:5px;
        text-decoration:none;
    `;


    document.body.appendChild(toast);


    setTimeout(() => {

        toast.style.opacity = "0";

        toast.style.transform =
            "translateY(10px)";

        toast.style.transition =
            ".3s";


        setTimeout(() => {

            toast.remove();

        }, 300);

    }, 3000);

}


/* =====================================================
   SEARCH
===================================================== */

document.addEventListener(
    "DOMContentLoaded",
    function() {

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


function filterProducts() {

    const searchInput =
        document.getElementById(
            "searchInput"
        );

    const categorySelect =
        document.getElementById(
            "categorySelect"
        );


    const searchValue =
        searchInput
            ? searchInput.value
                .toLowerCase()
                .trim()
            : "";


    const category =
        categorySelect
            ? categorySelect.value
            : "all";


    const products =
        document.querySelectorAll(
            ".product-card"
        );


    let visible = 0;


    products.forEach(product => {

        const name =
            (
                product.dataset.name || ""
            ).toLowerCase();


        const brand =
            (
                product.dataset.brand || ""
            ).toLowerCase();


        const price =
            Number(
                product.dataset.price || 0
            );


        const searchMatch =
            name.includes(searchValue) ||
            brand.includes(searchValue);


        let categoryMatch = true;


        if (category === "flagship") {

            categoryMatch =
                price >= 700000;

        }


        if (category === "gaming") {

            categoryMatch =
                name.includes("gt") ||
                name.includes("phantom");

        }


        if (
            searchMatch &&
            categoryMatch
        ) {

            product.style.display = "";

            visible++;

        } else {

            product.style.display = "none";

        }

    });


    const noProducts =
        document.getElementById(
            "noProducts"
        );


    if (noProducts) {

        noProducts.style.display =
            visible === 0
                ? "block"
                : "none";

    }

}


/* =====================================================
   BRAND FILTER
===================================================== */

let currentBrand = "all";


function filterBrand(
    brand,
    button
) {

    currentBrand = brand;


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


    applyBrandFilter();

}


function applyBrandFilter() {

    const products =
        document.querySelectorAll(
            ".product-card"
        );


    const searchInput =
        document.getElementById(
            "searchInput"
        );


    const search =
        searchInput
            ? searchInput.value
                .toLowerCase()
                .trim()
            : "";


    let visible = 0;


    products.forEach(product => {

        const brand =
            (
                product.dataset.brand || ""
            ).toLowerCase();


        const name =
            (
                product.dataset.name || ""
            ).toLowerCase();


        const brandMatch =
            currentBrand === "all" ||
            brand === currentBrand;


        const searchMatch =
            !search ||
            name.includes(search) ||
            brand.includes(search);


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


    const noProducts =
        document.getElementById(
            "noProducts"
        );


    if (noProducts) {

        noProducts.style.display =
            visible === 0
                ? "block"
                : "none";

    }

}


/* =====================================================
   RESET FILTERS
===================================================== */

function resetFilters() {

    currentBrand = "all";


    const searchInput =
        document.getElementById(
            "searchInput"
        );

    if (searchInput) {
        searchInput.value = "";
    }


    const categorySelect =
        document.getElementById(
            "categorySelect"
        );

    if (categorySelect) {
        categorySelect.value = "all";
    }


    document
        .querySelectorAll(".brand")
        .forEach(button => {

            button.classList.remove(
                "active"
            );

        });


    const firstBrand =
        document.querySelector(
            ".brand"
        );


    if (firstBrand) {

        firstBrand.classList.add(
            "active"
        );

    }


    document
        .querySelectorAll(".product-card")
        .forEach(product => {

            product.style.display = "";

        });


    const noProducts =
        document.getElementById(
            "noProducts"
        );


    if (noProducts) {

        noProducts.style.display =
            "none";

    }

}


/* =====================================================
   SORT PRODUCTS
===================================================== */

function sortProducts() {

    const grid =
        document.getElementById(
            "productsGrid"
        );


    if (!grid) {
        return;
    }


    const products =
        Array.from(
            grid.querySelectorAll(
                ".product-card"
            )
        );


    const sortSelect =
        document.getElementById(
            "sortSelect"
        );


    if (!sortSelect) {
        return;
    }


    const sort =
        sortSelect.value;


    if (sort === "low") {

        products.sort(
            (a, b) =>
                Number(
                    a.dataset.price || 0
                ) -
                Number(
                    b.dataset.price || 0
                )
        );

    }


    else if (sort === "high") {

        products.sort(
            (a, b) =>
                Number(
                    b.dataset.price || 0
                ) -
                Number(
                    a.dataset.price || 0
                )
        );

    }


    else if (sort === "rating") {

        products.sort(
            (a, b) =>
                Number(
                    b.dataset.rating || 0
                ) -
                Number(
                    a.dataset.rating || 0
                )
        );

    }


    products.forEach(product => {

        grid.appendChild(product);

    });

}


/* =====================================================
   WISHLIST HEART
===================================================== */

function toggleHeart(button) {

    button.classList.toggle(
        "liked"
    );


    button.textContent =
        button.classList.contains("liked")
            ? "♥"
            : "♡";

}


/* =====================================================
   WISHLIST BUTTON
===================================================== */

function toggleWishlist() {

    alert(
        "Your wishlist will be available soon. ❤️"
    );

}


/* =====================================================
   COMPARE
===================================================== */

function showCompare() {

    alert(
        "Product comparison will be available soon. ⚖️"
    );

}


/* =====================================================
   HERO
===================================================== */

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


/* =====================================================
   SHOW ALL BRANDS
===================================================== */

function showAllBrands(event) {

    if (event) {

        event.preventDefault();

    }

    resetFilters();

}


/* =====================================================
   NEWSLETTER
===================================================== */

function subscribeNewsletter(event) {

    event.preventDefault();


    const input =
        event.target.querySelector(
            "input"
        );


    const email =
        input
            ? input.value
            : "";


    alert(
        "Thanks! " +
        email +
        " has been subscribed to NaijaCart updates. 🎉"
    );


    event.target.reset();

}


/* =====================================================
   INITIALIZE
===================================================== */

document.addEventListener(
    "DOMContentLoaded",
    function() {

        updateCartCount();

    }
);


/* =====================================================
   UPDATE CART WHEN ANOTHER TAB CHANGES IT
===================================================== */

window.addEventListener(
    "storage",
    function(event) {

        if (event.key === CART_KEY) {

            updateCartCount();

        }

    }
);