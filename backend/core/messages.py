from django.utils.translation import gettext_lazy as _

MSG_ERRORS = {
  # Autenticacion
  'invalid_credentials': _("Credenciales inválidas."),
  'account_disabled': _("Esta cuenta está desactivada."),
  'token_required': _("El token es requerido."),
  'token_invalid': _("El token es inválido o ya ha sido cerrado."),
  # Usuarios
  'user_do_not_exists': _('Usuario no encontrado'),
  'invalid_current_password': _("La contraseña actual es incorrecta."),
  'passwords_do_not_match': _("Las contraseñas no coinciden."),
  'password_do_short': _("La contraseña debe tener al menos 8 caracteres."),
  'password_any_uppercase': _("La contraseña debe contener al menos una letra mayúscula."),
  'password_any_lowercase': _("La contraseña debe contener al menos una letra minúscula."),
  'password_any_number': _("La contraseña debe contener al menos un número."),
  'password_any_special': _("La contraseña debe contener al menos un carácter especial (!@#$% etc)."),
  # Roles
  'role_do_exists': _('Ya existe un rol con este nombre.'),
  'role_do_not_permisions': _('Debe ser una lista de IDs de permisos.'),
  'role_do_assign': _("No se puede eliminar un rol que tiene usuarios asignados"),
  # Permisos
  'permission_do_not_exists': _('Debe enviar una lista de IDs de permisos'),
}

MSG_SUCCESS = {
  # Autenticacion
  'login': _("Inicio de sesión exitoso."),
  'logout': _("Cierre de sesión exitoso."),
  'token_refresh': _("Token actualizado exitosamente."),
  # Usuarios
  'user_list': _("Lista de usuarios."),
  'user_details': _("Detalles del usuario."),
  'user_create': _("Usuario creado exitosamente."),
  'user_update': _("Usuario actualizado correctamente."),
  'user_password_update': _("Contraseña cambiada correctamente."),
  'user_destroy': _("Usuario eliminado correctamente."),
  # Roles
  'role_list': _("Lista de roles."),
  'role_details': _("Detalles del rol."),
  'role_create': _("Rol creado exitosamente."),
  'role_update': _("Rol actualizado exitosamente."),
  'role_destroy': _("Rol eliminado exitosamente."),
  'role_assign': _("Rol asignado exitosamente."),
  # Permisos
  'permission_assign': _("Permiso asignado exitosamente."),
  # Logs
  'log_list': _("Listado de logs de acceso."),
  'log_details': _("Detalle del log de acceso."),
}

MSG_LOGS = {
  # Autenticacion
  'login': _("Inicio de sesión"),
  'logout': _("Cierre de sesión"),
  'token_refresh': _("Actualización de token"),
  # Usuarios
  'user_list': _("Visualizó el listado de usuarios"),
  'user_details': _("Visualizó los detalles del usuario"),
  'user_create': _("Creó un nuevo usuario"),
  'user_update': _("Actualizó el usuario"),
  'user_password_update': _("Actualizó la contraseña del usuario"),
  'user_destroy': _("Eliminó el usuario"),
  # Roles
  'role_list': _("Visualizó el listado de roles"),
  'role_details': _("Visualizó el detalle del rol"),
  'role_create': _("Creó un nuevo rol"),
  'role_update': _("Actualizó el rol"),
  'role_destroy': _("Eliminó el rol"),
  'role_assign': _("Rol asignado"),
  # Permisos
  'permission_assign': _('Permiso asignado'),
  # Logs
  'log_list': _("Visualizó el listado de logs"),
  'log_details': _("Visualizó los detalles del log"),
  'log_export': _("Listado de logs de acceso con exportación."),
}