function updatePageLinks() {
  let page_links = document.querySelectorAll(".page-link");
  let url, search_params, current_url, current_search_params;
  for (let i = 0; i < page_links.length; i++) {
    url = new URL(page_links[i].href);
    search_params = url.searchParams;
    current_url = new URL(window.location.href);
    current_search_params = current_url.searchParams;
    current_search_params.set("page", search_params.get("page"));
    current_url.search = current_search_params.toString();
    page_links[i].href = current_url.toString();
  }
}

let categories = document.querySelector(".categories-list");
let categoriesToggler = document.querySelector(".categories-toggle");
let filterOptions = document.querySelector(".filter-options");
let filterOptionsToggler = document.querySelector(".filter-toggle");

categoriesToggler.addEventListener("click", () => {
  categories.classList.toggle("categories-active");

  setTimeout(() => {
    if (categories.classList.contains("categories-active") && categoriesToggler.classList.contains("fa-plus")) {
      categoriesToggler.classList.remove("fa-plus");
      categoriesToggler.classList.add("fa-minus");
    } else if (!categories.classList.contains("categories-active") && categoriesToggler.classList.contains("fa-minus")) {
      categoriesToggler.classList.remove("fa-minus");
      categoriesToggler.classList.add("fa-plus");
    }
  }, 250);
});

filterOptionsToggler.addEventListener("click", () => {
  filterOptions.classList.toggle("filter-active");

  setTimeout(() => {
    if (filterOptions.classList.contains("filter-active") && filterOptionsToggler.classList.contains("fa-plus")) {
      filterOptionsToggler.classList.remove("fa-plus");
      filterOptionsToggler.classList.add("fa-minus");
    } else if (!filterOptions.classList.contains("filter-active") && filterOptionsToggler.classList.contains("fa-minus")) {
      filterOptionsToggler.classList.remove("fa-minus");
      filterOptionsToggler.classList.add("fa-plus");
    }
  }, 250);
});

let startPrice = document.getElementById("startPrice");
let endPrice = document.getElementById("endPrice");
const pattern = /[^0-9]+$/;

startPrice.addEventListener("input", () => {
  if (pattern.test(startPrice.value)) {
    startPrice.value = "";
  }
});

endPrice.addEventListener("input", () => {
  if (pattern.test(endPrice.value)) {
    endPrice.value = "";
  }
});

let from_to_price = document.getElementById("filter-button");

from_to_price.addEventListener("click", () => {
  let url = new URL(window.location.href);
  let search_params = url.searchParams;
  if (startPrice.value == "" && endPrice.value == "") {
    startPrice.style.border = "2px solid red";
    startPrice.placeholder = "Podaj";
    endPrice.style.border = "2px solid red";
    endPrice.placeholder = "cenę";
  } else {
    startPrice.style.border = "none";
    startPrice.placeholder = "Od";
    endPrice.style.border = "none";
    endPrice.placeholder = "Do";
    if (startPrice.value != "") {
      search_params.set("from_price", startPrice.value);
    }
    if (endPrice.value != "") {
      search_params.set("to_price", endPrice.value);
    }
  }
  if (search_params.has("page")) {
    search_params.delete("page");
  }
  url.search = search_params.toString();
  if (url.toString().includes("?")) {
    window.location = url;
  }
});

function resetFromToPrice() {
  let url = new URL(window.location.href);
  let search_params = url.searchParams;
  if (search_params.has("from_price")) {
    search_params.delete("from_price");
  }
  if (search_params.has("to_price")) {
    search_params.delete("to_price");
  }
  if (search_params.has("page")) {
    search_params.delete("page");
  }
  url.search = search_params.toString();
  window.location = url;
}

let product_state = document.getElementById("state-product");

product_state.addEventListener("change", () => {
  let url = new URL(window.location.href);
  let search_params = url.searchParams;
  search_params.set("product_state", product_state.value);
  if (search_params.has("page")) {
    search_params.delete("page");
  }
  url.search = search_params.toString();
  if (url.toString().includes("?")) {
    window.location = url;
  }
});

let sort_product = document.getElementById("product-sort");

sort_product.addEventListener("change", () => {
  let url = new URL(window.location.href);
  let search_params = url.searchParams;
  search_params.set("sort_product", sort_product.value);
  url.search = search_params.toString();
  if (url.toString().includes("?")) {
    window.location = url;
  }
});

$(".catalog-product-button").click(function (e) {
  e.preventDefault();

  let product_id = $(this).closest(".catalog-product-add").find(".prod_id").val();
  let token = $(this).closest(".catalog-product-add").find("input[name=csrfmiddlewaretoken").val();

  $.ajax({
    type: "POST",
    url: "/add-to-cart",
    data: {
      product_id: product_id,
      csrfmiddlewaretoken: token,
    },
    success: function (response) {
      $(".cart-total").html(response.cart_quantity);
      iziToast.show({
        class: "alert",
        message: response.status,
        messageColor: "#fff",
        backgroundColor: "#727d31",
        position: "topRight",
      });
    },
    error: function (response) {
      iziToast.show({
        class: "alert",
        message: response.responseJSON.error,
        messageColor: "#fff",
        backgroundColor: "#ff0000",
        position: "topRight",
      });
    },
  });
});
