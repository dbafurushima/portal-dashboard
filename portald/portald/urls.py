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
from apps.api.views import NotesViewSet, CommentViewSet, InventoryViewSet, HostViewSet, EnvironmentViewSet
from apps.charts.views import ChartsViewSet, DataViewSet
from rest_framework import routers

charts_router = routers.DefaultRouter()

charts_router.register('charts', ChartsViewSet, basename='charts')
charts_router.register('data', DataViewSet, basename='data')

router = routers.DefaultRouter()

router.register('note', NotesViewSet, basename='Note')
router.register('comment', CommentViewSet, basename='comment')
router.register('inventory', InventoryViewSet, basename='inventory')
router.register('host', HostViewSet, basename='host')
router.register('env', EnvironmentViewSet, basename='env')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('portal/', include('apps.portal.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('charts/', include('apps.charts.urls')),

    path('api/', include(router.urls)),
    path('api/', include(charts_router.urls)),

    path('', include('apps.management.urls')),
    path('', include('apps.public.urls')),
]
