let swiperOne = new Swiper(".gallerySwiper", {
  slidesPerView: "auto",
  spaceBetween: 16,
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
});

let swiperTwo = new Swiper(".recommendedSwiper", {
  slidesPerView: "auto",
  spaceBetween: 16,
  navigation: {
    nextEl: "#swiper-button-next-recommended",
    prevEl: "#swiper-button-prev-recommended",
  },
  loop: false,
  preventClicks: false,
  preventClicksPropagation: false,
  watchSlideProgress: true,
});

let swiperThree = new Swiper(".productSwiperThumbs", {
  spaceBetween: 10,
  slidesPerView: 4,
  freeMode: true,
  watchSlidesProgress: true,
});

let swiperFour = new Swiper(".productSwiper", {
  loop: true,
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
  thumbs: {
    swiper: swiperThree,
  },
});
