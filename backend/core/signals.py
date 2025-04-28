from django.db.models.signals import post_migrate, post_save, post_delete
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.dispatch import receiver

from .models import AccessLog
from .utils.models import get_model_name
from .middleware.thread_user import get_current_user

@receiver(post_migrate)
def set_custom_core_permissions(sender, **kwargs):
  if sender.name != 'core':
    return
  
  ct = ContentType.objects.get_for_model(AccessLog)
  
  perms = {
    'add_accesslog': _("Puede crear logs de acceso"),
    'change_accesslog': _("Puede editar logs de acceso"),
    'delete_accesslog': _("Puede eliminar logs de acceso"),
    'view_accesslog': _("Puede ver logs de acceso"),
  }

  for codename, name in perms.items():
    try:
      perm = Permission.objects.get(codename=codename, content_type=ct)
      perm.name = name
      perm.save()
    except Permission.DoesNotExist:
      continue

@receiver(post_migrate)
def rename_auth_model_permissions(sender, **kwargs):
  if sender.name != 'auth':
    return
  
  ct_group = ContentType.objects.get(app_label='auth', model='group')
  ct_permission = ContentType.objects.get(app_label='auth', model='permission')
  
  group_perms = {
    'add_group': _("Puede crear grupos"),
    'change_group': _("Puede editar grupos"),
    'delete_group': _("Puede eliminar grupos"),
    'view_group': _("Puede ver grupos"),
  }
  permission_perms = {
    'add_permission': _("Puede crear permisos"),
    'change_permission': _("Puede editar permisos"),
    'delete_permission': _("Puede eliminar permisos"),
    'view_permission': _("Puede ver permisos"),
  }
  
  for codename, new_name in permission_perms.items():
    try:
      perm = Permission.objects.get(codename=codename, content_type=ct_permission)
      perm.name = new_name
      perm.save()  
    except Permission.DoesNotExist:
      continue

  for codename, new_name in group_perms.items():
    try:
      perm = Permission.objects.get(codename=codename, content_type=ct_group)
      perm.name = new_name
      perm.save()
    except Permission.DoesNotExist:
      continue