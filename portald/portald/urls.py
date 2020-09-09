"""portald URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.api.views import MessageViewSet, CommentViewSet, ApplicationViewSet, InventoryViewSet, HostViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('message', MessageViewSet, basename='message')
router.register('comment', CommentViewSet, basename='comment')
router.register('application', ApplicationViewSet, basename='application')
router.register('inventory', InventoryViewSet, basename='inventory')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('portal/', include('apps.portal.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('charts/', include('apps.charts.urls')),
    path('api/', include(router.urls)),
    path('api/', include('apps.api.urls')),
    path('', include('apps.management.urls')),
    path('', include('apps.public.urls')),
]
