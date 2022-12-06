let menu = document.querySelector(".menu");
let menuBtn = document.querySelector(".menu-btn");
let closeBtn = document.querySelector(".close-btn");
let search = document.querySelector(".search");
let searchToggler = document.querySelector(".search-toggle");
let searchForm = document.getElementById("search-form");
let searchInput = document.querySelector(".product-input");
let searchBtn = document.querySelector(".btn-product-inline");
let clearBtn = document.querySelector(".clear");

menuBtn.addEventListener("click", () => {
  menu.classList.add("active");
});

closeBtn.addEventListener("click", () => {
  menu.classList.remove("active");
});

searchToggler.addEventListener("click", () => {
  search.classList.toggle("search-active");
});

searchInput.addEventListener("input", () => {
  if (searchInput.value != "") {
    document.querySelector(".clear").style.display = "flex";
  } else {
    document.querySelector(".clear").style.display = "none";
  }
});

searchBtn.addEventListener("click", () => {
  if (searchInput.value == "") {
    search.classList.toggle("search-active-inline");
  } else {
    searchForm.submit();
  }
});

clearBtn.addEventListener("click", () => {
  document.getElementById("searchproducts").value = "";
  document.querySelector(".clear").style.display = "none";
});
