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
from django.urls import path, include, re_path
from apps.api.views import NotesViewSet, CommentViewSet, InventoryViewSet, HostViewSet, EnvironmentViewSet,\
     ServiceViewSet, InstanceViewSet
from apps.charts.views import ChartsViewSet, DataViewSet, ListData
from rest_framework import routers

charts_router = routers.DefaultRouter()

charts_router.register('charts', ChartsViewSet, basename='charts')
charts_router.register('data', DataViewSet, basename='data')

cmdb_router = routers.DefaultRouter()

cmdb_router.register('environment', EnvironmentViewSet, basename='env')
cmdb_router.register('inventory', InventoryViewSet, basename='inventory')
cmdb_router.register('host', HostViewSet, basename='host')
cmdb_router.register('service', ServiceViewSet, basename='service')
cmdb_router.register('instance', InstanceViewSet, basename='instance')

router = routers.DefaultRouter()

router.register('note', NotesViewSet, basename='Note')
router.register('comment', CommentViewSet, basename='comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('portal/', include('apps.portal.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('view_charts/', include('apps.charts.urls')),

    re_path(r'api_charts/data/filter/', ListData.as_view()),

    path('api/', include(router.urls)),
    path('api/charts/', include(charts_router.urls)),
    path('api/cmdb/', include(cmdb_router.urls)),

    path('', include('apps.management.urls')),
    path('', include('apps.public.urls')),
]
