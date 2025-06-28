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
