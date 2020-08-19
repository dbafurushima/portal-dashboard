from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_view),
    path('sign-in', views.login_view, name='sign-in'),
    path('sign-out', views.register_view, name='sign-out'),
]
