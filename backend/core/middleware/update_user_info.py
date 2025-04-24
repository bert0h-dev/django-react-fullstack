from django.utils.timezone import now
from core.utils import get_client_ip
import logging

logger = logging.getLogger(__name__)

class UpdateUserInfoMiddleware:
  """
  Middleware que actualiza `last_activity` y `last_ip` del usuario autenticado en cada request.
  """

  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    response = self.get_response(request)

    # 🚫 Ignorar rutas que no son API
    if not request.path.startswith("/api/"):
      return response

    try:
      if request.user.is_authenticated:
        user = request.user
        ip = get_client_ip(request)
        updated = False

        # Actualiza la última actividad del usuario
        user.last_activity = now()
        updated = True

        # Actualiza la IP del usuario si ha cambiado
        if ip and ip != user.last_ip:
          user.last_ip = ip
          updated = True

        if updated:
          user.save(update_fields=['last_activity', 'last_ip'])
    except Exception as e:
      logger.warning(f"[Middleware] No se pudo actualizar la informacion default del usuario: {e}")

    return response