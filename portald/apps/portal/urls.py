from django.urls import path

from . import views


urlpatterns = [
    path('', views.home_view, name='portal-home'),
    path('list-graph', views.view_list_graph, name='list-graph'),
    path('create-topic', views.route_create_topic, name='route-create-topic'),
    path('create-note', views.route_create_note, name='route-create-note'),
    path('fav-note', views.route_fav_note, name='route-fav-note'),
    path('remove-note', views.route_delete_note, name='remove-note')
]
