from rest_framework.response import Response
from django.conf import settings

API_VERSION = getattr(settings, 'API_VERSION', '1.0.0')  # Por si no está definida

def api_success(data=None, message="Operación exitosa", status_code=200):
  return Response({
    "success": True,
    "version": API_VERSION,
    "status": status_code,
    "message": message,
    "data": data or {}
  }, status=status_code)

def api_error(message="Error en la operación", errors=None, status_code=400):
  return Response({
    "success": False,
    "version": API_VERSION,
    "status": status_code,
    "message": message,
    "errors": errors or {}
  }, status=status_code)