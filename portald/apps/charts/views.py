import requests

from rest_framework import viewsets

from django.shortcuts import render
from django.conf import settings

from .zabbix.api import Zabbix
from .fusioncharts import FusionCharts
from .fusioncharts import FusionTable
from .fusioncharts import TimeSeries

from .models import Chart, Data
from .serializer import ChartSerializer, DataSerializer

from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAdminUser


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

    for chart in Chart.objects.all():

        fusion_table = FusionTable(schema, data)
        time_series = TimeSeries(fusion_table)

        time_series.AddAttribute("caption", "{text: '%s'}" % chart.caption_text)
        time_series.AddAttribute("subcaption", "{text: 'Grocery'}")
        time_series.AddAttribute("yAxis", chart.yAxis)

        fusion_chart = FusionCharts("timeseries", f"ex{chart.id}", chart.max_width, chart.max_height, 
                                    f"chart-{chart.id}", "json",
                                    time_series)

        render_charts.append({'chart': fusion_chart.render(),
                              'obj_chart': chart})

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


class ChartsViewSet(viewsets.ModelViewSet):
    """show all charts
    """

    queryset = Chart.objects.all()
    serializer_class = ChartSerializer
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]


class DataViewSet(viewsets.ModelViewSet):

    queryset = Data.objects.all()
    serializer_class = DataSerializer
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]
