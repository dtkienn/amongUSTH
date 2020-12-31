$(document).ready(function(){
    var filter = document.getElementById("filter");
    $("#search-filter-btn").click(function(){
        //var close = document.getElementsById("close");
        $("#filter").css("display", "block");
    })
    $("#close").click(function(){
        $("#filter").css("display", "none");
    })
})
