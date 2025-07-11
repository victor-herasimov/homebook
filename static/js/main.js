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

// Quantity controls
document.addEventListener("DOMContentLoaded", function () {
  const cartInputGroups = document.querySelectorAll(".cart-input-group");
  if (cartInputGroups) {
    cartInputGroups.forEach((item) => {
      const minusBtn = item.querySelector(".btn-minus");
      const plusBtn = item.querySelector(".btn-plus");
      const quantityInput = item.querySelector(
        '.input-group input[type="number"]'
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
});

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
  removeBooksFromCart();
}

function removeBooksFromCart() {
  // Remove book from modal cart
  const removeModalFormElements =
    document.querySelectorAll(".modal-remove-book");
  if (removeModalFormElements) {
    removeModalFormElements.forEach((removeModalForm) => {
      removeModalForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const formData = new FormData(removeModalForm);
        const url = removeModalForm.action;
        fetch(url, { method: removeModalForm.method, body: formData })
          .then((response) => {
            return response.json();
          })
          .then((json) => {
            updateCart(json);
          });
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
      if (form) {
        form.addEventListener("submit", (e) => {
          e.preventDefault();
          const formData = new FormData(form);
          const url = form.action;
          fetch(url, { method: form.method, body: formData })
            .then((response) => {
              return response.json();
            })
            .then((json) => {
              updateCart(json);
            });
        });
      }
    });
  }
  removeBooksFromCart();
});

// Обробка форми відгуків
const reviewForm = document.getElementById("reviewForm");
const ratingInputs = document.querySelectorAll('input[name="rating"]');
const ratingText = document.querySelector(".rating-text");

// Оновлення тексту рейтингу
ratingInputs.forEach((input) => {
  input.addEventListener("change", function () {
    const ratingTexts = {
      1: "Жахливо",
      2: "Погано",
      3: "Нормально",
      4: "Добре",
      5: "Відмінно",
    };
    ratingText.textContent = ratingTexts[this.value];
    ratingText.className = "rating-text text-warning fw-bold";
  });
});

// Відправка форми
reviewForm.addEventListener("submit", function (e) {
  e.preventDefault();

  const formData = new FormData(this);
  const reviewData = {
    name:
      formData.get("reviewerName") ||
      document.getElementById("reviewerName").value,
    email:
      formData.get("reviewerEmail") ||
      document.getElementById("reviewerEmail").value,
    rating: document.querySelector('input[name="rating"]:checked')?.value,
    text: document.getElementById("reviewText").value,
  };

  // Перевірка мінімальної довжини відгуку
  if (reviewData.text.length < 10) {
    alert("Відгук повинен містити мінімум 10 символів");
    return;
  }

  // Тут можна додати відправку на сервер
  alert("Дякуємо за ваш відгук! Він буде опублікований після модерації.");

  // Очищення форми
  this.reset();
  ratingText.textContent = "Оберіть оцінку";
  ratingText.className = "rating-text text-muted";
});
