$(document).on("click", ".plusQty", function (e) {
  e.preventDefault();

  let product_id = $(this).closest(".order-product").find(".cart_prod_id").val();
  let product_qty = $(this).closest(".product-qty-buttons").find(".productquantity");
  let product_qty_value = product_qty.val();
  product_qty_value++;
  let token = $(this).closest(".order-product").find("input[name=csrfmiddlewaretoken").val();
  let price_info = $(this).closest(".qty-price").find(".price");

  $.ajax({
    type: "POST",
    url: "/update-cart",
    data: {
      product_id: product_id,
      product_qty: product_qty_value,
      csrfmiddlewaretoken: token,
    },
    success: function (response) {
      $(".cart-total").html(response.cart_quantity);
      product_qty.val(response.cart_product_quantity);
      price_info.html(response.cart_product_price + " zł");
      $(".total-price").html(response.total_cart_price + " zł");
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
$(document).on("click", ".minusQty", function (e) {
  e.preventDefault();

  let product_id = $(this).closest(".order-product").find(".cart_prod_id").val();
  let product_qty = $(this).closest(".product-qty-buttons").find(".productquantity");
  let product_qty_value = product_qty.val();
  product_qty_value--;
  let token = $(this).closest(".order-product").find("input[name=csrfmiddlewaretoken").val();
  let price_info = $(this).closest(".qty-price").find(".price");

  if (product_qty_value != 0) {
    $.ajax({
      type: "POST",
      url: "/update-cart",
      data: {
        product_id: product_id,
        product_qty: product_qty_value,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        $(".cart-total").html(response.cart_quantity);
        product_qty.val(response.cart_product_quantity);
        price_info.html(response.cart_product_price + " zł");
        $(".total-price").html(response.total_cart_price + " zł");
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
  }
});
$(document).on("click", ".product-delete", function (e) {
  e.preventDefault();

  let product_id = $(this).closest(".order-product").find(".cart_prod_id").val();
  let token = $(this).closest(".order-product").find("input[name=csrfmiddlewaretoken").val();
  $.ajax({
    type: "POST",
    url: "/delete-from-cart",
    data: {
      product_id: product_id,
      csrfmiddlewaretoken: token,
    },
    success: function (response) {
      $(".cart-total").html(response.cart_quantity);
      $(".total-price").html(response.total_cart_price + " zł");
      $(".cart-container").load(location.href + " .cart-container");
      iziToast.show({
        class: "alert",
        message: response.status,
        messageColor: "#fff",
        backgroundColor: "#727d31",
        position: "topRight",
      });
    },
  });
});
