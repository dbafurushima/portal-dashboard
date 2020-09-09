from django.shortcuts import render
from .zabbix.api import get_history_from_itemids


def view_chart_line_basic(request):
    print(get_history_from_itemids('31359'))
    return render(request, 'pages/charts/basic-line-chart.html')
