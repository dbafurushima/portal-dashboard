from django.urls import path

from . import views


urlpatterns = [
    path('', views.home_view, name='portal-home'),
    path('list-graph', views.view_list_graph, name='list-graph'),
]
