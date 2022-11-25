var swiperOne = new Swiper(".gallerySwiper", {
  slidesPerView: "auto",
  spaceBetween: 16,
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
});

var swiperTwo = new Swiper(".recommendedSwiper", {
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

var swiperThree = new Swiper(".productSwiperThumbs", {
  spaceBetween: 10,
  slidesPerView: 4,
  freeMode: true,
  watchSlidesProgress: true,
});

var swiperFour = new Swiper(".productSwiper", {
  loop: true,
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
  thumbs: {
    swiper: swiperThree,
  },
});
