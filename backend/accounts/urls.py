from django.urls import path

from .views import (
    # Autenticación
    LoginView, LogoutView,

    # Usuarios
    UserListView, RegisterView, 
)

urlpatterns = [
    # Autenticación
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Usuarios
    path('users/', UserListView.as_view(), name='user-list'),
    path('register/', RegisterView.as_view(), name='register'),
]