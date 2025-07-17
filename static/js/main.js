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

// End ajax search --------------------------------------------------------------

// // Обробка форми відгуків
// const reviewForm = document.getElementById("reviewForm");
// const ratingInputs = document.querySelectorAll('input[name="rating"]');
// const ratingText = document.querySelector(".rating-text");

// // Оновлення тексту рейтингу
// ratingInputs.forEach((input) => {
//   input.addEventListener("change", function () {
//     const ratingTexts = {
//       1: "Жахливо",
//       2: "Погано",
//       3: "Нормально",
//       4: "Добре",
//       5: "Відмінно",
//     };
//     ratingText.textContent = ratingTexts[this.value];
//     ratingText.className = "rating-text text-warning fw-bold";
//   });
// });

// // Відправка форми
// reviewForm.addEventListener("submit", function (e) {
//   e.preventDefault();

//   const formData = new FormData(this);
//   const reviewData = {
//     name:
//       formData.get("reviewerName") ||
//       document.getElementById("reviewerName").value,
//     email:
//       formData.get("reviewerEmail") ||
//       document.getElementById("reviewerEmail").value,
//     rating: document.querySelector('input[name="rating"]:checked')?.value,
//     text: document.getElementById("reviewText").value,
//   };

//   // Перевірка мінімальної довжини відгуку
//   if (reviewData.text.length < 10) {
//     alert("Відгук повинен містити мінімум 10 символів");
//     return;
//   }

//   // Тут можна додати відправку на сервер
//   alert("Дякуємо за ваш відгук! Він буде опублікований після модерації.");

//   // Очищення форми
//   this.reset();
//   ratingText.textContent = "Оберіть оцінку";
//   ratingText.className = "rating-text text-muted";
// });
