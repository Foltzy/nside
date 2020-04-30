// custom.js
$(document).ready(function(){
    setTimeout(function() {
        $('.full-alert').fadeOut(4000);
    }, 3500);

    $('#colleges').select2({
        placeholder: "College",
        allowClear: false
    });

    $('#buildings').select2({
        placeholder: "Building",
        allowClear: false
    });

    $('#rooms').select2({
        placeholder: "Room",
        allowClear: false
    });

    $('#rooms').empty();
    $('#buildings').empty();


    $('#buildings').on('change', function(e) {
        $('#rooms .option-placeholder').html('room...');

        // remove option except the placeholder
        $('#rooms .option-value').remove();
    });

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
            });
        });
    });

    $('#colleges').on('change', function() {
        $('#buildings').empty();
        $('#rooms').empty();
    });
});