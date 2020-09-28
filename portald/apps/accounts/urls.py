from django.urls import path, include, re_path

from . import views

urlpatterns = [
    path('', views.login_view),
    path('sign-in', views.login_view, name='login'),
    path('totp-sign-in', views.totp_view, name='totp-sign-in'),
    path('logout', views.logout_view, name='logout'),
    re_path(r'totp/create/$', views.TOTPCreateView.as_view(), name='totp-create'),
    path('totp/login', views.totp_post_view, name='totp-login'),
]
