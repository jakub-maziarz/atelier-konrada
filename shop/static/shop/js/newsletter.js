$(".newsletter-btn").click(function (e) {
  e.preventDefault();

  let email = $(".email-input").val();
  let token = $(this).closest(".newsletter-email").find("input[name=csrfmiddlewaretoken").val();

  if (email == "") {
    $(".email-input").css("border", "2px solid red");
    $(".email-input").attr("placeholder", "Wymagane pole");
  } else {
    $(".email-input").css("border", "none");
    $(".email-input").attr("placeholder", "Wpisz adres e-mail");
    $.ajax({
      type: "POST",
      url: "/add-to-newsletter",
      data: {
        email: email,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        $(".email-input").val("");
        iziToast.show({
          class: "alert",
          message: response.status,
          messageColor: "#fff",
          backgroundColor: "#727d31",
          position: "topRight",
        });
      },
    });
  }
});
