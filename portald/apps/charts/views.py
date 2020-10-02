import requests
import json

from rest_framework import viewsets, generics

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

    for chart in Chart.objects.all():

        obj_data = Data.objects.filter(chart_id=chart.id)

        data_chart = [d.data for d in obj_data]

        print(chart.schema)
        fusion_table = FusionTable(chart.schema, data_chart)
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


class ChartsViewSet(viewsets.ModelViewSet):
    """create, update, list and delete all charts view
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


class ListData(generics.ListAPIView):
    serializer_class = DataSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        queryset = Data.objects.all()
        chartid = self.request.query_params.get('chartid', None)
        print(chartid)
        if chartid is not None:
            queryset = queryset.filter(chart_id=chartid)
        return queryset
