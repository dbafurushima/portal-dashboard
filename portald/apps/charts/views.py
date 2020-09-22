from django.shortcuts import render
from .zabbix.api import Zabbix
from django.conf import settings
from django.http import JsonResponse


def view_chart_line_basic(request):
    zb = Zabbix(settings.ZABBIX_USER, settings.ZABBIX_PASSWORD)
    data = zb.get_history_from_itemids('31359')
    return render(request, 'pages/charts/basic-line-chart.html', {'data': data})
