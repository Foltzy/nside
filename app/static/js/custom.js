// custom.js

$(document).ready(function(){
    // =======================================
    // CONTAINER LOGIC
    // =======================================
    $('#map-container').hide();
    $('#carouselExampleIndicators').hide();
    $('.display-cont').show();

    $('#back-trigger').on('click', function() {
        $('.display-cont').show();
        $('#map-container').hide();
        $('#carouselExampleIndicators').hide();
    });

    $('.map-trigger').on('click', function() {
        $('.display-cont').hide();
        $('#map-container').show();
        $('#carouselExampleIndicators').hide();
    });

    $('.room-img-trigger').on('click', function() {
        $('.display-cont').hide();
        $('#map-container').hide();
        $('#carouselExampleIndicators').show();
    });



    // =======================================
    // PREVIEW INPUT 
    // =======================================
    $('#rooms').on('input', function() {
        inner = $(this).find('option:selected').text();
        if (inner) {
            $('#user_room').removeClass("text-muted");
        } 

        $('#user_room').html(inner)
    });

    $('#first_name').on('input', function() {
        first = $('#first_name').val().substr(0, 1);
        inner = $('#first_name').val();
        if (inner) {
            $('#user_first').removeClass("text-muted");
        } 

        $('#user_first').html(inner);
        $('#first_letter').html(first);
    });

    $('#last_name').on('input', function() {
        first = $('#last_name').val().substr(0, 1);
        inner = $('#last_name').val();
        if (inner) {
            $('#user_last').removeClass("text-muted");
        } 

        $('#user_last').html(inner);
        $('#second_letter').html(first);
    });

    $('#email').on('input', function() {
        inner = $('#email').val();
        if (inner) {
            $('#user_email').removeClass("text-muted");
        } 

        $('#user_email').html(inner);
    });

    $('#password').on('input', function() {
        inner = $('#password').val();
        if (inner) {
            $('#user_password').removeClass("text-muted");
        } 

        $('#user_password').html(inner);
    });

    let cstudent = document.getElementById('cstudent');
    let cparent = document.getElementById('cparent');
    let cdean = document.getElementById('cdean');

    $('#cstudent').on('input', function() {
        if (cstudent.checked == true) {
            $('#user_role').removeClass("bg-match-avatar");
            $('#user_role').addClass("badge-warning");
            $('#user_role').html("Student");

            
            $('#avatar').addClass("bg-warning text-dark");
        } else {
            $('#user_role').addClass("bg-match-avatar");
            $('#user_role').removeClass("badge-warning");
            $('#user_role').html("Role");

            $('#avatar').removeClass("bg-warning bg-primary bg-success text-dark");
        }
    });

    $('#cparent').on('input', function() {
        if (cparent.checked == true) {
            $('#user_role').removeClass("bg-match-avatar");
            $('#user_role').addClass("badge-success");
            $('#user_role').html("Parent");

            $('#avatar').addClass("bg-success");
        } else {
            $('#user_role').addClass("bg-match-avatar");
            $('#user_role').removeClass("badge-success");
            $('#user_role').html("Role");

            $('#avatar').removeClass("bg-warning bg-primary bg-success text-dark");
        }
    });

    $('#cdean').on('input', function() {
        if (cdean.checked == true) {
            $('#user_role').removeClass("bg-match-avatar");
            $('#user_role').addClass("badge-primary");
            $('#user_role').html("Dean");

            $('#avatar').addClass("bg-primary");
        } else {
            $('#user_role').addClass("bg-match-avatar");
            $('#user_role').removeClass("badge-primary");
            $('#user_role').html("Role");

            $('#avatar').removeClass("bg-warning bg-primary bg-success text-dark");
        }
    });



    // =======================================
    // POPULATE SELECT FIELDS
    // =======================================
    // $('#rooms').empty();
    // $('#buildings').empty();

    // $('#buildings').on('change', function(e) {
    //     // remove option except the placeholder
    //     $('#rooms .option-value').remove();
    // });

    // let building_select = document.getElementById('buildings');
    // let room_select = document.getElementById('rooms');

    // building_select.onchange = function() {
    //     $(room_select).empty();

    //     building = building_select.value;

    //     fetch('/room/' + building).then(function(response) {
    //         response.json().then(function(data) {
    //             let optionHTML = '';

    //             optionHTML += '<option class="option-placeholder" disabled="" selected="">Room</option>';
                
    //             for (let room of data.rooms) {
    //                 optionHTML += '<option class="option-value" value="' + room.id + '">' + room.room_number + '</option>'
    //             }

    //             console.log('current optionHTML: ' + optionHTML);
    //             room_select.innerHTML = optionHTML;
    //         });
    //     });
    // }

    // $('#colleges').on('change', function() {
    //     var $buildings = $('#buildings').empty();

    //     var college = $(this).val();

    //     fetch('/building/' + college).then(function(response) {
    //         response.json().then(function(data) {
    //             //var option = new Option('building...', null, true, true);

    //             let optionHTML = '';

    //             optionHTML += '<option class="option-placeholder" disabled="" selected="">Building</option>';

    //             for (let building of data.buildings) {
    //                 optionHTML += '<option class="option-value" value="' + building.id + '">' + building.name + '</option>'
    //             }

    //             console.log('current optionHTML: ' + optionHTML);

    //             $buildings.html(optionHTML);
    //         });
    //     });
    // });

    // $('#colleges').on('change', function() {
    //     $('#buildings').empty();
    //     $('#rooms').empty();
    // });
});
