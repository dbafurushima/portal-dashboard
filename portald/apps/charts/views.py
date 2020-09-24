import requests

from django.shortcuts import render
from .zabbix.api import Zabbix
from django.conf import settings
from .fusioncharts import FusionCharts
from .fusioncharts import FusionTable
from .fusioncharts import TimeSeries


def view_chart_line_basic(request):
    zb = Zabbix(settings.ZABBIX_USER, settings.ZABBIX_PASSWORD)
    data = zb.get_history_from_itemids('31359')
    return render(request, 'pages/charts/basic-line-chart.html', {'data': data})


def fusioncharts_view(request):
    data = requests.get(
        'https://s3.eu-central-1.amazonaws.com/fusion.store/ft/data/area-chart-with-time-axis-data.json').text
    schema = requests.get(
        'https://s3.eu-central-1.amazonaws.com/fusion.store/ft/schema/area-chart-with-time-axis-schema.json').text

    fusionTable = FusionTable(schema, data)
    timeSeries = TimeSeries(fusionTable)

    timeSeries.AddAttribute("chart", """{
                                showLegend: 0
                            }""")

    timeSeries.AddAttribute("caption", """{
                                            text: 'Daily Visitors Count of a Website'
                                        }""")

    timeSeries.AddAttribute("yAxis", """[{
                                            plot: {
                                            value: 'Daily Visitors',
                                            type: 'area'
                                            },
                                        title: 'Daily Visitors (in thousand)'
                                    }]""")

    # Create an object for the chart using the FusionCharts class constructor
    fcChart = FusionCharts("timeseries", "ex1", 700, 450, "chart-1", "json", timeSeries)

    return render(request, 'pages/charts/fusioncharts.html', {'output': fcChart.render()})
