//  Category menu toogle

function categoryMenuToogle() {
  const menuButton = document.querySelector(".category-menu .btn");
  const categorryMenuNav = document.querySelector(
    ".category-menu .category-menu__nav"
  );
  const activeClass = "open";
  const btnActiveClass = "active";

  menuButton.addEventListener("click", () => {
    categorryMenuNav.classList.toggle(activeClass);
    menuButton.classList.toggle(btnActiveClass);
  });
}
categoryMenuToogle();

//  Category menu items toogle mobile
function categoryMenuItemsToogleMobile() {
  const btnElements = document.querySelectorAll(
    ".category-menu__nav .list-group .list-group-item:has(ul) > .plus"
  );

  btnElements.forEach((btnElement) => {
    btnElement.addEventListener("click", function (event) {
      event.stopPropagation();
      const itemElement = this.closest("li");
      const listElement = itemElement.querySelector("ul");
      listElement.classList.toggle("open");
    });
  });
}
categoryMenuItemsToogleMobile();

// Cart -------------------------------------------------------------------
// Quantity controls
function updateDetailQuantityControl() {
  const cartInputGroups = document.querySelectorAll(".cart-input-group");
  if (cartInputGroups) {
    cartInputGroups.forEach((item) => {
      const minusBtn = item.querySelector(".btn-minus");
      const plusBtn = item.querySelector(".btn-plus");
      const quantityInput = item.querySelector(
        '.input-group input[type="text"]'
      );
      minusBtn.addEventListener("click", function () {
        const currentValue = parseInt(quantityInput.value);
        if (currentValue > 1) {
          quantityInput.value = currentValue - 1;
        }
      });

      plusBtn.addEventListener("click", function () {
        const currentValue = parseInt(quantityInput.value);
        quantityInput.value = currentValue + 1;
      });
    });
  }
}

function updateModalCartQuantityControl() {
  const cartInputGroups = document.querySelectorAll(".modal-cart-input-group");
  if (cartInputGroups) {
    cartInputGroups.forEach((item) => {
      const minusBtn = item.querySelector(".btn-minus");
      const plusBtn = item.querySelector(".btn-plus");
      const quantityInput = item.querySelector(
        '.input-group input[type="text"]'
      );
      const form = item.closest("form");

      function send() {
        if (quantityInput.value != "" && quantityInput.value != "0") {
          formSend(form).then((json) => {
            updateCart(json);
          });
        }
        if (quantityInput.value == "0") {
          form.setAttribute("action", form.dataset.removeUrl);
          formSend(form).then((json) => {
            updateCart(json);
          });
        }
      }

      quantityInput.addEventListener("input", () => {
        send();
      });

      minusBtn.addEventListener("click", function () {
        const currentValue = parseInt(quantityInput.value);
        if (currentValue > 1) {
          quantityInput.value = currentValue - 1;
          send();
        }
      });

      plusBtn.addEventListener("click", function () {
        const currentValue = parseInt(quantityInput.value);
        quantityInput.value = currentValue + 1;
        send();
      });
    });
  }
}

// Add book to cart
function setCartQuantity(quantity) {
  const cartLabel = document.querySelector(".total-card");
  if (cartLabel) {
    cartLabel.querySelector(".products").innerHTML = `Товарів ${quantity}`;
  }
}
function setCartTotalPrice(price) {
  const cartLabel = document.querySelector(".total-card");
  if (cartLabel) {
    cartLabel.querySelector(".prices").innerHTML = `${price} грн`;
  }
}

function updateModalCartBody(body) {
  const modalCartBody = document.querySelector("#modal-cart-body");
  if (modalCartBody) {
    modalCartBody.innerHTML = body;
  }
}

function updateOrderInfo(body) {
  const orderInfoBody = document.querySelector(".order-info__body");
  if (orderInfoBody) {
    orderInfoBody.innerHTML = body;
    orderInfoBody.querySelector("table")?.classList.add("table-bordered");
  }
}

function updateModalOrderBtnStatus(status) {
  const btn = document.querySelector("#modal-order-btn");
  if (btn) {
    if (status) {
      btn.classList.add("disabled");
    } else {
      btn.classList.remove("disabled");
    }
  }
}

function updateCart(data) {
  updateModalCartBody(data.cart_body);
  updateOrderInfo(data.cart_body);
  setCartTotalPrice(parseFloat(data.total_price).toFixed(2));
  setCartQuantity(data.cart_quantity);
  removeBooksFromModalCart();
  updateModalCartQuantityControl();
  updateModalOrderBtnStatus(data.is_empty);
}

async function formSend(form) {
  const formData = new FormData(form);
  const url = form.action;
  const modalSpinner = document.querySelector(".modal-body .spinner");

  if (modalSpinner) {
    modalSpinner.classList.toggle("active");
  }

  return await fetch(url, {
    method: form.method,
    body: formData,
  }).then((response) => {
    if (modalSpinner) {
      modalSpinner.classList.toggle("active");
    }
    return response.json();
  });
}

function removeBookFromCart(form) {
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      formSend(form).then((json) => {
        updateCart(json);
      });
    });
  }
}

function removeBooksFromModalCart() {
  const removeModalFormElements =
    document.querySelectorAll(".cart-remove-book");
  if (removeModalFormElements) {
    removeModalFormElements.forEach((removeModalForm) => {
      removeBookFromCart(removeModalForm);
    });
  }
}

function addBookToCart(form) {
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      formSend(form).then((json) => {
        updateCart(json);
      });
    });
  }
}

document.addEventListener("DOMContentLoaded", function () {
  // Add to cart one book from card (from catalog)
  const bookCards = document.querySelectorAll(".card");
  if (bookCards) {
    bookCards.forEach((card) => {
      const form = card.querySelector("form");
      addBookToCart(form);
    });
  }

  // Add Book to cart from detail page
  const detaillAddToCartForm = document.querySelector("#detail-add-to-cart");
  if (detaillAddToCartForm) {
    console.log(detaillAddToCartForm);
    addBookToCart(detaillAddToCartForm);
  }

  // Remove books from cart
  const removeModalFormElements =
    document.querySelectorAll(".cart-remove-book");
  if (removeModalFormElements) {
    removeModalFormElements.forEach((removeModalForm) => {
      removeBookFromCart(removeModalForm);
    });
  }

  // Remove book from Modal cart
  removeBooksFromModalCart();
  updateModalCartQuantityControl();
  updateDetailQuantityControl();
});
// End cart ---------------------------------------------------------------------

// Start ajax search ------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  async function sendForm(form) {
    const formData = new FormData(form);
    const params = new URLSearchParams();

    for (const pair of formData.entries()) {
      params.append(pair[0], pair[1]);
    }
    const url = `${form.dataset.ajaxUrl}?${params.toString()}`;

    const response = await fetch(url);
    const data = await response.json();
    return data;
  }
  function renderAjaxSearchList(body) {
    const ajaxListHandler = document.querySelector("#autosearch-handler");
    ajaxListHandler.innerHTML = body;
  }
  function ajaxSearchFormHandler() {
    const searchInput = document.querySelector(
      '#search-form input[type="text"]'
    );
    searchInput.addEventListener("input", (e) => {
      if (searchInput.value.length >= 3) {
        console.log(searchInput.value);
        const searchFormElement = searchInput.closest("#search-form");
        sendForm(searchFormElement).then((data) => {
          renderAjaxSearchList(data.body);
        });
      } else {
        renderAjaxSearchList("");
      }
    });
  }
  ajaxSearchFormHandler();
});

// Catalog filters start --------------------------------------------------------
// Функція для оновлення діапазону цін (десктоп)
function updatePriceRange() {
  const minPriceSlider = document.getElementById("minPrice");
  const maxPriceSlider = document.getElementById("maxPrice");
  const minPriceValue = document.getElementById("minPriceValue");
  const maxPriceValue = document.getElementById("maxPriceValue");
  const priceTrack = document.getElementById("priceTrack");

  if (!minPriceSlider) return;

  const minVal = parseInt(minPriceSlider.value);
  const maxVal = parseInt(maxPriceSlider.value);

  if (minVal >= maxVal) {
    if (this === minPriceSlider) {
      minPriceSlider.value = maxVal - 10;
    } else {
      maxPriceSlider.value = minVal + 10;
    }
  }

  const minPercent =
    ((minPriceSlider.value - minPriceSlider.min) /
      (minPriceSlider.max - minPriceSlider.min)) *
    100;
  const maxPercent =
    ((maxPriceSlider.value - maxPriceSlider.min) /
      (maxPriceSlider.max - maxPriceSlider.min)) *
    100;

  priceTrack.style.left = minPercent + "%";
  priceTrack.style.right = 100 - maxPercent + "%";

  minPriceValue.textContent = minPriceSlider.value;
  maxPriceValue.textContent = maxPriceSlider.value;
}

function toogleMobileFilters() {
  const mobileFilterBtn = document.querySelector(".mobile-filter-btn");
  const filtersSidebar = document.querySelector(".filters-sidebar");
  if (mobileFilterBtn && filtersSidebar) {
    mobileFilterBtn.addEventListener("click", () => {
      mobileFilterBtn.classList.toggle("hide");
      filtersSidebar.classList.toggle("active");
    });
  }
  const closeMobileFilters = document.querySelector(
    ".filters-sidebar .btn-close"
  );
  if (closeMobileFilters) {
    closeMobileFilters.addEventListener("click", () => {
      mobileFilterBtn.classList.toggle("hide");
      filtersSidebar.classList.toggle("active");
    });
  }
}

// Ініціалізація після завантаження DOM
document.addEventListener("DOMContentLoaded", function () {
  // Десктопні слайдери
  const minPriceSlider = document.getElementById("minPrice");
  const maxPriceSlider = document.getElementById("maxPrice");

  if (minPriceSlider && maxPriceSlider) {
    minPriceSlider.addEventListener("input", updatePriceRange);
    maxPriceSlider.addEventListener("input", updatePriceRange);
    updatePriceRange();
  }

  toogleMobileFilters();
  // Кнопки очищення
  document
    .querySelector(".clear-filters")
    ?.addEventListener("click", function () {
      document
        .querySelectorAll('.catalog-filters input[type="checkbox"]')
        .forEach((checkbox) => {
          checkbox.checked = false;
        });

      if (minPriceSlider && maxPriceSlider) {
        minPriceSlider.value = 0;
        maxPriceSlider.value = 2000;
        updatePriceRange();
      }
    });

  // Закрити offcanvas після застосування
  const offcanvas = bootstrap.Offcanvas.getInstance(
    document.getElementById("mobileFilters")
  );
  if (offcanvas) {
    offcanvas.hide();
  }
});

// Catalog filters end ----------------------------------------------------------

// End ajax search --------------------------------------------------------------

// show ratings
let ratings = document.querySelectorAll(".star-rating");

if (ratings.length > 0) {
  initRatings();
}

function initRatings() {
  ratings = document.querySelectorAll(".star-rating");
  console.log(ratings);
  let ratingActive, ratingBody;
  ratings.forEach((rating) => {
    initRating(rating);
  });

  function initRating(rating) {
    initRatingVars(rating);
    setRatingActiveWidth();

    if (rating.classList.contains("rating-set")) {
      setRating(rating);
    }
  }

  function initRatingVars(rating) {
    ratingActive = rating.querySelector(".star-rating__active");
    ratingBody = rating.querySelector(".star-rating__body");
  }

  function setRatingActiveWidth(index = ratingBody.dataset.ratingValue) {
    const ratingActiveWidth = index / 0.05;
    ratingActive.style.width = `${ratingActiveWidth}%`;
  }

  function clearRatingChacked(rating) {
    const items = rating.querySelectorAll(".star-rating__item");
    items.forEach((item) => {
      item.removeAttribute("checked");
    });
  }
  function setRatingChacked(rating, value) {
    const items = rating.querySelectorAll(".star-rating__item");
    items.forEach((item, index) => {
      if (index == value - 1) {
        item.setAttribute("checked", true);
      }
    });
  }
  // end show ratings

  function setRating(rating) {
    const ratingItems = rating.querySelectorAll(".star-rating__item");
    clearRatingChacked(rating);
    setRatingChacked(rating, ratingBody.dataset.ratingValue);
    ratingItems.forEach((ratingItem, index) => {
      ratingItem.addEventListener("mouseenter", function (e) {
        initRatingVars(rating);
        setRatingActiveWidth(ratingItem.value);
      });
      ratingItem.addEventListener("mouseleave", function (e) {
        setRatingActiveWidth();
      });
      ratingItem.addEventListener("click", function (e) {
        initRatingVars(rating);
        ratingBody.dataset.ratingValue = index + 1;
        setRatingActiveWidth();
        clearRatingChacked(rating);
        setRatingChacked(rating, index + 1);
      });
    });
  }
}

// Обробка форми відгуків

const reviewForm = document.querySelector(".review-form");
if (reviewForm) {
  reviewFormSubmitBtn = reviewForm.querySelector('button[type="submit"]');
  reviewFormSubmitBtn.addEventListener("click", function (e) {
    e.preventDefault();
    const reviewFormData = new FormData(reviewForm);
    fetch(reviewForm.action, {
      method: "POST",
      body: reviewFormData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        reviewForm.querySelector("textarea").value = "";
        reviewForm.querySelector(".star-rating__body").dataset.ratingValue = 1;
        initRatings();
        getReviews();
        scrollToComment();
        document.querySelector(
          "#comment-btn"
        ).innerHTML = `Відгуки (${data.count})`;
      })
      .catch((error) => console.log(error));
  });
}

function scrollToComment() {
  const reviewHolder = document.querySelector(".reviews-holder");
  reviewHolder.scrollIntoView({
    behavior: "smooth",
    block: "start",
  });
}

// Get rewiews

function getReviews(params = null) {
  console.log("review");
  const reviewsHolder = document.querySelector(".reviews-holder");
  if (reviewsHolder) {
    let url = reviewsHolder.dataset.urlReview;
    if (params) {
      url = `${url}${params}`;
    }
    fetch(url)
      .then((response) => response.text())
      .then((html) => {
        reviewsHolder.innerHTML = html;
        initRatings();
        paginateReview();
      })
      .catch((error) => console.log(error));
  }
}

getReviews();

// Get reviews by paginate

function paginateReview() {
  const paginationLinks = document.querySelectorAll(
    ".comment-pagination a.page-link"
  );
  if (paginationLinks) {
    paginationLinks.forEach((link) => {
      link.addEventListener("click", function (e) {
        e.preventDefault();
        const params = this.getAttribute("href");
        getReviews(params);
        scrollToComment();
      });
    });
  }
}
