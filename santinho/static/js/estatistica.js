$(function() {
    var ticks = [];
    for (var i = 1; i <=60; i++) {
        if (i < 10) {
            i = "0" + i;
        }
        ticks.push(i);
    }
    var plot1 = $.jqplot (
            'quantidades',
            [quantidades],
            {
                seriesDefaults: {
                        showMarker:false,
                        pointLabels: { show:true }
                      },
                axes: {
                    xaxis: {
                        label: "Números",
                        renderer: $.jqplot.CategoryAxisRenderer,
                        labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                        tickOptions:{
                            formatString:'porra%'
                        }
                    }
                },
                highlighter: {
                  show: false
                },
                cursor: {
                  show: true,
                  tooltipLocation:'sw'
                }
            }
    );
//    $.plot($("#quantidades"),
//        [
//            {label: "Números", data: quantidade }
//        ],
//        {
//            series: {
//                bars: { show: true }
//            },
//            xaxis: {
//                ticks: ticks
//            }
//        }
//    );
});