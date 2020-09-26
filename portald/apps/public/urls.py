from django.urls import path

from . import views


urlpatterns = [
    path('public-home', views.home_view, name='public-home'),
    path('set-theme', views.set_theme_view, name='set-theme'),
]
