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

    //$(".MailItem").on('click', function () {
    //    var CurEle = window.event.srcElement;
    //    var TtlItem = $(".MailItem");
    //    $.each(TtlItem, function (index, obj) {
    //        $(obj).removeClass("MailItem-active");
    //    });
    //    $(CurEle).toggleClass("MailItem-active");
    //});

    $(".mailAdvBtn").on('click', function () {
        var eleSrc = window.event.srcElement;
        EleClickEvent(eleSrc);
    });

    $("#btnSend").on('click', function () {
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

    //$('.content').richText();
    $("#txtEditor").Editor();

    return {
        ShowMessage: ValidateMessage,
    };

})();