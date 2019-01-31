var boxShadow = "";

//User ID TextBox
$("#userTxt").on('mouseenter', function () {
    boxShadow = $(this).css('box-shadow');
    $(this).css('box-shadow', '');
}).on('mouseout', function () {
    $(this).css('box-shadow', boxShadow);
}).on('focus', function () {
    boxShadow = $(this).css('box-shadow');
    $(this).css('box-shadow', '');
}).on('blur', function () {
    $(this).css('box-shadow', boxShadow);
});

//User Password
$("#userPass").on('mouseenter', function () {
    boxShadow = $(this).css('box-shadow');
    $(this).css('box-shadow', '');
}).on('mouseout', function () {
    $(this).css('box-shadow', boxShadow);
}).on('focus', function () {
    boxShadow = $(this).css('box-shadow');
    $(this).css('box-shadow', '');
}).on('blur', function () {
    $(this).css('box-shadow', boxShadow);
});

//LoginButton
$("#btnLogin").on('mouseenter', function () {
    $(this).css('background-color', '#ace6cd').parent().css('background-color', '#ace6cd');
}).on('mouseout', function () {
    $(this).css('background-color', '#66e6af').parent().css('background-color', '#66e6af');
}).on('focus', function () {
    $(this).css('background-color', '#ace6cd').parent().css('background-color', '#ace6cd');
}).on('blur', function () {
    $(this).css('background-color', '#66e6af').parent().css('background-color', '#66e6af');
});

//SignUpBtn
$("#btnSignUp").on('mouseenter', function () {
    $(this).css('background-color', '#bdb6b6').parent().css('background-color', '#bdb6b6');
}).on('mouseout', function () {
    $(this).css('background-color', '#808080').parent().css('background-color', '#808080');
}).on('focus', function () {
    $(this).css('background-color', '#bdb6b6').parent().css('background-color', '#bdb6b6');
}).on('blur', function () {
    $(this).css('background-color', '#808080').parent().css('background-color', '#808080');
}).on('click', function () {
    $("#loginCont").removeClass('jackInTheBox').addClass('hinge');
    setTimeout(function () {
        var CurrLoc = location.pathname.split('/');
        console.log(CurrLoc);
        CurrLoc[CurrLoc.length - 2] = "SignUp_User";
        var NewLoc = CurrLoc.join('/');
        window.location = NewLoc;
    }, 1000);
});

var Validation ={
    UserValidte : function(LonginStatus){
        if(LonginStatus != "")
        {
            $("#MessageModal").modal("show");
        }
    }
};

$("#btnNext").on('click', function () {
    $("#MessageModal").modal("hide");
});