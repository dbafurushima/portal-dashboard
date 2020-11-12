from django.urls import path

from . import views


urlpatterns = [
    path('', views.clients_view),
    path('clients', views.clients_view, name='clients'),
    path('list-graph-clients', views.tree_graph_clients_view, name='list-graph-clients'),
    path('zabbix-graph-create', views.zabbix_create_view, name='zabbix-graph-create'),
    path('passwords-safe', views.passwords_safe_view, name='passwords-safe'),
    path('register-client', views.register_client, name='register-client'),
    path('kanban', views.kanban_view, name='kanban'),
    path('todolist', views.todolist_view, name='todolist'),
    path('inventory', views.inventory_view, name='inventory'),
    path('proxy_api', views.proxy_api_view, name='proxy_api'),
]
