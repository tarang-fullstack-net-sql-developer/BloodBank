var FrgtPssword = (function () {
    var ValidateMessage = function (ResponceStatus) {
        if (ResponceStatus != "") {
            $("#backDrop").toggleClass("hidden");
            $("#MessageModal").show();
        }
    };

    $("#btnNext").on('click', function () {
        $("#backDrop").hide();
        $("#MessageModal").hide();
    });

    return {
        ShowMessage: ValidateMessage,
    };

})();