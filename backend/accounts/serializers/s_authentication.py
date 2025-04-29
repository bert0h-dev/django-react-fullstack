from rest_framework.serializers import Serializer, EmailField, CharField, ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.messages import MSG_ERRORS

# Serializador de login
class LoginSerializer(TokenObtainPairSerializer):
  email = EmailField()
  password = CharField(write_only=True)

# Serializador de logout
class LogoutSerializer(Serializer):
  refresh = CharField()

  def validate(self, attrs):
    refresh_token = attrs.get('refresh')
    if not refresh_token:
      raise ValidationError([MSG_ERRORS['token_required']])
    return attrs

# Valida el refresh token.
class RefreshTokenSerializer(Serializer):
  refresh = CharField()

  def validate(self, attrs):
    refresh_token = attrs.get('refresh')
    if not refresh_token:
      raise ValidationError([MSG_ERRORS['token_required']])
    return attrs