from rest_framework.routers import DefaultRouter

from django.urls import path, include

from core.views.v_logs import AccessLogListView, AccessLogExportView

rLogs = DefaultRouter()
rLogs.register(r'logs', AccessLogListView, basename='log')

urlpatterns = [
  path('', include(rLogs.urls)),
  path('logs/export/', AccessLogExportView.as_view(), name='log-export'),
]
