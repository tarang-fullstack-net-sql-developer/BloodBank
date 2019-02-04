$('#OpenModal').on("click", function (e) {
    $("#backDrop").toggleClass("hidden");
    $("#dnrReg-Modal").toggleClass("hidden");

});

$("#btnSubmit").on('click', function () {
    $("#dnrReg-Modal").toggleClass("hidden");
});

$("#dnrListTab").dataTable();

$(".closeModal").on('click', function () {
    var CurModal = window.event.srcElement.attributes["data-target"].value;
    $(CurModal).toggleClass("hidden");
    $("#backDrop").toggleClass("hidden");
});

var ResStatus = {
    ValidateMessage: function (ResponceStatus) {
        if (ResponceStatus != "") {
            $("#backDrop").toggleClass("hidden");
            $("#MessageModal").show();
        }
    },
    SetDropValue: function (objId, SelectedSample) {
        $("#" + objId + " option:contains(" + SelectedSample + ")").attr('selected', 'selected');
    },
    DisplayEditForm: function (DonorData) {
        if (DonorData != "") {
            $("#backDrop").toggleClass("hidden");
            $("#dnrEditReg-Modal").toggleClass("hidden");
        }
    },
    CloseModal: function (obj) {
        $("#backDrop").toggleClass("hidden");
        $("#dnrEditReg-Modal").toggleClass("hidden");
    }
}

$(".editUser").on("click", function () {
    var eleSrc = (this).id.split("_")[1];
    window.location = "/donor-edit?DonorPkId=" + eleSrc;
});

$(".deleteUser").on("click", function () {
    var eleSrc = (this).id.split("_")[1];
    window.location = "/donor-delete?DonorPkId=" + eleSrc;
});


$(".InActiveLink").on("click", function () {
    var eleSrc = (this).id.split("_")[1];
    window.location = "/Deac-Donor?DonorPkId=" + eleSrc + "&Status=1&Message=Activated";
});
$(".ActiveLink").on("click", function () {
    var eleSrc = (this).id.split("_")[1];
    window.location = "/Deac-Donor?DonorPkId=" + eleSrc + "&Status=0&Message=De-Activated";
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

$(document).on("contextmenu", function (event) { event.preventDefault(); });