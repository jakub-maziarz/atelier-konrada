var alternativeCheckbox = document.getElementById("data-a");
var alternativeAddress = document.querySelector(".order-data-alternative");

var nextButton = document.querySelector(".next");

$(".next").click(function (e) {
  e.preventDefault();
  var orderData = document.querySelector(".order-data");
  var orderDataAlternative = document.querySelector(".order-data-alternative");
  var cartDataInputs = orderData.querySelectorAll(".form-input input");
  var cartDataAlternativeInputs = orderDataAlternative.querySelectorAll(".form-input input");
  var token = $(this).closest(".order-navigation").find("input[name=csrfmiddlewaretoken").val();
  var cartDataJson = {};
  var cartDataAlternativeJson = {};
  var completeData = true;
  var completeAlternativeData = true;
  cartDataInputs.forEach(function (input) {
    if (input.value == "") {
      input.style.border = "2px solid red";
      input.placeholder = "Wymagane pole";
      completeData = false;
    } else {
      input.style.border = "none";
      input.placeholder = "";
      var inputId = input.id;
      cartDataJson[input.id] = input.value;
    }
  });
  if (orderData.querySelector(".form-input textarea").value != "") {
    cartDataJson[orderData.querySelector(".form-input textarea").id] = orderData.querySelector(".form-input textarea").value;
  }
  cartDataJson = JSON.stringify(cartDataJson);

  if (alternativeCheckbox.checked) {
    cartDataAlternativeInputs.forEach(function (input) {
      if (input.value == "") {
        input.style.border = "2px solid red";
        input.placeholder = "Wymagane pole";
        completeAlternativeData = false;
      } else {
        input.style.border = "none";
        input.placeholder = "";
        var inputId = input.id;
        cartDataAlternativeJson[input.id] = input.value;
      }
    });
    if (orderDataAlternative.querySelector(".form-input textarea").value != "") {
      cartDataAlternativeJson[orderDataAlternative.querySelector(".form-input textarea").id] = orderDataAlternative.querySelector(".form-input textarea").value;
    }
  }

  cartDataAlternativeJson = JSON.stringify(cartDataAlternativeJson);

  if (completeData && completeAlternativeData) {
    $.ajax({
      type: "POST",
      url: "/update-data-cart",
      data: {
        cartData: cartDataJson,
        cartDataAlternative: cartDataAlternativeJson,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        window.location.href = response.url;
      },
    });
  }
});
if (alternativeCheckbox.checked) {
  alternativeAddress.classList.add("active");
}

alternativeCheckbox.addEventListener("change", () => {
  if (alternativeCheckbox.checked) {
    alternativeAddress.classList.add("active");
  } else {
    alternativeAddress.classList.remove("active");
  }
});
