import threading

_user = threading.local()

# Obtiene el usuario actual del hilo local.
def get_current_user():
  return getattr(_user, 'current_user', None)

# Middleware para almacenar el usuario actual en un hilo local.
class ThreadLocalUserMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    _user.value = request.user if request.user.is_authenticated else None
    response = self.get_response(request)
    return response