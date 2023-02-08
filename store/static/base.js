// When the user scrolls the page, execute myFunction
window.onscroll = function () {
  myFunction();
};

// Get the navbar
var navbar = document.getElementById("navbar");

// Get the offset position of the navbar
var sticky = navbar.offsetTop;

// Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
function myFunction() {
  if (window.pageYOffset >= sticky) {
    navbar.classList.add("sticky");
  } else {
    navbar.classList.remove("sticky");
  }
}

// pop-up sale-notification
$("#plus").click(function () {
  $("#popUp").css("margin-left", "0px");
  $(".sale-offer-notification").css("margin-left", "-525px");
});

$("#close").click(function () {
  $("#popUp").css("margin-left", "-425px");
  $(".sale-offer-notification").css("margin-left", "0px");
});


// 
var button = document.querySelector('.button');
var field = document.querySelector('.field');
var icon = document.querySelector('.header i');
var text = document.querySelector('.header p');

button.addEventListener('click', function(){
  
  if(field.value === ''){
    field.placeholder = 'You must enter your email';
    // alert('You must enter an email');
  } else {
    $.ajax({
        type : "POST",
        url: 'http://127.0.0.1:8000/account/subscribed/',
        data : {
            email:field.value,
            csrfmiddlewaretoken: CSRF_TOKEN,
            action: "post",
        },
        success: function (data) {
            console.log('success :',field.value);
            icon.classList.toggle('animation');
            text.classList.toggle('show');
        }
    });

  }
});