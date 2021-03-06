from django.contrib import admin
from .models import Chart, Data


@admin.register(Chart)
class ChartList(admin.ModelAdmin):
    list_display = ('id', 'client', 'uid', 'caption', 'yAxis_title', 'from_zabbix', 'number_data', 'itemid')
    search_fields = ('uid',)
    list_display_links = ('uid', 'caption')
    list_per_page = 20


@admin.register(Data)
class DataList(admin.ModelAdmin):
    list_display = ('index', 'value', 'chart')
    search_fields = ('value',)
    list_filter = ('chart',)
    list_display_links = ('value',)
    list_per_page = 50
