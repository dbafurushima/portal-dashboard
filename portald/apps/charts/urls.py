from django.urls import path

from . import views


urlpatterns = [
    path('chart-line-basic', views.view_chart_line_basic, name='chart-line-basic'),
]
