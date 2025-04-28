from django.utils import translation

# Middleware que activa el idioma configurado en el modelo del usuario autenticado.
# Debe ir después de AuthenticationMiddleware y antes de LocaleMiddleware.
class LanguageFromUserMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    # Si el usuario está autenticado, establece su idioma
    if request.user.is_authenticated:
      language = getattr(request.user, 'language', 'es')
      translation.activate(language)
      request.LANGUAGE_CODE = language
      
    return self.get_response(request)