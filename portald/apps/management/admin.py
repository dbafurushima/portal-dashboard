from django.contrib import admin
from .models import Client, Notification, PasswordSafe, Host, Locator, Inventory, EnterpriseUser


@admin.register(Client)
class ClientList(admin.ModelAdmin):
    list_display = ('id', 'display_name', 'company_name', 'cnpj', 'city', 'created_at')
    search_fields = ('display_name', 'company_name', 'cnpj')
    list_filter = ('city',)
    list_display_links = ('display_name',)
    list_per_page = 20


@admin.register(EnterpriseUser)
class EnterpriseUserList(admin.ModelAdmin):
    list_display = ('user', 'enterprise')
    search_fields = ('user', 'enterprise')
    list_filter = ('enterprise',)
    list_display_links = ('user',)
    list_per_page = 20


@admin.register(Notification)
class NotificationList(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at')
    search_fields = ('message', 'user')
    list_filter = ('user',)
    list_display_links = ('message',)
    list_per_page = 20


@admin.register(PasswordSafe)
class PasswordSafeList(admin.ModelAdmin):
    list_display = ('user', 'password')
    search_fields = ('user',)
    list_display_links = ('user',)
    list_per_page = 20


@admin.register(Host)
class HostList(admin.ModelAdmin):
    list_display = ('os_name', 'platform', 'ram', 'physical_cores', 'current_frequency')
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
