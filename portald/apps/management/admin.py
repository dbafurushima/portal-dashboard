from django.contrib import admin
from .models import Client, Notification


@admin.register(Client)
class ClientList(admin.ModelAdmin):
    list_display = ('display_name', 'company_name', 'cnpj', 'city', 'created_at')
    search_fields = ('display_name','company_name', 'cnpj')
    list_filter = ('city',)
    list_display_links = ('display_name',)
    list_per_page = 20


@admin.register(Notification)
class NotificationList(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at')
    search_fields = ('message', 'user')
    list_filter = ('user',)
    list_display_links = ('message',)
    list_per_page = 20
