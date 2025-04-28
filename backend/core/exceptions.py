from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    NotAuthenticated, AuthenticationFailed, PermissionDenied,
    NotFound, MethodNotAllowed, Throttled, ValidationError
)
from rest_framework.response import Response

from django.conf import settings

API_VERSION = getattr(settings, 'API_VERSION', '1.0.0')  # Por si no está definida

# Se personaliza el retorno de handle.
def custom_exception_handler(exc, context):
  response = exception_handler(exc, context)

  if response is not None:
    status_code = response.status_code

    # Mensajes personalizados según el tipo de excepción
    exception_messages = {
      NotAuthenticated: "Debes iniciar sesión para acceder a este recurso.",
      AuthenticationFailed: "Correo o contraseña incorrectos.",
      PermissionDenied: "No tienes permiso para realizar esta acción.",
      NotFound: "El recurso solicitado no existe.",
      MethodNotAllowed: "Método HTTP no permitido para esta ruta.",
      Throttled: "Has enviado demasiadas solicitudes. Intenta más tarde.",
      ValidationError: "Hay errores en los datos enviados."
    }
    # Usa el mensaje por tipo de error, o uno por defecto
    message = exception_messages.get(type(exc), "Ha ocurrido un error inesperado.")
    errors = response.data

    # Si hay un solo error con 'detail', lo usamos como mensaje principal
    if isinstance(errors, dict) and "detail" in errors:
      message = errors["detail"]

    response.data = {
      "success": False,
      "version": API_VERSION,
      "status": status_code,
      "message": message,
      "errors": errors or {}
    }
  
  return response