from functools import wraps
from django.utils.timezone import now

from .models import AccessLog
from .utils.base import get_client_ip

def log_view_action(action_base, object_getter=None, object_meta=None):
  """
  Decorador avanzado para registrar acciones con trazabilidad extendida.

  Params:
  - action_base: Texto base para la acción.
  - object_getter: Función que devuelve string descriptivo (opcional).
  - object_meta: Función que devuelve dict con 'id' y 'type' (opcional).
  """

  def decorator(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
      user = request.user
      if user and user.is_authenticated:
        dynamic_part = ""
        meta = {}

        if object_getter:
          try:
            dynamic_part = " " + str(object_getter(self, request, kwargs))
          except Exception:
            dynamic_part = " (No se pudo obtener el nombre dinámico)"
        
        if object_meta:
          try:
            meta = object_meta(self, request, kwargs) or {}
          except Exception:
            meta = {}
          
        AccessLog.objects.create(
          user=user,
          ip_address=get_client_ip(request),
          timestamp=now(),
          object_id=meta.get("id"),
          object_type=meta.get("type"),
          action=f"{action_base}{dynamic_part}",
          user_agent=request.META.get("HTTP_USER_AGENT", "")
        )
      return func(self, request, *args, **kwargs)
    return wrapper
  return decorator