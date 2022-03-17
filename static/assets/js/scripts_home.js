///// Global variable Section /////

///// End Global variable Section /////

///// Event Function Section /////
$(document).ready(function() {

    $("#data_readiness_Table").DataTable({
        "dom": '<"top"f>rt<"bottom"p>',
        "order": [1, 'desc'],
        "pageLength": 6
    });
});
///// End Event Function Section /////

 ///// Event Function Section /////
function openNav(param_Sidenav) {
    if (param_Sidenav == 'mySidenav'){
        $("#mySidenav").toggleClass("active");
        $("#sidenav_metadata").removeClass("active");
    }else if (param_Sidenav == 'sidenav_metadata'){
        $("#sidenav_metadata").toggleClass("active");
        $("#mySidenav").removeClass("active");
    }
}

function setnulltoblank(value) {
    return (value == null) ? "" : value
}
///// End Custom Function Section /////