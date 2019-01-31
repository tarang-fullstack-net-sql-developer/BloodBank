$('#OpenModal').on("click", function (e) {
    $("#backDrop").toggleClass("hidden");
    $("#UserReg-Modal").toggleClass("hidden");

});

$("#btnSubmit").on('click', function () {
    $("#UserReg-Modal").toggleClass("hidden");
});

$("#btnNext").on('click', function () {
    $("#backDrop").toggleClass("hidden");
    $("#MessageModal").hide();
});

$("#btnClose").on('click', function () {
    $("#backDrop").toggleClass("hidden");
    $("#UserReg-Modal").toggleClass("hidden");
});

$("#userTab").dataTable();

var ResStatus = {
    ValidateMessage: function (ResponceStatus) {
        if (ResponceStatus != "") {
            $("#backDrop").toggleClass("hidden");
            $("#MessageModal").show();
        }
    }
}

$(".deacUser").on("click", function () {
    var eleSrc = (this).id.split("_")[1];
    window.location = "/deac-user?UserPkId=" + eleSrc;
});

$(".deleteUser").on("click", function () {
    var eleSrc = (this).id.split("_")[1];
    window.location = "/delete-user?UserPkId=" + eleSrc;
});


$(".InActiveLink").on("click", function () {
    var eleSrc = (this).id.split("_")[1];
    window.location = "/deac-user?UserPkId=" + eleSrc + "&Status=1&Message=Activated";
});
$(".ActiveLink").on("click", function () {
    var eleSrc = (this).id.split("_")[1];
    window.location = "/deac-user?UserPkId=" + eleSrc + "&Status=0&Message=De-Activated";
});


$(".datepicker").datepicker({
    dateFormat: 'yy-mm-dd',
    showButtonPanel: true,
    changeMonth: true,
    changeYear: true,
    minDate: new Date(1980, 10 - 1, 25),
    yearRange: '1980:2030',
    inline: true
});