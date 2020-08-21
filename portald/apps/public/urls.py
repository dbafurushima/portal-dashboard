from django.urls import path

from . import views


urlpatterns = [
    path('public-home', views.home_view, name='public-home'),
]
