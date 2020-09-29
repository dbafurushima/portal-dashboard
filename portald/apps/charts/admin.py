from django.contrib import admin
from .models import Chart


@admin.register(Chart)
class ChartList(admin.ModelAdmin):
    list_display = ('id', 'uid', 'caption_text', 'yAxis_title')
    search_fields = ('uid',)
    list_display_links = ('uid', 'caption_text')
    list_per_page = 20
