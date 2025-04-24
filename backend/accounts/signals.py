from django.db.models.signals import post_migrate, post_save, pre_save
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver

from .models import User
from core.models import AccessLog
from core.utils.models import get_model_name
from core.middleware.thread_user import get_current_user

User = get_user_model()
_old_passwords = {}

@receiver(post_migrate)
def set_custom_account_permissions(sender, **kwargs):
  if sender.name != 'accounts':
    return
  
  ct = ContentType.objects.get_for_model(User)
  
  perms = {
    'add_user': _("Puede crear usuarios"),
    'change_user': _("Puede editar usuarios"),
    'delete_user': _("Puede eliminar usuarios"),
    'view_user': _("Puede ver usuarios"),
  }

  for codename, name in perms.items():
    try:
      perm = Permission.objects.get(codename=codename, content_type=ct)
      perm.name = name
      perm.save()
    except Permission.DoesNotExist:
      continue

@receiver(pre_save, sender=User)
def store_old_password(sender, instance, **kwargs):
  if instance.pk:
    try:
      old_instance = sender.objects.get(pk=instance.pk)
      _old_passwords[instance.pk] = old_instance.password
    except sender.DoesNotExist:
      _old_passwords[instance.pk] = None

@receiver(post_save, sender=User)
def log_user_save(sender, instance, created, **kwargs):
  user = get_current_user()
  if not user or not user.is_authenticated:
    return
  
  ip = user.last_ip or "Desconocido"
  password_changed = False
  action = ""

  if not created:
    old_password = _old_passwords.pop(instance.pk, None)
    password_changed = old_password and old_password != instance.password

  if created:
    action = f"Registro de nuevo usuario: {instance.email}"
  elif password_changed:
    action = f"Cambio de contraseña: {instance.email}"
  else:
    action = f"Actualización de usuario: {instance.email}"

  AccessLog.objects.create(
    user=user,
    ip_address=ip,
    timestamp=now(),
    object_id=instance.id,
    object_type=get_model_name(instance),
    action=action,
    user_agent="Autolog"
  )