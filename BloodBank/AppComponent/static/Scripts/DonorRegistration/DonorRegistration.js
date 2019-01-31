var Validation ={
    UserValidte : function(ResStatus){
        if(ResStatus != "")
        {
            $("#MessageModal").removeClass("hidden");
            $("#backdrop").removeClass("hidden");
        }
    }
};


$("#btnNext").on('click', function () {
    $("#MessageModal").addClass("hidden");
    $("#backdrop").addClass("hidden");
});