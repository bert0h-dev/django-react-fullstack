from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from .models import AccessTokenBlacklist

class CustomJWTAuthentication(JWTAuthentication):
  """
  Esta clase extiende la autenticacion JWT para verificar si el token
  ha sido revocado. Si el token ha sido revocado, se lanza una excepcion
  de autenticacion.
  """
  def authenticate(self, request):
    result = super().authenticate(request)
    if result is None:
      return None
    
    if result is not None:
      user, token = result
      jti = token.get('jti')
      if AccessTokenBlacklist.objects.filter(token=jti).exists():
        raise AuthenticationFailed('Este token ha sido invalidado. Inicia sesión de nuevo.')
      return user, token

    return None