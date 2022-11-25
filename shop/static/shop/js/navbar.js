var menu = document.querySelector(".menu");
var menuBtn = document.querySelector(".menu-btn");
var closeBtn = document.querySelector(".close-btn");
var search = document.querySelector(".search");
var searchToggler = document.querySelector(".search-toggle");
var searchForm = document.getElementById("search-form");
var searchInput = document.querySelector(".product-input");
var searchBtn = document.querySelector(".btn-product-inline");
var clearBtn = document.querySelector(".clear");

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
