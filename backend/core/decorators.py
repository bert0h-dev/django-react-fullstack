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

  def decorator(view_func):
    @wraps(view_func)
    def _wrapped_view(self, request, *args, **kwargs):
      response = view_func(self, request, *args, **kwargs)
      
      try:
        user = request.user if request.user.is_authenticated else None
        method = request.method
        path = request.path
        status_code = response.status_code
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        message = response.data.get('message') if hasattr(response, 'data') and isinstance(response.data, dict) else ''

        dynamic_part = ""
        meta = {}
        
        if object_getter:
          try:
            dynamic_part = ": " + str(object_getter(self, request, kwargs))
          except Exception:
            dynamic_part = ": (Not able to get dynamic name)"
        
        if object_meta:
          try:
            meta = object_meta(self, request, kwargs) or {}
          except Exception:
            meta = {}
        
        AccessLog.objects.create(
          user=user,
          method=method,
          path=path,
          action=f"{action_base}{dynamic_part}" or f"{view_func.__name__}{dynamic_part}",
          status_code=status_code,
          message=message,
          ip_address=ip_address,
          user_agent=user_agent,
          object_id=meta.get("id"),
          object_type=meta.get("type"),
          created_at=now(),
        )
      except Exception as e:
        # No fallamos la request si falla el log, solo registramos el error en consola
        print(f"[AccessLog Error] No se pudo registrar el log: {str(e)}")
        
      return response
    return _wrapped_view
  return decorator