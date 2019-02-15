$('#OpenModal').on("click", function (e) {
    $("#backDrop").toggleClass("hidden");
    $("#SampleReg-Modal").toggleClass("hidden");

});

$("#btnSubmit").on('click', function () {
    $("#SampleReg-Modal").toggleClass("hidden");
});

$("#btnNext").on('click', function () {
    $("#backDrop").toggleClass("hidden");
    $("#MessageModal").hide();
});

$("#btnClose").on('click', function () {
    $("#backDrop").toggleClass("hidden");
    $("#SampleReg-Modal").toggleClass("hidden");
});

$("#SmpleListStock").dataTable();

var ResStatus = {
    ValidateMessage: function (ResponceStatus) {
        if (ResponceStatus != "") {
            $("#backDrop").toggleClass("hidden");
            $("#MessageModal").show();
        }
    },
    ValidateEditMessage: function (StockData) {
        if (StockData != "") {
            $("#backDrop").toggleClass("hidden");
            $("#SampleEditReg-Modal").toggleClass("hidden");
        }
    },
    SetDropValue: function (SelectedSample) {
        $("#ddlEditSmpleType option:contains(" + SelectedSample + ")").attr('selected', 'selected');
    }
}

$(".editSample").on("click", function () {
    var eleSrc = (this).id.split("_")[1];
    window.location = "/Smp-Edit?SmpPkId=" + eleSrc;
});

$(".deleteSample").on("click", function () {
    var eleSrc = (this).id.split("_")[1];
    window.location = "/Smp-Delete?SmpPkId=" + eleSrc;
});


$(".InActiveLink").on("click", function () {
    var eleSrc = (this).id.split("_")[1];
    window.location = "/Smp-Dec?SmpPkId=" + eleSrc + "&Status=1&Message=Activated";
});
$(".ActiveLink").on("click", function () {
    var eleSrc = (this).id.split("_")[1];
    window.location = "/Smp-Dec?SmpPkId=" + eleSrc + "&Status=0&Message=De-Activated";
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


