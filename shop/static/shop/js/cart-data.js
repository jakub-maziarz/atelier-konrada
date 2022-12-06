let alternativeCheckbox = document.getElementById("data-a");
let alternativeAddress = document.querySelector(".order-data-alternative");

let nextButton = document.querySelector(".next");

$(".next").click(function (e) {
  e.preventDefault();
  let orderData = document.querySelector(".order-data");
  let orderDataAlternative = document.querySelector(".order-data-alternative");
  let cartDataInputs = orderData.querySelectorAll(".form-input input");
  let cartDataAlternativeInputs = orderDataAlternative.querySelectorAll(".form-input input");
  let token = $(this).closest(".order-navigation").find("input[name=csrfmiddlewaretoken").val();
  let cartDataJson = {};
  let cartDataAlternativeJson = {};
  let completeData = true;
  let completeAlternativeData = true;
  cartDataInputs.forEach(function (input) {
    if (input.value == "") {
      input.style.border = "2px solid red";
      input.placeholder = "Wymagane pole";
      completeData = false;
    } else {
      input.style.border = "none";
      input.placeholder = "";
      let inputId = input.id;
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
        let inputId = input.id;
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
