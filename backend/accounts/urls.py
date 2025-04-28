from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import LoginView, LogoutView, RefreshTokenView, UserViewSet

rUsers = DefaultRouter()
rUsers.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
]

# Se agregan las rutas de los usuarios
urlpatterns += rUsers.urls