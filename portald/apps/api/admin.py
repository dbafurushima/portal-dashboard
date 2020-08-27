from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageList(admin.ModelAdmin):
    list_display = ('ip', 'msg', 'read', 'deleted', 'timestamp')
    search_fields = ('ip', 'msg')
    list_filter = ('ip', 'read', 'deleted')
    list_display_links = ('msg', 'ip')
    list_per_page = 20
