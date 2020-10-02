from django.contrib import admin
from .models import Chart, Data


@admin.register(Chart)
class ChartList(admin.ModelAdmin):
    list_display = ('id', 'client', 'uid', 'caption_text', 'yAxis_title')
    search_fields = ('uid',)
    list_display_links = ('uid', 'caption_text')
    list_per_page = 20


@admin.register(Data)
class DataList(admin.ModelAdmin):
    list_display = ('index', 'value', 'chart')
    search_fields = ('value',)
    list_filter = ('chart',)
    list_display_links = ('value',)
    list_per_page = 50
