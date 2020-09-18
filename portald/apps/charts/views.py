from django.shortcuts import render
from .zabbix.api import get_history_from_itemids
from django.http import JsonResponse


def view_chart_line_basic(request):
    data = get_history_from_itemids('31359')
    return render(request, 'pages/charts/basic-line-chart.html', {'data': data})
