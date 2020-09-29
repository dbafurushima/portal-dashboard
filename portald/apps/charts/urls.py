from django.urls import path

from . import views


urlpatterns = [
    path('chart-line-basic', views.view_chart_line_basic, name='chart-line-basic'),
    path('fusioncharts', views.fusioncharts_view, name='fusioncharts'),
    path('create-charts', views.create_charts_view, name='create-charts'),
    path('show-charts', views.show_charts_view, name='show-charts'),
]
