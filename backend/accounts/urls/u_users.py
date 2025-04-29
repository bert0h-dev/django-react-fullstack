from rest_framework.routers import DefaultRouter

from django.urls import path, include

from accounts.views.v_users import UserViewSet

rUsers = DefaultRouter()
rUsers.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(rUsers.urls)),
]