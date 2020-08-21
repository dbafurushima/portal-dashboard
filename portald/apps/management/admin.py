from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientList(admin.ModelAdmin):
    list_display = ('display_name', 'company_name', 'cnpj', 'city', 'created_at')
    search_fields = ('display_name','company_name', 'cnpj')
    list_filter = ('city',)
    list_display_links = ('display_name',)
    list_per_page = 20

