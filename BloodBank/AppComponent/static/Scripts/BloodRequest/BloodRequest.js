var BldReq = (function () {
    var ValidateMessage = function (ResponceStatus) {
        if (ResponceStatus != "") {
            $("#backDrop").toggleClass("hidden");
            $("#MessageModal").show();
        }
    };

    $("#btnNext").on('click', function () {
        $("#backDrop").toggleClass("hidden");
        $("#MessageModal").hide();
    });

    $("#btnSubmit").on('click', function () {
        $("#loaderIndicator").show();
    });

    $(".datepicker").datepicker({
        dateFormat: 'yy-mm-dd',
        showButtonPanel: true,
        changeMonth: false,
        changeYear: false,
        minDate: 0,
        numberOfMonths: 2,
        inline: true
    });

    return {
        ShowMessage: ValidateMessage,
    };

})();