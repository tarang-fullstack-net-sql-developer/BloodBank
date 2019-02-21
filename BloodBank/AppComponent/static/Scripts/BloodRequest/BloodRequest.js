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

    return {
        ShowMessage: ValidateMessage,
    };

})();