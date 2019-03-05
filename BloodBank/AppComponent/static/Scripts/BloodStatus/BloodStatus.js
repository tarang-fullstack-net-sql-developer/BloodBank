var BldReqStatus = (function () {
    var ValidateMessage = function (ResponceStatus) {
        if (ResponceStatus != "") {
            $("#backDrop").toggleClass("hidden");
            $("#MessageModal").show();
        }
    };

    var ShowStatusDetail = function (isFound) {
        if (isFound > 0)
            $("#BloodRequestDetailModal").removeClass("hidden")
        else
            $("#BloodRequestDetailModal").addClass("hidden")
    };

    $("#btnNext").on('click', function () {
        $("#backDrop").toggleClass("hidden");
        $("#MessageModal").hide();
    });

    return {
        ShowMessage: ValidateMessage,
        ShowStatusDetail: ShowStatusDetail
    };

})();