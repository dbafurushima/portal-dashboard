from django.urls import path

from . import views

urlpatterns = [
    path('', views.status_route),
    path('status', views.status_route, name='api-status'),
]
