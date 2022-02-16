// site_data.js
$(document).ready(function(){
    // grab all elements with the class "hasTooltip"
    $('.hidden').hide();
    $('.hasTooltip').each(function() { 
        $(this).qtip({
            content: {
                text: $(this).next('div') 
            }
        });
        console.log('qtip loaded');
    });

    var apiObj = null;

    function loadLinked_room(apiObj) {
        // linked room
        // get user id from hidden div
        var user_id = $('.current_userid').attr('value');
        // check user_id
        console.log(user_id);

        // why is apiobj null here but not above? can't be null for room link
        // for xml's loaded on document ready they must be a function like above that gets run after the 'apiReadyCallback'
        // if 'apiObj' is null look to this function for the example of how to fix
        // note: 'apiObj' is only null if run before 'apiReadyCallback' is complete 
        console.log(apiObj);

        // query linked room 
        fetch('/linked_room/' + user_id).then(function(response) {
            response.json().then(function(linked_room) {
                console.log(linked_room.linked_xml);
                if (apiObj != null){
                    apiObj.reload(linked_room.linked_xml);
                    console.log(' == linked room reload complete ==');
                }
            });
        });
        // /fetch
    }

    // TODO
    // Call with webrotate operator suggested that I pass the xml file as a variable
    // that was deterimined before the .rotator loads

    // imagerotator 
    // tells webrotate what room to load first then replace with the linked room
    // tells webrotate API how to load xml's as well
    jQuery('#wr360PlayerId').rotator({
        licenseFileURL: '/static/360_assets/license.lic',
        configFileURL: '/static/360_assets/E24_1_final_wr/E24_1_final_wr.xml',
        graphicsPath: '/static/img/retina',
        responsiveBaseWidth: 600,
        responsiveBaseHeight: 550,
        responsiveMinHeight: 0,
        googleEventTracking: false,
        apiReadyCallback: function(api){apiObj = api; loadLinked_room(apiObj);},
    });

    // on change of room select field
    $('#rooms').on('change', function() {
        $('.link-view').empty();
        // updates the first two fields of 'viewing' 
        // to represent selected college name and building name
        // update college name
        $('#colleges option').each(function() {
            console.log('1 pass');
            if($(this).is(':selected')) {
                console.log('2 pass');
                // college select field data
                var college = $(this).html();
                // check college
                console.log('college: ' + college);

                // update college view
                $('.p-college-name').text(college);
            }
        });

        // update building name
        $('#buildings option').each(function() {
            console.log('1 pass');
            if($(this).is(':selected')) {
                console.log('2 pass');
                // building select field data
                var building = $(this).html();
                // check building
                console.log('building: ' + building);

                // update building view
                $('.p-building-name').text(building);
            }
        });

        // if no linked room stil display if selection
        $('.hide').hide();
        $('.wr360_player').show();
        $('#about').show();

        ///////////////////////
        // DYNAMIC SITE DATA //
        ///////////////////////
        // get the selected room id
        var room_id = $(this).val();
        // check the room id
        console.log('room id: ' + room_id);

        // response == return value in fetch
        fetch('/selected_room/' + room_id).then(function(response) {
            response.json().then(function(room) {
                console.log('room: ' + JSON.stringify(room));

                console.log("room number: " + room.number);

                $('.p-room-number').text(room.number);

                // update model
                // FILE PATH FORMAT: FULL  /static/360_assets/model/model.xml  NO QUOTES
                if (apiObj != null){
                    apiObj.reload(room.xml_path);
                    console.log('reload complete');
                    apiObj = apiObj;
                }

                // update description
                $('.r-desc').text(room.desc);

                // update name
                $('.r-name').text(room.building_name + ' ' + room.number);
                // update address
                $('.r-addr').text(room.address);
                // update website
                $(".r-site").attr("href", room.site);
                // update floor plan
                $(".r-floorplan").attr("href", room.floorplan);

                // update internet
                $('.r-inte').text(room.internet) 
                // update outlet count
                $('.r-outl').text(room.outlet_count);
                // update mirror count 
                $('.r-mirr').text(room.mirror_count);
                // update drawer count
                $('.r-draw').text(room.drawer_count);
                // update closet count
                $('.r-clos').text(room.closet_count);
                // update shelf count
                $('.r-shel').text(room.shelf_count);
                // update capacity
                $('.r-capa').text(room.capacity);

                // update gender
                $('.r-gend').text(room.gender);
                $('.r-ac').text(room.ac);
                $('.r-heat').text(room.heating);

                $('.r-outl-t').text(room.outlet_total);
                $('.r-mirr-t').text(room.mirror_total);
                $('.r-draw-t').text(room.drawer_total);
                $('.r-clos-t').text(room.closet_total);
                $('.r-shel-t').text(room.shelf_total);

                // update room dims
                $('.r-room-dims').text(room.full_dims);
                // update bed dims
                $('.r-bed-dims').text(room.bed_dims);
                // update desk dims
                $('.r-desk-dims').text(room.desk_dims);
                // update carpet dims
                $('.r-carp-dims').text(room.carpet_dims);
                // update shelf dims
                $('.r-shel-dims').text(room.shelf_dims);
                // update closet dims
                $('.r-clos-dims').text(room.closet_dims);

                // update to dining hall
                $('.r-hall-com').text(room.to_hall);
                // update to gym
                $('.r-gym-com').text(room.to_gym);
                // udpate to grocery
                $('.r-groc-com').text(room.to_grocery);

                // update fridge
                $('.r-frid-pro').text(room.fridge);
                // update toaster
                $('.r-toas-pro').text(room.toaster);
                // update coffee
                $('.r-coff-pro').text(room.coffee);
                // update tv
                $('.r-tv-pro').text(room.tv);

                // update img1
                $(".r-img1").attr("src", room.img1);
                // update img2
                $(".r-img2").attr("src", room.img2);
                // update img3
                $(".r-img3").attr("src", room.img3);
                // update img4
                $(".r-img4").attr("src", room.img4);
                // update iframe
                $(".r-iframe").attr("src", room.iframe_src);

                // log that updates complete
                console.log('room selection render complete');
            });
        }); 
        // /fetch
    });
});