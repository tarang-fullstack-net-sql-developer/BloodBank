var BldReq = (function () {
    var ValidateMessage = function (ResponceStatus) {
        if (ResponceStatus != "") {

            $("#loaderIndicator").hide();
            $("#backDrop").toggleClass("hidden");

            $(".MessageContainer").html(ResponceStatus);

            $("#DailogBoxModal").show();
        }
    };

    $("#btnNext").on('click', function () {
        $("#backDrop").toggleClass("hidden");
        $("#DailogBoxModal").hide();
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