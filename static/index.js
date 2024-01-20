window.onload = () => {
  let fileType = "image";
  $("#sendbutton").click(() => {
    $("#loadFile").css("display", "block");
    imagebox = $("#imagebox");
    link = $("#link");
    input = $("#imageinput")[0];
    if (input.files && input.files[0]) {
      let formData = new FormData();
      formData.append("video", input.files[0]);
      console.log(formData);
      $.ajax({
        url: "/detect",
        type: "POST",
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        error: function (data) {
          console.log("upload error", data);
          console.log(data.getAllResponseHeaders());
        },
        success: function (data) {
          console.log(data);

          $("#loadFile").css("display", "none");
          $('#sendbutton').removeAttr('disabled');
          $("#link").css("visibility", "visible");
          $("#noPlateText").css("display", "block");
          document.getElementById("noPlateText").innerHTML = `<h2>Number Plate is <span style="color: #1e88e5;">${data[1]}</span></h2>`
          $("#download").css("display", "block");
          $("#download").attr("href", "static/Saved/" + data[0]);
          if (fileType = "video") {
            $("#videoImgRes").css("display", "block");
            var timestamp = new Date().getTime();
            $("#videoImgRes").attr("src", "static/Saved/" + data[0]);
          } else {
            $("#imagebox").attr("src", "static/Saved/" + data[0]);
          }
          console.log(data);
        },
      });
    }
    else {
      $("#loadFile").css("display", "none");
      $('#sendbutton').removeAttr('disabled');
    }
  });
  $("#opencam").click(() => {
    console.log("opened openCam");
    $.ajax({
      url: "/opencam",
      type: "GET",
      error: function (data) {
        console.log("upload error", data);
      },
      success: function (data) {
        console.log(data);
      }
    });
  })
};

function readUrl(input) {
  imagebox = $("#imagebox");
  videobox = $("#videobox");
  console.log(imagebox);
  console.log("opened readUrl");
  if (input.files && input.files[0]) {
    let reader = new FileReader();
    reader.onload = function (e) {
      fileType = e.target.result.slice(5, 10);
      console.log(fileType);
      $("#videoImgRes").css("display", "none");
      $("#noPlateText").css("display", "none");
      if (fileType == "video") {
        imagebox.css("display", "none");
        videobox.css("display", "block");
        videobox.attr("src", e.target.result);
        // videobox.height(500);
        // videobox.width(800);
      } else {
        videobox.css("display", "none");
        imagebox.css("display", "block");
        imagebox.attr("src", e.target.result);
        // imagebox.height(500);
        // imagebox.width(800);
      }
    };
    reader.readAsDataURL(input.files[0]);
  }
}

function disableSend() {
  $('#sendbutton').attr('disabled','disabled');
}

function openCam(e){
  console.log("opened openCam");
  e.preventDefault();
  console.log("opened openCam");
  console.log(e);
}