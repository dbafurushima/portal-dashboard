from django.urls import path

from . import views


urlpatterns = [
    path('', views.list_clients_view),
    path('clients', views.list_clients_view, name='clients'),
]
