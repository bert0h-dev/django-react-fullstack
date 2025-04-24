from rest_framework.permissions import BasePermission

from core.utils.base import BasePermissionOrAdminType

class IsVerified(BasePermission):
  def has_permission(self, request, view):
    user = request.user
    return user and user.is_verified
  
# Users
class CanViewUsers(BasePermissionOrAdminType):
  required_permission = "accounts.view_user"
  
class CanEditUsers(BasePermissionOrAdminType):
  required_permission = "accounts.change_user"