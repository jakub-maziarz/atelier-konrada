$(".message-btn").click(function (e) {
  e.preventDefault();

  var email = $(".email").val();
  var topic = $(".topic").val();
  var message = $(".form-input textarea").val();
  var token = $(this).closest(".contact-form").find("input[name=csrfmiddlewaretoken").val();
  var completeData = true;

  if (email == "") {
    completeData = false;
    $(".email").css("border", "2px solid red");
    $(".email").attr("placeholder", "Wymagane pole");
  } else {
    $(".email").css("border", "none");
    $(".email").attr("placeholder", "");
  }
  if (topic == "") {
    completeData = false;
    $(".topic").css("border", "2px solid red");
    $(".topic").attr("placeholder", "Wymagane pole");
  } else {
    $(".topic").css("border", "none");
    $(".topic").attr("placeholder", "");
  }
  if (message == "") {
    completeData = false;
    $(".message").css("border", "2px solid red");
    $(".message").attr("placeholder", "Wymagane pole");
  } else {
    $(".message").css("border", "none");
    $(".message").attr("placeholder", "");
  }

  if (completeData) {
    $.ajax({
      type: "POST",
      url: "/send-message",
      data: {
        email: email,
        topic: topic,
        message: message,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        $(".email").val("");
        $(".topic").val("");
        $(".message").val("");
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
