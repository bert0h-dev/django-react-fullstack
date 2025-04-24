from django.utils.timezone import now

from core.models import AccessLog
from .base import get_client_ip

def log_action(request, action, description=None):
  """
  Registra una accion en el modelo AccessLog desde cualquier vista.
  """
  user = getattr(request, 'user', None)

  if not user or not user.is_authenticated:
    return
  
  AccessLog.objects.create(
    user=user,
    ip_address=get_client_ip(request),
    timestamp=now(),
    action=action,
    description=description,
  )