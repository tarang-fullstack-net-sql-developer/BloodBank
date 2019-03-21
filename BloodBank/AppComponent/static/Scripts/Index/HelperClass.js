$("#DropDownMenuToogle").on('click', function () {
    $("#ddlList > ul").toggle();
});


$(".editBldReqLink").on('click', function () {
    $("#backDrop").toggleClass('hidden');
    HelperClass.FetchBloodReqDetail($(this));
    $("#BloodReqEdit-Modal").show();
});

$("#btnClose").on('click', function () {
    $("#backDrop").toggleClass('hidden');
    $("#BloodReqEdit-Modal").hide();
});

$("#btnNext").on('click', function () {
    $("#backDrop").toggleClass('hidden');
    $("#MessageModal").hide();
    document.location.reload();
});

$("#BldReqUpdteForm").on('submit', function (event) {
    var $this = $(this);
    var frmValues = $this.serialize();
    $.ajax({
        type: $this.attr('method'),
        url: $this.attr('action'),
        data: frmValues
    })
    .done(function (result) {
        $("#BloodReqEdit-Modal").hide();
        $("#MessageModal").show()
        $("#MessageContainer").html(result);
    })
    .fail(function (xhr) {
        $("#BloodReqEdit-Modal").hide();
        $("#MessageModal").show()
        $("#MessageContainer").html(xhr.responcetext);
    });
    event.preventDefault();
});

//UpdateBldReqDetail


var HelperClass =
{
    ValidateMessage: function (ResponceStatus) {
        if (ResponceStatus != "") {
            $("#backDrop").toggleClass("hidden");
            $("#MessageModal").show();
        }
    },

    IncrementCount: function (Obj, Count, IncCnt) {
        var EleObject = document.getElementById(Obj);
        var PrevValue = EleObject.innerText;

        var IncSetIntervel = setInterval(function () {
            if (Number(PrevValue) >= Number(Count)) {
                clearInterval(IncSetIntervel);
                EleObject.innerText = Count;
            }
            else {
                PrevValue = Number(PrevValue) + Number(IncCnt);
                EleObject.innerText = PrevValue;
            }
        }, 20);
    },

    MapDisplay: function (EleObject) {
        jQuery('#' + EleObject).vectorMap(
        {
            map: 'world_en',
            backgroundColor: '#383f47',
            borderColor: '#818181',
            borderOpacity: 0.25,
            borderWidth: 1,
            color: '#f4f3f0',
            enableZoom: false,
            hoverColor: '#c9dfaf',
            hoverOpacity: null,
            normalizeFunction: 'linear',
            scaleColors: ['#b6d6ff', '#005ace'],
            selectedColor: '#c9dfaf',
            selectedRegions: ['IN', 'US', 'RU'],
            showTooltip: true,
            onRegionClick: function (element, code, region) {
                var message = 'You clicked '
                    + region
                    + '" which has the code: '
                    + code.toUpperCase();

                alert(message);
            }
        });
    },

    CreateChart: function (canvasObj) {
        var ctx = document.getElementById(canvasObj);
        var myChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ["Jan-Mar", "Apr-Jun", "Jul-Sep", "Oct-Dec"],
                datasets: [{
                    label: '# of Votes',
                    data: [70, 55, 60, 40],
                    backgroundColor: [
                        Color(window.chartColors.red).alpha(0.5).rgbString(),
                        Color(window.chartColors.blue).alpha(0.5).rgbString(),
                        Color(window.chartColors.green).alpha(0.5).rgbString(),
                        Color(window.chartColors.orange).alpha(0.5).rgbString()
                    ],
                    borderColor: [
                        window.chartColors.red,
                        window.chartColors.blue,
                        window.chartColors.green,
                        window.chartColors.orange
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                rotation: 1 * Math.PI,
                circumference: 1 * Math.PI,
                responsive: true,
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Yearly Sales Report (%)'
                }
            }
        });
    },


    FetchBloodReqDetail: function (obj) {
        var eleSrc = $(obj)[0].id.split("_")[1];
        var BldReqDetailUrl = '/BloodReq-Edit?BldreqId=' + eleSrc;

        $.ajax({
            url: BldReqDetailUrl,
            type: 'GET',
            contentType: "application/json; charset=utf-8",
            success: function (result) {
                result = JSON.parse(result);

                $("#BldReqPkIdHid").val(result[0].pk);

                $("#bldReqCode").html(result[0].fields.UniqueCode);
                $("#bldReqOn").html(result[0].fields.CreatedOn);
                $("#bldReqStatus").html(result[0].fields.ReqStatus);
                //$("#BldType").html(result[0].fields.BloodType);
                //$("#bldReqFor").html(result[0].fields.Gender);
                $("#bldQuantity").val(result[0].fields.Quantity);
                $("#bldDelDate").val(result[0].fields.DeliverDate);

                $("#BldType option").prop('selected', false).filter(function () {
                    return $(this).text() == result[0].fields.BloodType;
                }).prop('selected', 'selected');

                $("#bldReqFor option").prop('selected', false).filter(function () {
                    return $(this).text() == result[0].fields.Gender;
                }).prop('selected', 'selected');

                //result[0].fields.Message

            },
            error: function (xhr) {
                console.log(xhr);
            }
        });
    },

    UpdateBldReqDetail: function (obj) {

        var eleSrc = $(obj)[0].id.split("_")[1];

        

        //var BldReqDetailUrl = '/BloodReq-Edit/?BldreqId=' + eleSrc;

        //$.ajax({
        //    url: BldReqDetailUrl,
        //    type: 'POST',
        //    contentType: "application/json; charset=utf-8",
        //    success: function (result) {
        //        result = JSON.parse(result);
        //        $("#MessageContainer"), html(result[0]);
        //    },
        //    error: function (xhr) {
        //        console.log(xhr);
        //    }
        //});
    }
}