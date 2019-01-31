$("#DropDownMenuToogle").on('click',function(){
        $("#ddlList > ul").toggle();
});

var HelperClass = 
{
    IncrementCount : function(Obj, Count, IncCnt){
        var EleObject = document.getElementById(Obj);
        var PrevValue = EleObject.innerText;
               
        var IncSetIntervel = setInterval(function(){
            if(Number(PrevValue) >= Number(Count))
            {
                clearInterval(IncSetIntervel);
                EleObject.innerText = Count;
            }
            else
            {   
                PrevValue = Number(PrevValue) + Number(IncCnt);
                EleObject.innerText = PrevValue;
            }
        }, 20);
    },

    MapDisplay : function(EleObject) { 
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
            selectedRegions: ['IN','US','RU'],
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

    CreateChart : function(canvasObj)
    {
        var ctx = document.getElementById(canvasObj);
        var myChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ["Jan-Mar","Apr-Jun","Jul-Sep","Oct-Dec"],
                datasets: [{
                    label: '# of Votes',
                    data: [70,55,60,40],
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
    }
}