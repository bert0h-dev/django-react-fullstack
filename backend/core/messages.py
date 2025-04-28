from django.utils.translation import gettext_lazy as _

ACCOUNT_ERRORS = {
  'invalid_credentials': _("Credenciales inválidas."),
  'account_disabled': _("Esta cuenta está desactivada."),
  'token_required': _("El token es requerido."),
  'token_invalid': _("El token es inválido o ya ha sido cerrado."),
}

ACCOUNT_SUCCESS = {
  'login': _("Inicio de sesión exitoso."),
  'logout': _("Cierre de sesión exitoso."),
  'token_refresh': _("Token actualizado exitosamente."),

  'user_list': _("Lista de usuarios."),
  'user_details': _("Detalles del usuario."),
  'user_create': _("Usuario creado exitosamente."),
  'user_update': _("Usuario actualizado correctamente."),
  'user_destroy': _("Usuario eliminado correctamente."),
}

ACCOUNT_LOG = {
  'login': _("Inicio de sesión"),
  'logout': _("Cierre de sesión"),
  'token_refresh': _("Actualización de token"),

  'log_list': _("Visualizó el listado de logs"),
  'log_details': _("Visualizó los detalles del log"),

  'user_list': _("Visualizó el listado de usuarios"),
  'user_details': _("Visualizó los detalles del usuario"),
  'user_create': _("Creó un nuevo usuario"),
  'user_update': _("Actualizó el usuario"),
  'user_destroy': _("Eliminó el usuario"),
}