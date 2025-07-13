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
function updateQuantityControl() {
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

function updateCart(data) {
  updateModalCartBody(data.cart_body);
  setCartTotalPrice(parseFloat(data.total_price).toFixed(2));
  setCartQuantity(data.cart_quantity);
  removeBooksFromModalCart();
  updateQuantityControl();
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

  // const json = await response.json();
  // if (modalSpinner) {
  //   modalSpinner.classList.toggle("acitve");
  // }
  // return json;
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
    document.querySelectorAll(".modal-remove-book");
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

  // Remove books from cart
  const removeModalFormElements =
    document.querySelectorAll(".modal-remove-book");
  if (removeModalFormElements) {
    removeModalFormElements.forEach((removeModalForm) => {
      removeBookFromCart(removeModalForm);
    });
  }

  // Remove book from Modal cart
  removeBooksFromModalCart();
  updateQuantityControl();
});
// End cart ---------------------------------------------------------------------

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
