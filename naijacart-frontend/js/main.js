/* =====================================================
   NAIJACART HOMEPAGE JAVASCRIPT
===================================================== */


/* =====================================================
   PRODUCT DATA
===================================================== */

const products = [

    {
        name: "iPhone 15 Pro Max",
        category: "Smartphones",
        price: "₦1,250,000",
        rating: "4.9",
        reviews: "124",
        discount: "-12%",
        image: "https://images.pexels.com/photos/788946/pexels-photo-788946.jpeg?auto=compress&cs=tinysrgb&w=500&q=70"
    },

    {
        name: "Samsung Galaxy S24 Ultra",
        category: "Smartphones",
        price: "₦1,180,000",
        rating: "4.8",
        reviews: "98",
        discount: "-10%",
        image: "https://images.pexels.com/photos/404280/pexels-photo-404280.jpeg?auto=compress&cs=tinysrgb&w=500&q=70"
    },

    {
        name: "Google Pixel 9 Pro",
        category: "Smartphones",
        price: "₦980,000",
        rating: "4.8",
        reviews: "76",
        discount: "-15%",
        image: "https://images.pexels.com/photos/1092644/pexels-photo-1092644.jpeg?auto=compress&cs=tinysrgb&w=500&q=70"
    },

    {
        name: "Xiaomi 14 Ultra",
        category: "Smartphones",
        price: "₦820,000",
        rating: "4.7",
        reviews: "63",
        discount: "-9%",
        image: "https://images.pexels.com/photos/1092644/pexels-photo-1092644.jpeg?auto=compress&cs=tinysrgb&w=500&q=70"
    },

    {
        name: "MacBook Air M3",
        category: "Laptops",
        price: "₦1,650,000",
        rating: "4.9",
        reviews: "86",
        discount: "-15%",
        image: "https://images.pexels.com/photos/205421/pexels-photo-205421.jpeg?auto=compress&cs=tinysrgb&w=500&q=70"
    },

    {
        name: "HP Pavilion 15",
        category: "Laptops",
        price: "₦650,000",
        rating: "4.7",
        reviews: "74",
        discount: "-10%",
        image: "https://images.pexels.com/photos/18105/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=500&q=70"
    },

    {
        name: "Dell XPS 15",
        category: "Laptops",
        price: "₦1,200,000",
        rating: "4.8",
        reviews: "61",
        discount: "-12%",
        image: "https://images.pexels.com/photos/18105/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=500&q=70"
    },

    {
        name: "PlayStation 5",
        category: "Gaming",
        price: "₦950,000",
        rating: "4.9",
        reviews: "112",
        discount: "-8%",
        image: "https://images.pexels.com/photos/3945651/pexels-photo-3945651.jpeg?auto=compress&cs=tinysrgb&w=500&q=70"
    },

    {
        name: "Xbox Wireless Controller",
        category: "Gaming",
        price: "₦85,000",
        rating: "4.8",
        reviews: "94",
        discount: "-15%",
        image: "https://images.pexels.com/photos/1298601/pexels-photo-1298601.jpeg?auto=compress&cs=tinysrgb&w=500&q=70"
    },

    {
        name: "Sony WH-1000XM5",
        category: "Audio",
        price: "₦350,000",
        rating: "4.9",
        reviews: "150",
        discount: "-18%",
        image: "https://images.pexels.com/photos/3394650/pexels-photo-3394650.jpeg?auto=compress&cs=tinysrgb&w=500&q=70"
    },

    {
        name: "AirPods Pro",
        category: "Audio",
        price: "₦280,000",
        rating: "4.8",
        reviews: "201",
        discount: "-20%",
        image: "https://images.pexels.com/photos/8534088/pexels-photo-8534088.jpeg?auto=compress&cs=tinysrgb&w=500&q=70"
    },

    {
        name: "Apple Watch Series 9",
        category: "Smartwatches",
        price: "₦420,000",
        rating: "4.8",
        reviews: "88",
        discount: "-12%",
        image: "https://images.pexels.com/photos/437037/pexels-photo-437037.jpeg?auto=compress&cs=tinysrgb&w=500&q=70"
    },

    {
        name: "Anker PowerBank 20,000mAh",
        category: "Accessories",
        price: "₦45,000",
        rating: "4.7",
        reviews: "61",
        discount: "-25%",
        image: "https://images.pexels.com/photos/4526463/pexels-photo-4526463.jpeg?auto=compress&cs=tinysrgb&w=500&q=70"
    }

];


/* =====================================================
   ELEMENTS
===================================================== */

const productsContainer =
    document.getElementById("productsContainer");

const productTitle =
    document.getElementById("productTitle");

const productLabel =
    document.getElementById("productLabel");

const searchInput =
    document.getElementById("searchInput");

const searchButton =
    document.getElementById("searchButton");

const cartCountElement =
    document.getElementById("cartCount");

const toast =
    document.getElementById("toast");

const toastMessage =
    document.getElementById("toastMessage");


/* =====================================================
   CART
===================================================== */

let cartCount =
    Number(localStorage.getItem("naijaCartCount")) || 0;


function updateCartDisplay() {

    cartCountElement.textContent =
        cartCount;

}


function saveCart() {

    localStorage.setItem(
        "naijaCartCount",
        cartCount
    );

}


function showToast(message) {

    toastMessage.textContent =
        message;

    toast.classList.add("show");

    clearTimeout(
        window.toastTimer
    );

    window.toastTimer =
        setTimeout(() => {

            toast.classList.remove("show");

        }, 2500);

}


function addToCart(productName, button = null) {

    cartCount++;

    updateCartDisplay();

    saveCart();

    showToast(
        `${productName} added to cart`
    );


    if (button) {

        const originalHTML =
            button.innerHTML;

        button.innerHTML =
            `<i class="fa-solid fa-check"></i> Added`;

        button.classList.add("added");

        button.disabled = true;

        setTimeout(() => {

            button.innerHTML =
                originalHTML;

            button.classList.remove(
                "added"
            );

            button.disabled = false;

        }, 1000);

    }

}


updateCartDisplay();


/* =====================================================
   PRODUCT CARD
===================================================== */

function createProductCard(product) {

    const card =
        document.createElement("article");

    card.className =
        "product-card";


    card.innerHTML = `

        <div class="product-image">

            <span class="discount">
                ${product.discount}
            </span>

            <img
                src="${product.image}"
                alt="${product.name}"
                loading="lazy"
            >

        </div>


        <div class="product-info">

            <span class="product-category">
                ${product.category}
            </span>

            <h3>
                ${product.name}
            </h3>

            <div class="rating">

                ★★★★★

                <span>
                    ${product.rating}
                    (${product.reviews})
                </span>

            </div>

            <div class="price">
                ${product.price}
            </div>

            <button
                class="add-cart"
                type="button"
            >

                <i class="fa-solid fa-cart-shopping"></i>

                Add to Cart

            </button>

        </div>

    `;


    const addButton =
        card.querySelector(".add-cart");


    addButton.addEventListener(
        "click",
        () => {

            addToCart(
                product.name,
                addButton
            );

        }
    );


    return card;

}


/* =====================================================
   DISPLAY PRODUCTS
===================================================== */

function displayProducts(
    category = "all",
    shouldScroll = false
) {

    productsContainer.innerHTML = "";


    let filteredProducts;


    if (category === "all") {

        filteredProducts =
            products;

        productTitle.textContent =
            "Best Selling Products";

        productLabel.textContent =
            "TRENDING NOW";

    } else {

        filteredProducts =
            products.filter(
                product =>
                    product.category === category
            );

        productTitle.textContent =
            category;

        productLabel.textContent =
            "SHOP CATEGORY";

    }


    if (filteredProducts.length === 0) {

        showEmptyProducts();

        return;

    }


    filteredProducts.forEach(product => {

        productsContainer.appendChild(
            createProductCard(product)
        );

    });


    if (shouldScroll) {

        document
            .getElementById("products")
            .scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

    }

}


/* =====================================================
   EMPTY PRODUCTS
===================================================== */

function showEmptyProducts() {

    productsContainer.innerHTML = `

        <div class="empty-products">

            <i class="fa-solid fa-box-open"></i>

            <h3>
                No products found
            </h3>

            <p>
                Try another category or search term.
            </p>

        </div>

    `;

}


/* =====================================================
   INITIAL PRODUCTS
===================================================== */

displayProducts();


/* =====================================================
   CATEGORY BUTTONS
===================================================== */

document
    .querySelectorAll(
        ".hero-btn"
    )
    .forEach(button => {

        button.addEventListener(
            "click",
            () => {

                const category =
                    button.dataset.category;

                displayProducts(
                    category,
                    true
                );

            }
        );

    });


/* =====================================================
   CATEGORY CARDS
===================================================== */

document
    .querySelectorAll(
        ".category-card"
    )
    .forEach(card => {

        card.addEventListener(
            "click",
            function(event) {

                /*
                 * If the category already has
                 * an actual page link, let the
                 * browser follow the link.
                 */

                if (
                    this.getAttribute("href")
                ) {
                    return;
                }

                event.preventDefault();

                const category =
                    this.dataset.category;

                if (category) {

                    displayProducts(
                        category,
                        true
                    );

                }

            }
        );

    });


/* =====================================================
   SHOW ALL PRODUCTS
===================================================== */

document
    .getElementById("showAll")
    .addEventListener(
        "click",
        () => {

            displayProducts(
                "all",
                true
            );

        }
    );


/* =====================================================
   SEARCH
===================================================== */

function searchProducts() {

    const search =
        searchInput.value
            .toLowerCase()
            .trim();


    if (!search) {

        displayProducts(
            "all",
            false
        );

        return;

    }


    const results =
        products.filter(product => {

            const name =
                product.name
                    .toLowerCase();

            const category =
                product.category
                    .toLowerCase();

            return (
                name.includes(search) ||
                category.includes(search)
            );

        });


    productsContainer.innerHTML = "";


    productTitle.textContent =
        "Search Results";

    productLabel.textContent =
        `${results.length} PRODUCTS FOUND`;


    if (results.length === 0) {

        showEmptyProducts();

    } else {

        results.forEach(product => {

            productsContainer.appendChild(
                createProductCard(product)
            );

        });

    }


    document
        .getElementById("products")
        .scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

}


searchButton.addEventListener(
    "click",
    searchProducts
);


searchInput.addEventListener(
    "keydown",
    event => {

        if (event.key === "Enter") {

            searchProducts();

        }

    }
);


/* =====================================================
   CART BUTTON
===================================================== */

document
    .getElementById("cartButton")
    .addEventListener(
        "click",
        () => {

            if (cartCount === 0) {

                showToast(
                    "Your cart is empty"
                );

            } else {

                showToast(
                    `Your cart has ${cartCount} item${cartCount === 1 ? "" : "s"}`
                );

            }

        }
    );


/* =====================================================
   HERO SLIDER
===================================================== */

const slides =
    document.querySelectorAll(
        ".hero-slide"
    );

const dots =
    document.querySelectorAll(
        ".dot"
    );

let currentSlide = 0;

let sliderTimer;


function showSlide(index) {

    slides.forEach(
        slide =>
            slide.classList.remove(
                "active"
            )
    );

    dots.forEach(
        dot =>
            dot.classList.remove(
                "active"
            )
    );


    slides[index]
        .classList
        .add("active");

    dots[index]
        .classList
        .add("active");


    currentSlide =
        index;

}


function nextSlide() {

    currentSlide =
        (currentSlide + 1)
        % slides.length;

    showSlide(currentSlide);

}


function previousSlide() {

    currentSlide--;

    if (
        currentSlide < 0
    ) {

        currentSlide =
            slides.length - 1;

    }

    showSlide(currentSlide);

}


/* =====================================================
   RESET SLIDER TIMER
===================================================== */

function resetSliderTimer() {

    clearInterval(
        sliderTimer
    );

    sliderTimer =
        setInterval(
            nextSlide,
            5000
        );

}


/* =====================================================
   HERO CONTROLS
===================================================== */

document
    .getElementById("nextSlide")
    .addEventListener(
        "click",
        () => {

            nextSlide();

            resetSliderTimer();

        }
    );


document
    .getElementById("previousSlide")
    .addEventListener(
        "click",
        () => {

            previousSlide();

            resetSliderTimer();

        }
    );


dots.forEach(
    (dot, index) => {

        dot.addEventListener(
            "click",
            () => {

                showSlide(index);

                resetSliderTimer();

            }
        );

    }
);


resetSliderTimer();


/* =====================================================
   DEAL BUTTON
===================================================== */

const dealButton =
    document.getElementById(
        "dealButton"
    );


if (dealButton) {

    dealButton.addEventListener(
        "click",
        () => {

            displayProducts(
                "all",
                true
            );

        }
    );

}


/* =====================================================
   NEWSLETTER
===================================================== */

const newsletterForm =
    document.getElementById(
        "newsletterForm"
    );


if (newsletterForm) {

    newsletterForm.addEventListener(
        "submit",
        event => {

            event.preventDefault();

            const email =
                document
                    .getElementById(
                        "newsletterEmail"
                    )
                    .value
                    .trim();


            if (!email) {

                showToast(
                    "Please enter your email"
                );

                return;

            }


            showToast(
                "Thanks for subscribing!"
            );


            newsletterForm.reset();

        }
    );

}


/* =====================================================
   PAUSE SLIDER WHEN TAB IS NOT ACTIVE
===================================================== */

document.addEventListener(
    "visibilitychange",
    () => {

        if (
            document.hidden
        ) {

            clearInterval(
                sliderTimer
            );

        } else {

            resetSliderTimer();

        }

    }
);