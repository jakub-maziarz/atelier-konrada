let qtyProduct = document.getElementById("quantityproduct");

qtyProduct.addEventListener("input", () => {
  qtyProduct.value = "1";
});

function incrementQuantity(max) {
  let qtyProduct = document.getElementById("quantityproduct");
  let value = parseInt(qtyProduct.value, 10);
  value = isNaN(value) ? 0 : value;
  console.log(parseInt(max, 10) == 0);
  if (parseInt(max, 10) == 0) {
    value++;
  } else {
    if (value < parseInt(max, 10)) {
      value++;
    }
  }
  qtyProduct.value = value;
}

function decrementQuantity() {
  let qtyProduct = document.getElementById("quantityproduct");
  let value = parseInt(qtyProduct.value, 10);
  value = isNaN(value) ? 0 : value;
  if (value > 1) {
    value--;
    qtyProduct.value = value;
  }
}

$(".product-button").click(function (e) {
  e.preventDefault();

  let product_id = $(this).closest(".add-to-cart").find(".prod_id").val();
  let product_qty = $(".productquantity").val();
  let token = $(this).closest(".add-to-cart").find("input[name=csrfmiddlewaretoken").val();

  $.ajax({
    type: "POST",
    url: "/add-to-cart",
    data: {
      product_id: product_id,
      product_qty: product_qty,
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
