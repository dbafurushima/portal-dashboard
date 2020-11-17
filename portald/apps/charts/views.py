import requests
import json
import uuid

from rest_framework import viewsets, generics

from django.shortcuts import render
from django.conf import settings
from django.contrib import messages

from .zabbix.api import Zabbix
from .fusioncharts import FusionCharts
from .fusioncharts import FusionTable
from .fusioncharts import TimeSeries

from .models import Chart, Data
from .serializer import ChartSerializer, DataSerializer

from apps.management.models import Client

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


def make_graph(graph: Chart, theme) -> str:
    obj_data = Data.objects.filter(chart_id=graph.id)

    data_chart = [d.data for d in obj_data]

    fusion_table = FusionTable(graph.schema, data_chart)
    time_series = TimeSeries(fusion_table)

    if theme == 'dark':
        time_series.AddAttribute("chart", "{showLegend: 0, theme: 'candy'}")

    time_series.AddAttribute("caption", "{text: '%s'}" % graph.caption)
    time_series.AddAttribute("subcaption", "{text: '%s'}" % graph.caption)
    time_series.AddAttribute("yAxis", graph.yAxis)

    fusion_chart = FusionCharts(
        "timeseries",
        f"ex{graph.id}",
        "100%",
        450,
        f"chart-{graph.id}", "json",
        time_series
    )

    return fusion_chart.render()


def view_get_graph(request):
    if request.method == 'GET':
        return JsonResponse(
            {
                'code': 200,
                'msg': 'uptime.'
            })

    graph_uid = request.POST.get('graph-uid', None)
    theme = request.POST.get('theme', 'dark')

    if graph_uid is None:
        return JsonResponse(
            {
                'code': 400,
                'msg': 'incorrect request.'
            })

    graph = Chart.objects.get(uid=graph_uid)
    render_graph = make_graph(graph, theme)

    return JsonResponse(
            {
                'code': 200,
                'graph': render_graph,
                'id': graph.id
            })


def __make_uid(name):
    step_uid = str(uuid.uuid4()).split('-')[1]
    step_name = name[:14].replace(' ', '_')

    return '%s_%s' % (step_uid, step_name)


def create_charts_view(request):
    if request.method == 'GET':
        return render(
            request,
            'pages/management/create-charts.html',
            {
                'clients': Client.objects.all()
            }
        )

    if ('caption' in request.POST) and ('cid' in request.POST)\
            and ('schema' in request.POST) and ('subcaption_text' in request.POST)\
            and ('uid' in request.POST) and ('yAxis_format_prefix' in request.POST)\
            and ('yAxis_plot_type' in request.POST) and ('yAxis_plot_value' in request.POST)\
            and ('yAxis_title' in request.POST):

        # TODO :: regex validation uid
        uid = request.POST['uid']
        uid = __make_uid(request.POST['yAxis_title']) if uid == '' else uid

        number_data = int(request.POST.get('number_data', 100)) if 'number_data' in request.POST else 100

        from_zabbix = bool(request.POST.get('from_zabbix', False))

        if from_zabbix:
            itemid = request.POST.get('itemid', None)
            if itemid is None:
                return JsonResponse(
                    {
                        'code': 400,
                        'msg': ('you are trying to create a chart from Zabbix, '
                                'you need to enter the "itemid"')
                    })
        else:
            itemid = None

        data_post = {
            "client": None if not request.POST['cid'] else int(request.POST['cid']),
            "uid": uid,
            "caption": request.POST['caption'],
            "yAxis_plot_value": request.POST['yAxis_plot_value'],
            "yAxis_plot_type": request.POST['yAxis_plot_type'],
            "yAxis_title": request.POST['yAxis_title'],
            "yAxis_format_prefix": request.POST['yAxis_format_prefix'],
            "subcaption": request.POST.get('subcaption_text', ''),
            "schema": request.POST['schema'],
            "itemid": itemid,
            "from_zabbix": from_zabbix,
            "number_data": number_data
        }

        print(data_post)

        request_to_api = json.loads(
                requests.post(
                    f'http://{request.headers.get("host")}/api/charts/charts/',
                    data=data_post,
                    headers={'Authorization': f'Token {settings.USER_API_KEY}'}
                ).text
            )

        if request_to_api.get('id', None):
            messages.success(
                request,
                json.dumps(request_to_api))
        else:
            messages.error(
                request,
                json.dumps(request_to_api))

        return JsonResponse(request_to_api)
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

        time_series.AddAttribute("chart", "{showLegend: 0, theme: 'candy'}")
        time_series.AddAttribute("caption", "{text: '%s'}" % chart.caption)
        time_series.AddAttribute("subcaption", "{text: '%s'}" % chart.caption)
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
        {
            'output': render_charts
        }
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
