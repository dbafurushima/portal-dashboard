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

from django.http import JsonResponse


def view_chart_line_basic(request):

    zb = Zabbix(settings.ZABBIX_USER, settings.ZABBIX_PASSWORD)
    data = zb.get_history_from_itemids('31359')

    return render(
        request,
        'pages/charts/basic-line-chart.html',
        {
            'data': data
        })


def create_charts_view(request):
    import uuid

    if request.method == 'GET':
        return render(request, 'public/create-charts.html')

    if ('yAxis_plot_type' in request.POST) and ('yAxis_format_prefix' in request.POST)\
            and ('yAxis_title' in request.POST) and ('client' in request.POST)\
            and ('columns' in request.POST) and ('max_height' in request.POST)\
            and ('caption-text' in request.POST) and ('strftime' in request.POST):

        step_uid = str(uuid.uuid4()).split('-')[1]
        step_name = request.POST['yAxis_title'][:9].replace(' ', '_')

        data_post = {
            "client": int(request.POST['client']),
            "uid": f'{step_uid}_{step_name}',
            "caption_text": request.POST['caption-text'],
            "yAxis_plot_value": "default",
            "yAxis_plot_type": request.POST['yAxis_plot_type'],
            "yAxis_title": request.POST['yAxis_title'],
            "yAxis_format_prefix": request.POST['yAxis_format_prefix'],
            "max_height": request.POST['max_height'],
            "max_width": 700,
            "schema": '[{"name":"Time","type":"date","format":"%s"},{"name":"%s","type":"%s"}]' % \
                (request.POST['strftime'], request.POST['yAxis_title'], "number"),
            "columns": request.POST['columns']
        }

        return JsonResponse(
            json.loads(
                requests.post(
                    f'http://{request.headers.get("host")}/api/charts/charts/',
                    data=data_post,
                    headers={'Authorization': f'Token {settings.USER_API_KEY}'}
                ).text
            ))
    else:
        return JsonResponse(
            {
                'code': 400,
                'msg': 'incorrect request, check if the parameters are correct.'
            })


def show_charts_view(request):
    render_charts = []

    for chart in Chart.objects.all():

        obj_data = Data.objects.filter(chart_id=chart.id)

        data_chart = [d.data for d in obj_data]

        fusion_table = FusionTable(chart.schema, data_chart)
        time_series = TimeSeries(fusion_table)

        time_series.AddAttribute("caption", "{text: '%s'}" % chart.caption_text)
        time_series.AddAttribute("subcaption", "{text: 'Chart'}")
        time_series.AddAttribute("yAxis", chart.yAxis)

        fusion_chart = FusionCharts(
            "timeseries",
            f"ex{chart.id}",
            "100%",
            450,
            f"chart-{chart.id}", "json",
            time_series
        )

        render_charts.append(
            {
                'chart': fusion_chart.render(),
                'obj_chart': chart
            })

    return render(
        request,
        'public/show-charts.html',
        {'output': render_charts}
    )


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
        chartuid = self.request.query_params.get('chartuid', None)

        if chartid is not None:
            queryset = queryset.filter(chart_id=chartid)
        elif chartuid is not None:
            queryset = queryset.filter(chart__uid=chartuid)
        return queryset
