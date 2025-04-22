# core/messages.py

ACCOUNT_ERRORS = {
  'invalid_email': "El formato del email no es válido.",
  'email_exists': "Ya existe un usuario con ese email.",

  'first_name_letters_only': "El primer nombre solo puede contener letras.",
  'first_name_too_short': "El primer nombre debe tener al menos 2 caracteres.",
  'last_name_letters_only': "El segundo nombre solo puede contener letras.",
  'last_name_too_short': "El segundo nombre debe tener al menos 2 caracteres.",
  
  'first_surname_letters_only': "El primer apellido solo puede contener letras.",
  'first_surname_too_short': "El primer apellido debe tener al menos 2 caracteres.",
  'last_surname_letters_only': "El segundo apellido solo puede contener letras.",
  'last_surname_too_short': "El segundo apellido debe tener al menos 2 caracteres.",

  'user_not_found': "El Email/Usuario no está registrado.",
  'invalid_password': "Contraseña incorrecta.",
  'not_verified': "Tu cuenta aún no ha sido verificada.",
  'account_disabled': "Esta cuenta está desactivada.",
  'missing_refresh_token': "El token de actualización es requerido.",
}