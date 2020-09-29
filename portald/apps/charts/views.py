import requests

from django.shortcuts import render
from .zabbix.api import Zabbix
from django.conf import settings
from .fusioncharts import FusionCharts
from .fusioncharts import FusionTable
from .fusioncharts import TimeSeries
from .models import Chart


def view_chart_line_basic(request):
    zb = Zabbix(settings.ZABBIX_USER, settings.ZABBIX_PASSWORD)
    data = zb.get_history_from_itemids('31359')

    return render(request, 'pages/charts/basic-line-chart.html', {'data': data})


def create_charts_view(request):
    return render(request, 'public/create-charts.html')


def show_charts_view(request):
    render_charts = []

    data = requests.get(
        'https://s3.eu-central-1.amazonaws.com/fusion.store/ft/data/area-chart-with-time-axis-data.json').text
    schema = requests.get(
        'https://s3.eu-central-1.amazonaws.com/fusion.store/ft/schema/area-chart-with-time-axis-schema.json').text

    for chart_obj in Chart.objects.all():
        fusion_table = FusionTable(schema, data)
        time_series = TimeSeries(fusion_table)

        time_series.AddAttribute("caption", "{text: '%s'}" % chart_obj.caption_text)
        time_series.AddAttribute("subcaption", "{text: 'Grocery'}")
        time_series.AddAttribute("yAxis", ("[{"
                                           "plot: {"
                                           "value: '%s',"
                                           "type: '%s'"
                                           "},"
                                           "format: {"
                                           "prefix: '%s'"
                                           "},"
                                           "title: '%s'"
                                           "}]" % (chart_obj.yAxis_plot_value, chart_obj.yAxis_plot_type,
                                                   chart_obj.yAxis_format_prefix, chart_obj.yAxis_title)))

        tmp_chart = FusionCharts("timeseries", f'ex{chart_obj.id}', 700, 450, f"chart-{chart_obj.id}", "json",
                                 time_series)

        render_charts.append({'chart': tmp_chart.render(),
                              'chart_raw': chart_obj})

    return render(request, 'public/show-charts.html',
                  {'output': render_charts})


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
