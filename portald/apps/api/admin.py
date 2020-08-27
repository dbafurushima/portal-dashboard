from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageList(admin.ModelAdmin):
    list_display = ('subject', 'msg', 'read', 'deleted', 'timestamp')
    search_fields = ('subject', 'msg')
    list_filter = ('subject', 'read', 'deleted')
    list_display_links = ('msg', 'subject')
    list_per_page = 20
