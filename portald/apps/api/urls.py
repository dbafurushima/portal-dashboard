from django.urls import path

from . import views

urlpatterns = [
    path('zabbix', views.status, name='zabbix'),
]
