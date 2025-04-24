from rest_framework.permissions import BasePermission

from .utils.base import BasePermissionOrAdminType

# Grups
class CanViewGroup(BasePermissionOrAdminType):
  required_permission = "auth.view_group"

class CanCreateGroup(BasePermissionOrAdminType):
  required_permission = "auth.add_group"

class CanUpdateGroup(BasePermissionOrAdminType):
  required_permission = "auth.change_group"

class CanDeleteGroup(BasePermissionOrAdminType):
  required_permission = "auth.delete_group"

# Logs
class CanViewLog(BasePermissionOrAdminType):
  required_permission = "core.view_accesslog"