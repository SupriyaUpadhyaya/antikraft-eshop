function myFunction() {
    var x = document.getElementById("password");
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
  }


  function validateForm() {
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirm-password").value;

    if (password !== confirmPassword) {
      document.getElementById("password-error").style.display = "block";
      return false;
    }
    return true;
  }

  var subjectObject = {
      "Luxury": ["Antique Architectural", "Antique Boxes", "Antique Folkart", "Antique Kitchenware", "Antique Perfumes"],
      "Art": ["Abstract", "Paintings", "Sculptures", "Vintage", "Other"],
      "Clocks": ["Astronamical Clock", "Cuckoo Clock", "Mantel Clock", "Pocket Watches", "Wall Clock"],
      "Furniture": ["Beds and Headboards", "Case-pices And Storage", "Garden", "Seating and Tables", "Wall Decoration"],
      "Jewelry & Watches": ["Antique Jewelry", "Antique Watches", "Artisan Jewelry", "Victorian Jewelry", "Vintage Jewelry"],
      "Lighting": ["candle Holders", "Chandelier", "Floor Lamps", "Table Lamps", "Wall Lamps"],
      "Mirrors": ["Cheval Mirrors", "Pocket Mirror", "Silver Mirror", "Two-way Mirror", "Wall Mirror"],
      "Silver": ["American Silver", "Antique Silver", "English Silver", "French Silver", "Sterling Silver"]
  }
  window.onload = function() {
    var topicSel = document.getElementById("topic");
    var chapterSel = document.getElementById("chapter");
    for (var x in subjectObject) {
      topicSel.options[topicSel.options.length] = new Option(x, x);
    }
    topicSel.onchange = function() {
         //empty Chapters dropdown
         chapterSel.length = 1;
          //display correct values
          var z = subjectObject[this.value];
    for (var i = 0; i < z.length; i++) {
      chapterSel.options[chapterSel.options.length] = new Option(z[i], z[i]);
    }
        }
  }

  function offerPercent() {
    // Get the checkbox
    var checkBox = document.getElementById("offerflag");
    // Get the output text
    var text = document.getElementById("offerpercent");
  
    // If the checkbox is checked, display the output text
    if (checkBox.checked == true){
      text.style.display = "block";
    } else {
      text.style.display = "none";
    }
  }

  function sponsorproduct() {
    // Get the checkbox
    var checkBox = document.getElementById("sponsor");
    // Get the output text
    var text = document.getElementById("sponsoramt");
  
    // If the checkbox is checked, display the output text
    if (checkBox.checked == true){
      text.style.display = "block";
    } else {
      text.style.display = "none";
    }
  }

  function fileValidation() {
    var fileInput = document.getElementById('image');
    
    for (var i = 0; i < fileInput.files.length; ++i) {
      var ext = fileInput.files[i].name.substr(-3);
      console.log(ext)
      if(ext!== "jpg" && ext!== "png")  {
        alert('Not an accepted file extension. Only JPG and PNG files accepted');
        fileInput.value = '';
        return false;
      }
    }
    
    console.log(fileInput.files.length)
    if(fileInput.files.length != 5){
      alert("Please upload 5 images");
      fileInput.value = '';
      return false;
    }
}

function offersFileValidation() {
  var fileInput = document.getElementById('image');
  
  for (var i = 0; i < fileInput.files.length; ++i) {
    var ext = fileInput.files[i].name.substr(-3);
    console.log(ext)
    if(ext!== "jpg" && ext!== "png")  {
      alert('Not an accepted file extension. Only JPG and PNG files accepted');
      fileInput.value = '';
      return false;
    }
  }
  
  console.log(fileInput.files.length)
  if(fileInput.files.length != 1){
    alert("Please upload 5 images");
    fileInput.value = '';
    return false;
  }
}

$(function() {
  $(".msg-panel").show()
  setTimeout(function() {
      $(".msg-panel").hide()
  }, 10000);
});

