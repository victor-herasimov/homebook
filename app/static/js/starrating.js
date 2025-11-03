"use strict";

// show ratings
const ratings = document.querySelectorAll(".star-rating");

if (ratings.length > 0) {
  initRatings();
}

function initRatings() {
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
  // end show ratings

  function setRating(rating) {
    const ratingItems = rating.querySelectorAll(".star-rating__item");
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
      });
    });
  }
}
