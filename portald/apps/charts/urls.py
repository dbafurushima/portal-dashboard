from django.urls import path

from . import views


urlpatterns = [
    path('chart-line-basic', views.view_chart_line_basic, name='chart-line-basic'),
    path('create-charts', views.create_charts_view, name='create-charts'),
    path('show-charts', views.show_charts_view, name='show-charts'),
    path('render-graph', views.view_get_graph, name='render-graph')
]
