var BldReqList = (function () {
    var ValidateMessage = function (ResponceStatus) {
        if (ResponceStatus != "") {
            $("#backDrop").toggleClass("hidden");
            $("#MessageModal").show();
        }
    };

    var ApprovedReq = function () {
        var UniqueCode = (this).event.srcElement.id.split("_")[1];
        var BloodApprdUrl = "/BloodReq-List?UniqueCode=" + UniqueCode + "&StatusTo=Approved&ActiveState=1&Message=Approved Successfully !!";
        window.location = BloodApprdUrl;
    };

    var DeclinedReq = function () {
        var UniqueCode = (this).event.srcElement.id.split("_")[1];
        var BloodApprdUrl = "/BloodReq-List?UniqueCode=" + UniqueCode + "&StatusTo=Declined&ActiveState=0&Message=Declined Successfully !!";
        window.location = BloodApprdUrl;
    };

    var bindHtmlControl = function () {
        $("#btnNext").on('click', function () {
            $("#backDrop").toggleClass("hidden");
            $("#MessageModal").hide();
        });

        $("#btnSubmit").on('click', function () {
            $("#loaderIndicator").show();
        });

        $(".approvedLink").on('click', function () {
            ApprovedReq();
        });

        $(".declinedLink").on('click', function () {
            DeclinedReq();
        });
    }

    return {
        ShowMessage: ValidateMessage,
        ControlEvent: bindHtmlControl
    };

})();
