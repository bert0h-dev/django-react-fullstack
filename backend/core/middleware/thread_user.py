import threading

_user = threading.local()

def get_current_user():
  """
  Obtiene el usuario actual del hilo local.
  """
  return getattr(_user, 'current_user', None)

class ThreadLocalUserMiddleware:
  """
  Middleware para almacenar el usuario actual en un hilo local.
  """
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    _user.value = request.user if request.user.is_authenticated else None
    response = self.get_response(request)
    return response