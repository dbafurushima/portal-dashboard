from django.urls import path

from . import views


urlpatterns = [
    path('', views.clients_view),
    path('clientes', views.clients_view, name='clients'),
    path('list-graph-clients', views.tree_graph_clients_view, name='list-graph-clients'),
    path('zabbix-graph-create', views.zabbix_create_view, name='zabbix-graph-create'),
    path('passwords-safe', views.passwords_safe_view, name='passwords-safe'),
    path('register-client', views.register_client, name='register-client'),
    path('notes', views.kanban_view, name='kanban'),
    path('todolist', views.todolist_view, name='todolist'),
    path('inventory', views.inventory_view, name='inventory'),
    path('proxy_api', views.proxy_api_view, name='proxy_api'),
    path('pre-view-graph-zabbix', views.zabbix_pre_view_graph, name='pre-view-graph-zabbix'),
    path('list-zabbix-graphs', views.zabbix_list_graphs_view, name='list-zabbix-graphs'),
]
