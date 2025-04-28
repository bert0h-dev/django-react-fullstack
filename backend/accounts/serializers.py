from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import get_user_model
from django.utils import timezone
from zoneinfo import ZoneInfo

from core.messages import ACCOUNT_ERRORS
from .models import User

User = get_user_model()

# Helper para lanzar ValidationError con mensajes centralizadoscd 
def validation_error(code):
  return serializers.ValidationError([ACCOUNT_ERRORS[code]])

# Listar los usuarios
class UserSerializer(serializers.ModelSerializer):
  last_activity_local = serializers.SerializerMethodField()

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
class ChangePasswordSerializer(serializers.Serializer):
  current_password = serializers.CharField(write_only=True)
  new_password = serializers.CharField(write_only=True)
  confirm_password = serializers.CharField(write_only=True)

  def validate(self, attrs):
    user = self.context['request'].user

    if not user.check_password(attrs.get('current_password')):
      raise validation_error("invalid_current_password")

    if attrs.get('new_password') != attrs.get('confirm_password'):
      raise validation_error("passwords_do_not_match")

    return attrs

  def save(self, **kwargs):
    user = self.context['request'].user
    user.set_password(self.validated_data['new_password'])
    user.requires_password_reset = False
    user.save()
    return user

# Serializador de login
class LoginSerializer(TokenObtainPairSerializer):
  email = serializers.EmailField()
  password = serializers.CharField(write_only=True)

# Serializador de logout
class LogoutSerializer(serializers.Serializer):
  refresh = serializers.CharField()

  def validate(self, attrs):
    refresh_token = attrs.get('refresh')
    if not refresh_token:
      raise validation_error("token_required")
    return attrs

# Valida el refresh token.
class RefreshTokenSerializer(serializers.Serializer):
  refresh = serializers.CharField()

  def validate(self, attrs):
    refresh_token = attrs.get('refresh')
    if not refresh_token:
      raise validation_error("token_required")
    return attrs