from rest_framework.permissions import BasePermission

class IsVerified(BasePermission):
  """
  Permiso que permite el acceso solo a usuarios verificados (is_verified=True).
  """

  def has_permission(self, request, view):
    user = request.user
    return user and user.is_verified