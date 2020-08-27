from django.contrib import admin
from .models import Message, Comment


@admin.register(Message)
class MessageList(admin.ModelAdmin):
    list_display = ('id', 'subject', 'msg', 'read', 'deleted', 'timestamp')
    search_fields = ('subject', 'msg')
    list_filter = ('subject', 'read', 'deleted')
    list_display_links = ('msg', 'subject')
    list_per_page = 20


@admin.register(Comment)
class CommentList(admin.ModelAdmin):
    list_display = ('id', 'origin_message', 'commented_by', 'created_at', 'updated_at')
    search_fields = ('commented_by', 'origin_message')
    list_filter = ('commented_by',)
    list_display_links = ('commented_by',)
    list_per_page = 20
