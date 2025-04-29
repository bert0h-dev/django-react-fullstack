from django.urls import path

from accounts.views.v_users import ChangePasswordView
from accounts.views.v_roles import RoleAssignUserView
from accounts.views.v_permissions import PermissionAssignUserView

urlpatterns = [
    path('<int:user_id>/change-password/', ChangePasswordView.as_view(), name='user_change_password'),
    path('<int:user_id>/assign-role/', RoleAssignUserView.as_view(), name='assign_user_role'),
    path('<int:user_id>/assign-permissions/', PermissionAssignUserView.as_view(), name='assign_user_permissions'),
]