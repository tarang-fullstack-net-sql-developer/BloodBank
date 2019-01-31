var ChangePassword = (function () {


    $("#oldPassword").on("keyup", function () {
        EleKeyEvent($(this));
    });


    var ValidateMessage = function (ResponceStatus) {
        if (ResponceStatus != "") {
            $("#backDrop").toggleClass("hidden");
            $("#MessageModal").show();
        }
    };

    var EleKeyEvent = function (obj) {

        var UserPassword = $(obj).val();
        var CurPass = window.atob($("#UserCurPasswordHid").val());

        if (UserPassword != CurPass) {
            $(".newpassword").prop('disabled', true);
            $("#passwordIndicator").text('Wrong Password');
            $("#passwordIndicator").css('color', 'red');
        }
        else {
            $(".newpassword").prop('disabled', false);
            $("#passwordIndicator").text('Validated');
            $("#passwordIndicator").css('color', 'green');
        }

        if (UserPassword.trim() == "")
            $("#passwordIndicator").text('');
    };

    $("#btnNext").on('click', function () {
        $("#backDrop").hide();
        $("#MessageModal").hide();
    });

    return {
        ShowMessage: ValidateMessage,
        EleKeyEvent: EleKeyEvent
    };

})();