const swiper = new Swiper(".new-books-slider", {
  // Optional parameters
  loop: true,
  slidesPerView: 1,
  spaceBetween: 15,
  //   autoHeight: true,
  //   zoom: true,
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
  // Navigation arrows
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },

  // And if we need scrollbar
  scrollbar: {
    el: ".swiper-scrollbar",
  },
  breakpoints: {
    450: {
      slidesPerView: 2,
    },
    768: {
      slidesPerView: 3,
    },
    992: {
      slidesPerView: 4,
    },
  },
});
