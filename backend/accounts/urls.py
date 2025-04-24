from django.urls import path

from .views import (
    # Autenticación
    LoginView, LogoutView,
    # Usuarios
    UserListView, RegisterView, 
    MeView, UpdateProfileView,
    ChangePasswordView,
    # Roles
    AssignRolesToUserView, UserRolesView,
)

urlpatterns = [
    # Autenticación
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # Usuarios
    path('user/me/', MeView.as_view(), name='me-profile'),
    path('user/me/update/', UpdateProfileView.as_view(), name='me-update'),
    path('user/me/change-password/', ChangePasswordView.as_view(), name='me-change-password'),
    path('user/list/', UserListView.as_view(), name='user-list'),
    path('user/register/', RegisterView.as_view(), name='user-register'),
    # Roles
    path('user/<int:id>/assign-roles/', AssignRolesToUserView.as_view(), name='user-assign-roles'),
    path("user/<int:id>/roles/", UserRolesView.as_view(), name="user-roles"),
]