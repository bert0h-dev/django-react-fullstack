from rest_framework.permissions import BasePermission

def get_client_ip(request):
  """
  Obtiene la dirección IP del cliente desde la solicitud.
  """
  
  x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
  if x_forwarded_for:
    ip = x_forwarded_for.split(',')[0]
  else:
    ip = request.META.get('REMOTE_ADDR')
  return ip

class BasePermissionOrAdminType(BasePermission):
  """
  Valida que el usuario tenga permisos específicos o sea tipo admin.
  """

  required_permission = None
  
  def has_permission(self, request, view):
    user = request.user
    return (
      user.is_authenticated and (
        (self.required_permission and user.has_perm(self.required_permission)) or
        getattr(user, "user_type", None) == "admin"
      )
    )