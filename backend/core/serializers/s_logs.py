from rest_framework import serializers

from django.contrib.auth.models import Group, Permission

from core.models import AccessLog

# Serializador para el historial de accesos al sistema.
class AccessLogSerializer(serializers.ModelSerializer):
  user_email = serializers.EmailField(source="user.email", read_only=True)

  class Meta:
    model = AccessLog
    fields = [
      'id',
      'user',
      'user_email',
      'method',
      'path',
      'action',
      'status_code',
      'message',
      'ip_address',
      'user_agent',
      'created_at'
    ]