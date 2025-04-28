from rest_framework.permissions import BasePermission

# Permiso que permite acceso sólo a usuarios administradores o staff.
class IsAdminOrStaff(BasePermission):
  def has_permission(self, request, view):
    return bool(
      request.user 
      and request.user.is_authenticated 
      and (request.user.is_staff or request.user.user_type == 'admin')
    )