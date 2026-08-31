/* =====================================================
   CART
===================================================== */

let cartCount = 0;

const cartButton =
    document.getElementById("cartButton");

const cartCountElement =
    document.getElementById("cartCount");


if (cartButton) {

    cartButton.addEventListener(
        "click",
        function () {

            if (cartCount === 0) {

                alert("Your cart is empty.");

            } else {

                alert(
                    `You have ${cartCount} item(s) in your cart.`
                );

            }

        }
    );

}


/* =====================================================
   SEARCH
===================================================== */

const searchInput =
    document.getElementById("searchInput");

const searchButton =
    document.getElementById("searchButton");


function performSearch() {

    const search =
        searchInput.value.trim();

    if (!search) {

        searchInput.focus();

        return;

    }

    /*
       Send the user back to the homepage
       with the search term.
    */

    window.location.href =
        `index.html?search=${encodeURIComponent(search)}`;

}


if (searchButton) {

    searchButton.addEventListener(
        "click",
        performSearch
    );

}


if (searchInput) {

    searchInput.addEventListener(
        "keydown",
        function (event) {

            if (event.key === "Enter") {

                performSearch();

            }

        }
    );

}


/* =====================================================
   STAT COUNTERS
===================================================== */

const counters =
    document.querySelectorAll(".counter");


const observer =
    new IntersectionObserver(
        function (entries, observer) {

            entries.forEach(entry => {

                if (!entry.isIntersecting) {
                    return;
                }

                const counter =
                    entry.target;

                const target =
                    Number(
                        counter.dataset.target
                    );

                let current = 0;

                const duration = 1400;

                const increment =
                    target / (duration / 16);


                function updateCounter() {

                    current += increment;

                    if (current < target) {

                        counter.textContent =
                            Math.floor(current).toLocaleString() + "+";

                        requestAnimationFrame(
                            updateCounter
                        );

                    } else {

                        counter.textContent =
                            target.toLocaleString() + "+";

                    }

                }


                updateCounter();

                observer.unobserve(counter);

            });

        },
        {
            threshold: 0.5
        }
    );


counters.forEach(counter => {

    observer.observe(counter);

});


/* =====================================================
   NEWSLETTER
===================================================== */

const newsletterButton =
    document.getElementById(
        "newsletterButton"
    );

const newsletterEmail =
    document.getElementById(
        "newsletterEmail"
    );

const newsletterMessage =
    document.getElementById(
        "newsletterMessage"
    );


if (newsletterButton) {

    newsletterButton.addEventListener(
        "click",
        function () {

            const email =
                newsletterEmail.value.trim();


            if (!email) {

                newsletterMessage.textContent =
                    "Please enter your email.";

                newsletterEmail.focus();

                return;

            }


            if (
                !email.includes("@") ||
                !email.includes(".")
            ) {

                newsletterMessage.textContent =
                    "Please enter a valid email.";

                return;

            }


            newsletterMessage.textContent =
                "Thanks for subscribing!";


            newsletterEmail.value = "";

        }
    );

}


/* =====================================================
   REVEAL ANIMATION
===================================================== */

const revealElements =
    document.querySelectorAll(
        ".story-card, .why-card, .offer-card, .mission-card"
    );


const revealObserver =
    new IntersectionObserver(
        function (entries) {

            entries.forEach(entry => {

                if (entry.isIntersecting) {

                    entry.target.classList.add(
                        "show"
                    );

                }

            });

        },
        {
            threshold: 0.12
        }
    );


revealElements.forEach(element => {

    element.classList.add("reveal");

    revealObserver.observe(element);

});