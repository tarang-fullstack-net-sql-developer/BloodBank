var CntctUs = (function () {
    var ValidateMessage = function (ResponceStatus) {
        if (ResponceStatus != "") {
            $("#backDrop").toggleClass("hidden");
            $("#MessageModal").show();
        }
    };

    var EleClickEvent = function (tarUrl, obj, status, Message) {
        var eleSrc = (obj).id.split("_")[1];
        window.location = "/" + tarUrl + "?CommentPkId=" + eleSrc + "&Status=" + status + "&Message=" + Message;
    };

    $("#btnNext").on('click', function () {
        $("#backDrop").hide();
        $("#MessageModal").hide();
    });

    return {
        ShowMessage: ValidateMessage,
        EleClickEvent: EleClickEvent
    };

})();