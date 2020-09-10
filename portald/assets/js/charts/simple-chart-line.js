$(function() {
    'use strict';

    function load_chart_data() {
        let token = $('input[name="csrfmiddlewaretoken"]').val();

        let nfd = new FormData();
        nfd.append('csrfmiddlewaretoken', token);

        let raw_url = window.location;
        let url = raw_url.protocol + '//' + raw_url.host + '/charts/chart-line-basic';

        $.ajax({
            url: url,
            method: 'post',
            data: nfd,
            beforeSend: function () {
            },
            success: function(data) {
                if ( data ) {
                    console.log(data)
                }
            },
            error: function () {
                alert('internal error!')
            }
        });
    }

    $(document).ready(function() {
        load_chart_data();
    });

    function create_chart_simple_line(data) {
        var options = {
            series: [{
                data: data
            }],
            chart: {
                id: 'chart2',
                type: 'line',
                height: 230,
                toolbar: {
                    autoSelected: 'pan',
                    show: false
                }
            },
            colors: [],
            stroke: {
                width: 3
            },
            dataLabels: {
                enabled: false
            },
            fill: {
                opacity: 1,
            },
            markers: {
                size: 0
            },
            xaxis: {
                type: 'datetime'
            }
        };

        var chart = new ApexCharts(document.querySelector("#chart-line2"), options);
        chart.render();

        var optionsLine = {
            series: [{
                data: data
            }],
            chart: {
                id: 'chart1',
                height: 130,
                type: 'area',
                brush:{
                target: 'chart2',
                enabled: true
            },
            selection: {
                enabled: true,
                xaxis: {
                    min: new Date('19 Jun 2017').getTime(),
                    max: new Date('14 Aug 2017').getTime()
                }
            },
            },
            colors: ['#008FFB'],
            fill: {
                type: 'gradient',
                gradient: {
                    opacityFrom: 0.91,
                    opacityTo: 0.1,
                }
            },
            xaxis: {
                type: 'datetime',
                tooltip: {
                    enabled: false
                }
            },
            yaxis: {
                tickAmount: 2
            }
        };

        var chartLine = new ApexCharts(document.querySelector("#chart-line"), optionsLine);
        chartLine.render();
    }

});