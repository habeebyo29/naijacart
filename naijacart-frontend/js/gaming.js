/* =========================================================
   NAJIA CART GAMING PAGE
========================================================= */


/* =========================================================
   CART
========================================================= */

let cart =
    JSON.parse(
        localStorage.getItem("naijacart_cart")
    ) || [];


let wishlist =
    JSON.parse(
        localStorage.getItem("naijacart_wishlist")
    ) || [];


let currentBrand = "all";


/* =========================================================
   UPDATE CART COUNT
========================================================= */

function updateCartCount() {

    const cartCount =
        document.getElementById("cartCount");

    if (cartCount) {

        cartCount.textContent =
            cart.reduce(
                (total, item) =>
                    total + (Number(item.quantity) || 1),
                0
            );

    }

}


/* =========================================================
   ADD TO CART
========================================================= */

function addToCart(
    productName,
    price,
    image
) {

    const existingProduct =
        cart.find(
            item =>
                item.name === productName
        );


    if (existingProduct) {

        existingProduct.quantity =
            (existingProduct.quantity || 1) + 1;

    }

    else {

        cart.push({

            name: productName,

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


    alert(
        productName +
        " has been added to your cart! 🛒"
    );

}


/* =========================================================
   GO TO CART
========================================================= */

function showCart() {

    window.location.href =
        "cart.html";

}


/* =========================================================
   SEARCH
========================================================= */

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


function filterProducts() {

    const searchValue =
        searchInput
        ? searchInput.value.toLowerCase().trim()
        : "";


    const categorySelect =
        document.getElementById(
            "categorySelect"
        );


    const selectedCategory =
        categorySelect
        ? categorySelect.value
        : "all";


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


        const category =
            product.dataset.category
            ? product.dataset.category.toLowerCase()
            : "";


        const brandMatch =
            currentBrand === "all" ||
            brand === currentBrand;


        const searchMatch =
            name.includes(searchValue) ||
            brand.includes(searchValue);


        const categoryMatch =
            selectedCategory === "all" ||
            category === selectedCategory;


        if (
            brandMatch &&
            searchMatch &&
            categoryMatch
        ) {

            product.style.display = "";

            visible++;

        }

        else {

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


/* =========================================================
   BRAND FILTER
========================================================= */

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


    button.classList.add(
        "active"
    );


    filterProducts();

}


/* =========================================================
   RESET FILTERS
========================================================= */

function resetFilters() {

    currentBrand = "all";


    if (searchInput) {

        searchInput.value = "";

    }


    const categorySelect =
        document.getElementById(
            "categorySelect"
        );


    if (categorySelect) {

        categorySelect.value =
            "all";

    }


    document
        .querySelectorAll(".brand")
        .forEach(btn => {

            btn.classList.remove(
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


    filterProducts();

}


/* =========================================================
   SORT PRODUCTS
========================================================= */

function sortProducts() {

    const grid =
        document.getElementById(
            "productsGrid"
        );


    const products =
        Array.from(
            grid.querySelectorAll(
                ".product-card"
            )
        );


    const sort =
        document.getElementById(
            "sortSelect"
        ).value;


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

}


/* =========================================================
   WISHLIST HEART
========================================================= */

function toggleHeart(button) {

    button.classList.toggle(
        "liked"
    );


    button.textContent =
        button.classList.contains("liked")
            ? "♥"
            : "♡";

}


/* =========================================================
   WISHLIST
========================================================= */

function toggleWishlist() {

    alert(
        "Your wishlist is coming soon! ❤️"
    );

}


/* =========================================================
   COMPARE
========================================================= */

function showCompare() {

    alert(
        "Product comparison is coming soon! ⚖️"
    );

}


/* =========================================================
   HERO SCROLL
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
   SHOW ALL
========================================================= */

function showAllBrands(event) {

    event.preventDefault();

    resetFilters();

}


/* =========================================================
   NEWSLETTER
========================================================= */

function subscribeNewsletter(event) {

    event.preventDefault();


    const email =
        event.target
        .querySelector("input")
        .value;


    alert(
        "Thanks! " +
        email +
        " has been subscribed to NaijaCart updates. 🎉"
    );


    event.target.reset();

}


/* =========================================================
   INITIALIZE
========================================================= */

updateCartCount();

filterProducts();