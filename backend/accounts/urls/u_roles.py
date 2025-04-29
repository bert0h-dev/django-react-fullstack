from rest_framework.routers import DefaultRouter

from django.urls import path, include

from accounts.views.v_roles import RoleViewSet

rRoles = DefaultRouter()
rRoles.register(r'roles', RoleViewSet, basename='roles')

urlpatterns = [
    path('', include(rRoles.urls)),
]