$(document).on("click", ".place-order", function (e) {
  e.preventDefault();
  var token = $(this).closest(".order-navigation").find("input[name=csrfmiddlewaretoken").val();
  $.ajax({
    type: "POST",
    url: "/place-order",
    data: {
      csrfmiddlewaretoken: token,
    },
    success: function (response) {
      window.location.href = response.url;
    },
    error: function (response) {
      window.location.href = response.responseJSON.url;
    },
  });
});
