/**
 * Created by Administrator on 2017/5/19 0019.
 * 用于资产首页基本图标的展示
 */
function initBusiness() {
    var options = {
        credits: {
            text: '百度资产',
            href: 'https://www.baidu.com/'
        },
        chart: {
            type: 'column',
            options3d: {
                enabled: true,
                alpha: 10,
                beta: 25,
                depth: 70
            }
        },
        title: {
            text: '3D chart with null values'
        },
        subtitle: {
            text: 'Notice the difference between a 0 value and a null point'
        },
        plotOptions: {
            column: {
                depth: 25
            }
        },
        xAxis: {
            //categories: Highcharts.getOptions().lang.shortMonths
            categories: ['业务线A', '业务线B', '业务线C']
        },
        yAxis: {
            allowDecimals: true,
            title: {
                text: '资产数量'
            }
        },
        series: [{
            name: '服务器',
            data: [2, 3, null]
        }, {
            name: '路由器',
            data: [2, 3, null]
        }, {
            name: '资产',
            data: [2, 3, null]
        }
        ]
    };
    $.ajax({
        url: '/chart-business',
        type: 'GET',
        dataType: 'JSON',
        success: function (arg) {
            if (arg.status) {
                options.xAxis.categories = arg.data.categories;
                options.series = arg.data.series;
                $('#container_business').highcharts(options);
            } else {
                alert(arg.error)
            }
        }
    })
}

function initCategory() {
    var options = {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: 'Browser market shares January, 2015 to May, 2015'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: false
                },
                showInLegend: true
            }
        },
        series: [{
            name: 'Brands',
            colorByPoint: true,
            data: [{
                name: 'IE',
                y: 56.33
            }, {
                name: 'Chrome',
                y: 24.03,
                sliced: true,
                selected: true
            }, {
                name: 'Firefox',
                y: 10.38
            }, {
                name: 'Safari',
                y: 4.77
            }, {
                name: 'Opera',
                y: 0.91
            }, {
                name: 'Propri',
                y: 0.2
            }]
        }]
    };
    $('#container_category').highcharts(options);
}
function initGroup() {
    var options = {
        chart: {
            type: 'bar'
        },
        title: {
            text: 'Historic World Population by Region'
        },
        subtitle: {
            text: 'Source: <a href="https://en.wikipedia.org/wiki/World_population">Wikipedia.org</a>'
        },
        xAxis: {
            categories: ['Africa', 'America', 'Asia', 'Europe', 'Oceania'],
            title: {
                text: null
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Population (millions)',
                align: 'high'
            },
            labels: {
                overflow: 'justify'
            }
        },
        tooltip: {
            valueSuffix: ' millions'
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: true
                }
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            x: -40,
            y: 80,
            floating: true,
            borderWidth: 1,
            backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
            shadow: true
        },
        credits: {
            enabled: false
        },
        series: [{
            name: 'Year 1800',
            data: [107, 31, 635, 203, 2]
        }, {
            name: 'Year 1900',
            data: [133, 156, 947, 408, 6]
        }, {
            name: 'Year 2012',
            data: [1052, 954, 4250, 740, 38]
        }]
    };
    $('#container_group').highcharts(options);
}

function initDynamic() {
    Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });
    (function () {
        var chart = {
            type: 'spline',
            animation: Highcharts.svg, // don't animate in IE < IE 10.
            marginRight: 10,
            events: {
                load: function () {
                    // set up the updating of the chart each second
                    var series = this.series[0];
                    setInterval(function () {
                        var x = (new Date()).getTime(), // current time
                            y = Math.random();
                        series.addPoint([x, y], true, true);
                    }, 1000);
                }
            }
        };
        var title = {
            text: 'Live random data'
        };
        var xAxis = {
            type: 'datetime',
            tickPixelInterval: 150
        };
        var yAxis = {
            title: {
                text: 'Value'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        };
        var tooltip = {
            formatter: function () {
                return '<b>' + this.series.name + '</b><br/>' +
                    Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                    Highcharts.numberFormat(this.y, 2);
            }
        };
        var plotOptions = {
            area: {
                pointStart: 1940,
                marker: {
                    enabled: false,
                    symbol: 'circle',
                    radius: 2,
                    states: {
                        hover: {
                            enabled: true
                        }
                    }
                }
            }
        };
        var legend = {
            enabled: false
        };
        var exporting = {
            enabled: false
        };
        var series = [{
            name: 'Random data',
            data: (function () {
                // generate an array of random data
                var data = [], time = (new Date()).getTime(), i;
                for (i = -19; i <= 0; i += 1) {
                    data.push({
                        x: time + i * 1000,
                        y: Math.random()
                    });
                }
                return data;
            }())
        }];

        var json = {};
        json.chart = chart;
        json.title = title;
        json.tooltip = tooltip;
        json.xAxis = xAxis;
        json.yAxis = yAxis;
        json.legend = legend;
        json.exporting = exporting;
        json.series = series;
        json.plotOptions = plotOptions;


        Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });
        $('#container_dynamic').highcharts(json);

    })();
}