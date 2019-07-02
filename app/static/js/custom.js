// custom.js
// watch nav scroll
// $(function () {
//     $(document).scroll(function () {
//       var $nav = $(".fixed-top");
//       var $dropdown = $(".select2-dropdown");
//       var $masthead = $(".masthead");
//       $nav.toggleClass('scrolled', $(this).scrollTop() > $nav.height());
//       $dropdown.toggleClass('scrolled', $(this).scrollTop() > $masthead.height());
//     });
//   });

// fade flash messages out
$(document).ready(function(){
    setTimeout(function() {
        $('.ribbon-flash').fadeOut('slow');
    }, 3500);
});

// (college) search bar js
// $(document).ready(function() {
//     var select_field = document.getElementById('colleges');
//     var option = document.createElement('option');

//     // add text to the select field
//     // option.appendChild(document.createTextNode('default'));
//     option.id = 'default';

//     select_field.appendChild(option);
// });

$(document).ready(function() {
    $('#colleges').select2({
        placeholder: "College",
        allowClear: false
    });
});

$(document).ready(function() {
    $('#buildings').select2({
        placeholder: "Building",
        allowClear: false
    });
});

$(document).ready(function() {
    $('#rooms').select2({
        placeholder: "Room",
        allowClear: false
    });
});

// filter 'display' select2 fields
$(document).ready(function(){
    //let college_select = document.getElementById('colleges');
    //let building_select = document.getElementById('buildings');

    $('#colleges').on('change', function() {
        var $buildings = $('#buildings').empty();

        var college = $(this).val();

        fetch('/building/' + college).then(function(response) {
            response.json().then(function(data) {
                //var option = new Option('building...', null, true, true);

                let optionHTML = '';

                optionHTML += '<option class="option-placeholder" disabled="" selected="">Building</option>';

                for (let building of data.buildings) {
                    optionHTML += '<option class="option-value" value="' + building.id + '">' + building.name + '</option>'
                }

                console.log('current optionHTML: ' + optionHTML);

                $buildings.html(optionHTML);

                //$buildings.trigger('change');
            });
        });
    });

    // college_select.onchange = function() {
    //     $(building_select).empty();

    //     college = college_select.value;

    //     fetch('/building/' + college).then(function(response) {
    //         response.json().then(function(data) {
    //             let optionHTML = '';

    //             optionHTML += '<option class="option-placeholder" disabled="" selected="">building...</option>';

    //             for (let building of data.buildings) {
    //                 optionHTML += '<option class="option-value" value="' + building.id + '">' + building.name + '</option>'
    //             }

    //             console.log('current optionHTML: ' + optionHTML);
    //             building_select.innerHTML = optionHTML;

    //             $(building_select).trigger('change');
    //         });
    //     });
    // }
});

// filter 'display' select2 fields
$(document).ready(function(){
    let building_select = document.getElementById('buildings');
    let room_select = document.getElementById('rooms');

    building_select.onchange = function() {
        $(room_select).empty();

        building = building_select.value;

        fetch('/room/' + building).then(function(response) {
            response.json().then(function(data) {
                let optionHTML = '';

                optionHTML += '<option class="option-placeholder" disabled="" selected="">Room</option>';
                
                for (let room of data.rooms) {
                    optionHTML += '<option class="option-value" value="' + room.id + '">' + room.room_number + '</option>'
                }

                console.log('current optionHTML: ' + optionHTML);
                room_select.innerHTML = optionHTML;
            });
        });
    }
});

// CHANGE THIS TO HIDE
// disable second dropdown field if first isn't filled out
$(document).ready(function(){
    //$('#colleges').on('change', function(e) {
    //    $('#buildings .option-placeholder').html('building...');

        // remove option except the placeholder
    //    $('#buildings .option-value').remove();

        
        // $('#buildings').trigger('change');
    //});

    $('#buildings').on('change', function(e) {
        $('#rooms .option-placeholder').html('room...');

        // remove option except the placeholder
        $('#rooms .option-value').remove();
    });
});

// webrotate script // MAKE FUNCTION
// jQuery(document).ready(function(){
//     console.log('web rotate 360 is loading...');
//     console.log('wr360 model xml path loaded: '); 
//     jQuery('#wr360PlayerId').rotator({
//           licenseFileURL: 'license.lic',
//           configFileURL: '/static/360_assets/for_site_bathroom_ren/for_site_bathroom_ren.xml',
//           graphicsPath: '/static/img/basic',
//           zIndexLayersOn: false,
//           responsiveBaseWidth: 600,
//           responsiveMinHeight: 0,
//           googleEventTracking: false,
//     });
// });

$(document).ready(function(){
    // attempt to disable select fields
    // var $buildings = $('#buildings');
    // var $rooms = $('#rooms');

    // $('.option-value').click(function() {
    //     $('#colleges option').each(function() {
    //         if($(this).is(':selected')) {
    //             $buildings.disabled = "false"
    //         }
    //     });
    // });

    // $('.option-value').click(function() {
    //     $('#buildings option').each(function() {
    //         if($(this).is(':selected')) {
    //             $rooms.disabled = "false"
    //         }
    //     });
    // });
    $('#rooms').empty();
    $('#buildings').empty();

    $("#dot-hide").click(function(){
        $("#prev").toggle();
        $("#next").toggle();

        if ($('#prev').is(':visible')) {
            $("#dot-hide img").attr("src","/static/img/svg/hide.svg");
        } else {
            $("#dot-hide img").attr("src","/static/img/svg/eye.svg");
        }

        // $("#dot-hide img").attr("src","{{ url_for('static', filename='img/svg/eye.svg') }}");
        // $("#dot-hide img").attr("src","{{ url_for('static', filename='img/svg/hide.svg') }}");
    });


    $('#prev').on('click', function() {
        plusSlides(-1);
    });

    $('#next').on('click', function() {
        plusSlides(1);
        console.log('plusSlides(1)');
    });

    // $('.dot').each(function(index) {
    //     $(this).on('click', function() {
    //         console.log('click index: ' + index);
    //         currentSlide(index);
    //     });
    // });

    // var f = FUNCTIONS;

    // console.log("NAME: " + f.name);
    // console.log("NAME: " + f.foobar);

    // slideshow js
    var slideIndex = 1;
    console.log("showSlides");
    showSlides(slideIndex);

    $('#colleges').on('change', function() {
        $('#buildings').empty();
        $('#rooms').empty();
    });

    // $('.arrow-down').hide();
    // console.log('arrow hidden');

    $('#rooms').on('change', function(){
        $('.arrow-down').show();
        console.log('arrow showing');
    });

    if ($('.p-college-name').text() == '') {
        $('.arrow-down').hide();
    } else {
        $('.arrow-down').show();
    }
});