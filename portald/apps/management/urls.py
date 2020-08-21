from django.urls import path

from . import views


urlpatterns = [
    path('', views.clients_view),
    path('clients', views.clients_view, name='clients'),
    path('passwords-safe', views.passwords_safe_view, name='passwords-safe'),
    path('register-client', views.register_client, name='register-client'),
]
