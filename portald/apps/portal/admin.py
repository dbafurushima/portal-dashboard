from django.contrib import admin
from .models import AppNote, Topic


@admin.register(AppNote)
class AppNoteList(admin.ModelAdmin):
    list_display = ('id', 'title', 'display', 'favorite', 'updated_at')
    search_fields = ('title', )
    list_filter = ('favorite',)
    list_display_links = ('title',)
    list_per_page = 20


@admin.register(Topic)
class TopicList(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('name',)
    list_display_links = ('name',)
    list_per_page = 20
