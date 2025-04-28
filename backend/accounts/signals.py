from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver

from .models import User

User = get_user_model()

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