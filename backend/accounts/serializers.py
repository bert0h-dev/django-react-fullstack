from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers  import TokenObtainPairSerializer

from django.contrib.auth import get_user_model

import re
from core.messages import ACCOUNT_ERRORS
from datetime import timezone
from .models import User

User = get_user_model()

# 🔧 Helper para lanzar ValidationError con mensajes centralizados
def validation_error(code):
  return serializers.ValidationError([ACCOUNT_ERRORS[code]])

class UserSerializer(serializers.ModelSerializer):
  """
  Listar los usuarios
  """

  class Meta:
    model = User
    fields = ['id', 'email', 'first_name', 'last_name', 'first_surname', 'last_surname', 'is_verified', 'is_active', 'last_activity']

class RegisterSerializer(serializers.ModelSerializer):
  """
  Crear un nuevo usuario
  """

  password = serializers.CharField(write_only=True)

  class Meta:
    model = User
    fields = ['email', 'username', 'password', 'first_name', 'last_name', 'first_surname', 'last_surname']
    
  def validate_email(self, value):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_regex, value):
      raise validation_error("invalid_email")
    if User.objects.filter(email=value).exists():
      raise validation_error("email_exists")
    return value

  def validate_first_name(self, value):
    firs_name_regex = r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$'
    # if not re.match(firs_name_regex, value):
    if not value.isalpha():
      raise validation_error("first_name_letters_only")
    if len(value) < 2:
      raise validation_error("first_name_too_short")
    return value

  def validate_last_name(self, value):
    last_name_regex = r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$'
    if len(value) > 0:
      # if not re.match(last_name_regex, value):
      if not value.isalpha():
        raise validation_error("last_name_letters_only")
      if len(value) < 2:
        raise validation_error("last_name_too_short")
    return value
  
  def validate_first_surname(self, value):
    firs_surname_regex = r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$'
    # if not re.match(firs_name_regex, value):
    if not value.isalpha():
      raise validation_error("first_surname_letters_only")
    if len(value) < 2:
      raise validation_error("first_surname_too_short")
    return value

  def validate_last_surname(self, value):
    last_surname_regex = r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$'
    if len(value) > 0:
      # if not re.match(last_name_regex, value):
      if not value.isalpha():
        raise validation_error("last_surname_letters_only")
      if len(value) < 2:
        raise validation_error("last_surname_too_short")
    return value

  def create(self, validated_data):
    user = User(
      email=validated_data['email'],
      username=validated_data['username'],
      first_name=validated_data.get('first_name', ''),
      last_name=validated_data.get('last_name', ''),
      first_surname=validated_data.get('first_surname', ''),
      last_surname=validated_data.get('last_surname', ''),
      last_activity=timezone.now(),
    )
    user.set_password(validated_data['password'])
    user.is_verified = False
    user.requires_password_reset = True
    user.save()

    # Crear tokens
    refresh = RefreshToken.for_user(user)
    self._tokens  = {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
    }

    return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
  """
  Se obtiene el token de acceso y el token de actualización
  """

  def validate(self, attrs):
    login = attrs.get("username")  # puede ser username o email
    password = attrs.get("password")

    # Buscar por email o username
    user = User.objects.filter(email__iexact=login).first()
    if not user:
      user = User.objects.filter(username__iexact=login).first()

    if user is None:
      raise validation_error("username", "user_not_found")
    
    if not user.check_password(password):
      raise validation_error("password", "invalid_password")

    # Se valida si el usuario esta verificado
    if not user.is_verified:
      raise validation_error("verified", "not_verified")
    
    if not user.is_active:
      raise validation_error("active", "account_disabled")
    
    # Actualizar el campo de última actividad
    user.last_activity = timezone.now()
    user.save(update_fields=['last_activity'])
    
    # Autenticación correcta: generar tokens
    refresh = RefreshToken.for_user(user)
    data = {
      "refresh": str(refresh),
      "access": str(refresh.access_token),
      "user": {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "first_surname": user.first_surname,
        "last_surname": user.last_surname,
      }
    }

    return data

class LogoutSerializer(serializers.Serializer):
  """
  Cerrar sesión
  """

  refresh = serializers.CharField()

  def validate(self, attrs):
    refresh_token = attrs.get('refresh')
    if not refresh_token:
      raise validation_error("token", "missing_refresh_token")
    return attrs