from rest_framework.routers import DefaultRouter

from .views import AccessLogListView

rLogs = DefaultRouter()
rLogs.register(r'access-logs', AccessLogListView, basename='access-log')

urlpatterns = rLogs