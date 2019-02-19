$('#OpenModal').on("click", function (e) {
    $("#backDrop").toggleClass("hidden");
    $("#SampleReg-Modal").toggleClass("hidden");

});

$("#btnSubmit").on('click', function () {
    $("#SampleReg-Modal").toggleClass("hidden");
});

$("#btnNext").on('click', function () {
    $("#backDrop").toggleClass("hidden");
    $("#MessageModal").hide();
});

$("#btnClose").on('click', function () {
    $("#backDrop").toggleClass("hidden");
    $("#SampleReg-Modal").toggleClass("hidden");
});

$("#SmpleListStock").dataTable();

var ResStatus = {
    ValidateMessage: function (ResponceStatus) {
        if (ResponceStatus != "") {
            $("#backDrop").toggleClass("hidden");
            $("#MessageModal").show();
        }
    },
    ValidateEditMessage: function (StockData) {
        if (StockData != "") {
            $("#backDrop").toggleClass("hidden");
            $("#SampleEditReg-Modal").toggleClass("hidden");
        }
    },
    SetDropValue: function (SelectedSample) {
        $("#ddlEditSmpleType option:contains(" + SelectedSample + ")").attr('selected', 'selected');
    }
}

$(".InActiveLink").on("click", function () {
    var eleSrc = (this).id.split("_")[1];
    window.location = "/Smp-Dec?SmpPkId=" + eleSrc + "&Status=1&Message=Activated";
});
$(".ActiveLink").on("click", function () {
    var eleSrc = (this).id.split("_")[1];
    window.location = "/Smp-Dec?SmpPkId=" + eleSrc + "&Status=0&Message=De-Activated";
});


$(".ActiveListTab").on("click", function () {
    DisplayList(1);
});
$(".DeActiveListTab").on("click", function () {
    DisplayList(0);
});

function DisplayList(listType)
{
    $.ajax({
        url: '/Stock-list?ListType=' + listType,
        method: 'GET',
        content: 'application/json',
        success: function (responce) {
            var dataArray = [];
            var pkId = [];

            $.each(responce, function (id, item) {
                dataArray.push(item.fields);
                pkId.push(item.pk);
            });

            var columns = [
                { "defaultContent": "", title: 'S.No.' },
                { data: 'Sample', title: 'Blood Type' },
                { data: 'Quantity', title: 'Quantity' },
                { data: 'PurchasedOn', title: 'Purchased On' },
                { data: 'ExpireOn', title: 'Expire On' },
                { data: 'CreatedBy', title: 'Register By' },
                { data: 'isActive', title: 'Status' },
                { "defaultContent": "", title: 'Action' },
            ];

            $("#ListContainer").empty();
            $('#ListContainer').append('<table id="SmpleListStock" class="table table-striped table-bordered table-hover font-small"></table>');
            var sampleDataTable = $("#SmpleListStock").dataTable({
                data: dataArray,
                columns: columns,
            });

            $('#SmpleListStock thead tr:first-child').addClass('bg-primary');

            $('#SmpleListStock td:first-child').each(function (index) {
                var $td = $(this);
                $td.html(new Number(index) + 1);
            });
            $('#SmpleListStock td:last-child').each(function (index) {
                var $td = $(this);
                $td.html('<a href="/Smp-Edit?SmpPkId=' + pkId[index] + '" id="Edit_' + pkId[index] + '" class="fa fa-edit cursor-pointer editSample"></a>&nbsp;<a href="/Smp-Delete?SmpPkId=' + pkId[index] + '" id="Delete_' + pkId[index] + '" class="fa fa-trash-o cursor-pointer deleteSample"></a>');
            });

        },
        error: function (error) {
            console.log(error.responseText);
        }
    });
}


$(".datepicker").datepicker({
    dateFormat: 'yy-mm-dd',
    showButtonPanel: true,
    changeMonth: true,
    changeYear: true,
    minDate: new Date(1980, 10 - 1, 25),
    yearRange: '1980:2030',
    inline: true
});


