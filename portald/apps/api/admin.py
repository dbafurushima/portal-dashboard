from django.contrib import admin
from .models import Message, Comment, Host, Application, Inventory, Locator


@admin.register(Message)
class MessageList(admin.ModelAdmin):
    list_display = ('id', 'subject', 'msg', 'read', 'deleted', 'timestamp')
    search_fields = ('subject', 'msg')
    list_filter = ('subject', 'read', 'deleted')
    list_display_links = ('msg', 'subject')
    list_per_page = 20


@admin.register(Comment)
class CommentList(admin.ModelAdmin):
    list_display = ('id', 'message', 'commented_by', 'created_at', 'updated_at')
    search_fields = ('commented_by', 'message')
    list_filter = ('commented_by',)
    list_display_links = ('message',)
    list_per_page = 20


@admin.register(Host)
class HostList(admin.ModelAdmin):
    list_display = ('os_name', 'platform', 'ram', 'cores', 'frequency')
    search_fields = ('platform',)
    list_display_links = ('platform',)
    list_per_page = 20


@admin.register(Locator)
class LocatorList(admin.ModelAdmin):
    list_display = ('locator', 'size', 'speed', 'host')
    search_fields = ('locator',)
    list_display_links = ('locator',)
    list_per_page = 20


@admin.register(Inventory)
class InventoryList(admin.ModelAdmin):
    list_display = ('host', 'equipment')
    search_fields = ('host',)
    list_display_links = ('host',)
    list_per_page = 20
