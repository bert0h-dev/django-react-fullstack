import re

from rest_framework.serializers import Serializer, ModelSerializer, SerializerMethodField, CharField, ValidationError

from django.contrib.auth import get_user_model
from django.utils import timezone
from zoneinfo import ZoneInfo

from core.messages import MSG_ERRORS
from accounts.models import User

User = get_user_model()

# Listar los usuarios
class UserSerializer(ModelSerializer):
  last_activity_local = SerializerMethodField()

  class Meta:
    model = User
    fields = [
      'id', 'email', 'username', 
      'first_name', 'last_name', 
      'user_type', 'is_active', 
      'last_activity', 'last_activity_local', 
      'timezone'
    ]

  def get_last_activity_local(self, obj):
    if not obj.last_activity:
      return None
    
    # Convertir la fecha y hora UTC a la zona horaria del usuario
    try:
      tz = ZoneInfo(obj.timezone or "UTC")
    except Exception:
      tz = ZoneInfo("UTC")

    dt = obj.last_activity
    if timezone.is_naive(dt):
      dt = timezone.make_aware(dt)
    
    return timezone.localtime(dt, timezone=tz).strftime("%Y-%m-%d %H:%M:%S")

# Cambiar la contraseña del usuario
class ChangePasswordSerializer(Serializer):
  current_password = CharField(write_only=True)
  new_password = CharField(write_only=True)
  confirm_password = CharField(write_only=True)

  def validate(self, attrs):
    user = self.context['request'].user
    current_pass = attrs.get('current_password')
    password = attrs.get['new_password']
    confirm = attrs.get['confirm_password']

    if not user.check_password(current_pass):
      raise ValidationError(MSG_ERRORS['invalid_current_password'])

    if password != confirm:
      raise ValidationError(MSG_ERRORS['passwords_do_not_match'])
    
    # Validaciones extra
    if len(password) < 8:
      raise ValidationError(MSG_ERRORS['password_do_short'])
    if not re.search(r"[A-Z]", password):
      raise ValidationError(MSG_ERRORS['password_any_uppercase'])
    if not re.search(r"[a-z]", password):
      raise ValidationError(MSG_ERRORS['password_any_lowercase'])
    if not re.search(r"[0-9]", password):
      raise ValidationError(MSG_ERRORS['password_any_number'])
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
      raise ValidationError(MSG_ERRORS['password_any_special'])

    return attrs