from django.utils.translation import gettext_lazy as _

ACCOUNT_ERRORS = {
  'invalid_email': _("El formato del email no es válido."),
  'email_exists': _("Ya existe un usuario con ese email."),

  'invalid_current_password': _("La contraseña actual es incorrecta."),
  'passwords_do_not_match': _("Las contraseñas no coinciden."),

  'first_name_letters_only': _("El primer nombre solo puede contener letras."),
  'first_name_too_short': _("El primer nombre debe tener al menos 2 caracteres."),
  'last_name_letters_only': _("El segundo nombre solo puede contener letras."),
  'last_name_too_short': _("El segundo nombre debe tener al menos 2 caracteres."),
  
  'first_surname_letters_only': _("El primer apellido solo puede contener letras."),
  'first_surname_too_short': _("El primer apellido debe tener al menos 2 caracteres."),
  'last_surname_letters_only': _("El segundo apellido solo puede contener letras."),
  'last_surname_too_short': _("El segundo apellido debe tener al menos 2 caracteres."),

  'user_not_found': _("No se encontró ninguna cuenta con ese correo."),
  'invalid_password': _("Contraseña incorrecta."),
  'not_verified': _("Tu cuenta aún no ha sido verificada."),
  'account_disabled': _("Esta cuenta está desactivada."),
  'missing_refresh_token': _("El token de actualización es requerido."),
}