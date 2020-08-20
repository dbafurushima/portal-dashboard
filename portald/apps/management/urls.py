from django.urls import path

from . import views


urlpatterns = [
    path('', views.passwords_safe_view),
    path('passwords-safe', views.passwords_safe_view, name='passwords-safe'),
    path('register-client', views.register_client, name='register-client'),
]
