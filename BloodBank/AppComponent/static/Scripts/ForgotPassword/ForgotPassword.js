var FrgtPssword = (function () {
    var ValidateMessage = function (ResponceStatus) {
        if (ResponceStatus != "") {
            $("#backDrop").toggleClass("hidden");
            $("#MessageModal").show();
        }
    };

    $("#cnfPassword").on('keyup', function () {

        var UserPassword = $("#password").val();
        var CurPass = $("#cnfPassword").val();

        if (UserPassword != CurPass) {
            $("#passwordIndicator").text('Not Matched');
            $("#passwordIndicator").css('color', 'red');
            $("#btnChngPassword").prop('disabled', true);
        }
        else {
            $("#passwordIndicator").text('Matched');
            $("#passwordIndicator").css('color', 'green');
            $("#btnChngPassword").prop('disabled', false);
        }

        if (CurPass.trim() == "")
            $("#passwordIndicator").text('');
    });

    $("#btnNext").on('click', function () {
        $("#backDrop").hide();
        $("#MessageModal").hide();
    });

    return {
        ShowMessage: ValidateMessage,
    };

})();