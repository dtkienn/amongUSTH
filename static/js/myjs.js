$(document).ready(function(){
    $("#retry-btn").click(function(){
        $("#login-noti").css("display", "none");
    });
    //$("#change-password").click(function(){
        //$("#user-password").append("<div class="change-password-box">aaaaaaaa</div>");
    //});
    var filterTitle = document.getElementById("filter-type");
    if (filterTitle.innerHTML.includes("Any") == true){
        $("#filter-select").css("background-color", "black");
    }
});
