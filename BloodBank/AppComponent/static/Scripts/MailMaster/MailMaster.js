var MailMaster = (function () {
    var ValidateMessage = function (ResponceStatus) {
        if (ResponceStatus != "") {
            $("#backDrop").toggleClass("hidden");
            $("#MessageModal").show();
        }
    };

    var EleClickEvent = function (eleSrc) {
        var listElementCont = $(eleSrc).parent().parent().find("p");
        var inputText = $(eleSrc).parent().parent().find("input[type='text']");
        var HiddenEle = $(eleSrc).parent().parent().find("input[type='hidden']");

        //Setting to Hidden Value
        HiddenEle.val(HiddenEle.val() + inputText.val() + ";")

        $(listElementCont).append('<span class="badge MailList GlbFont">' + inputText.val() + '<i class="fa fa-times removeMailId cursor-pointer" aria-hidden="true" onclick="removeMailId(this);"></i></span><span id="' + inputText.val() + '" class="MailListdivider">&nbsp;</span>').removeClass('hidden');
        $(inputText).val("").focus();
    };

    removeMailId = function (obj) {
        var ParentELe = $(obj).parent();
        $("#" + ParentELe.text()).remove();
        //Removing from Hidden Feild
        $(obj).parent().parent().parent().find("input[type='hidden']").val().replace(ParentELe.text() + ';', "");
        ParentELe.remove();
    }

    $("#btnNext").on('click', function () {
        $("#backDrop").hide();
        $("#MessageModal").hide();
    });

    $(".mailAdvBtn").on('click', function () {
        var eleSrc = window.event.srcElement;
        EleClickEvent(eleSrc);
    });

    $("#btnSend").on('click', function () {

        $("#MailModeHid").val("1");

        $("#messageHid").val($(".Editor-editor").html());
        $("#mailSentFrm").submit();
        $("#btnNext").focus();
    });

    $("#btnDraft").on('click', function () {
        $("#MailModeHid").val("2");
        $("#messageHid").val($(".Editor-editor").html());
        $("#mailSentFrm").submit();
        $("#btnNext").focus();
    });

    $(".MailItem").on('click', function () {
        $(".MailItem").removeClass("nav-active");

        var CurEle = window.event.srcElement;
        $(CurEle).addClass("nav-active");
        var ShowTab = CurEle.attributes["data-target"].nodeValue;
        $(".MailDataTab").addClass("hidden");
        $(ShowTab).removeClass("hidden");

    });


    $(".MailListDataItems").on('click', function () {
        var MailCurId = $(this).parent()[0].attributes["data-MailId"].value;
        var MailMessage = $(this).parent()[0].attributes["data-Mailtype"].value;

        var MailMessageUrl = "/Mail-Message?MailPkId=" + MailCurId + "&MailType=" + MailMessage
        $.ajax({
            url: MailMessageUrl,
            type: 'GET',
            contentType: "application/json; charset=utf-8",
            success: function (result) {

                result = JSON.parse(result); //[0].fields.From

                $("#MailBody").html(result[0].fields.Message);

                if (new Number(MailMessage) == 1 || new Number(MailMessage) == 3)
                    $("#MailHeader").html("To : " + result[0].fields.SentTo);
                else
                    $("#MailHeader").html("From : " + result[0].fields.From);


                $("#MailTimer").html(result[0].fields.CreatedOn);
                $("#backDrop").toggleClass("hidden");
                $("#MailViewModal").show();
            },
            error: function (xhr) {
                console.log(xhr);
            }
        });
    });

    $("#btnClose").on('click', function () {
        $("#backDrop").hide();
        $("#MailViewModal").hide();
    });

    //$('.content').richText();
    $("#txtEditor").Editor();

    return {
        ShowMessage: ValidateMessage,
    };

})();