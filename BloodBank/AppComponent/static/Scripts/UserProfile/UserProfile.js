var UserProfile = (function () {

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

    var PreviewImage = function (event) {

        var fileName = event.target.files[0].name;
        document.getElementById('ImageName').value = fileName;

        var reader = new FileReader();
        reader.onload = function () {
            var output = document.getElementById('imgProfile');
            output.src = reader.result;
            document.getElementById('UserProfImg').value = output.src;
        }
        reader.readAsDataURL(event.target.files[0]);

    };

    var SetDropDwnData = function (Obj, SelectedSample) {
        $("#" + Obj + " option:contains(" + SelectedSample + ")").attr('selected', 'selected');
    };

    $("#btnNext").on('click', function () {
        $("#backDrop").hide();
        $("#MessageModal").hide();
    });

    return {
        ShowMessage: ValidateMessage,
        EleClickEvent: EleClickEvent,
        PreviewImage: PreviewImage,
        SetDropDwnData: SetDropDwnData
    };

})();