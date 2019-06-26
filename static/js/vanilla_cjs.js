// ;var FUNCTIONS = (function() {

// //     // Next/previous controls
// //     function plusSlides(n) {
// //         showSlides(n);
// //     }
   
// //     // Thumbnail image controls
// //     function currentSlide(n) {
// //         showSlides(n);
// //     }
   
// //     function showSlides(n) {
// //         console.log("show slides: " + n);

// //         var $slides = $('.mySlides');
// //         var $dots = $('.dot');

// //         $slides.hide();
// //         $dots.removeClass('active');

// //         $slides.eq(n).show();
// //         $dots.eq(n).addClass('active');
// //     }

// //     return {
// //         name        : "I'm called FUNCTIONS",

// //         plusSlides  : plusSlides,
// //         currentSlide: currentSlide,
// //         showSlides  : showSlides
// //     };
    

//     return {
//     name        : "I'm called FUNCTIONS",

//     plusSlides  : plusSlides,
//     currentSlide: currentSlide,
//     showSlides  : showSlides
//     };
// })();
 
// slideshow js
var slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
    showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    var i;
    var slides = document.getElementsByClassName("mySlides");
    var dots = document.getElementsByClassName("dot");
    if (n > slides.length) {slideIndex = 1} 
    if (n < 1) {slideIndex = slides.length}

    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none"; 
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }

    slides[slideIndex-1].style.display = "block"; 
    dots[slideIndex-1].className += " active";
}