from rest_framework.serializers import Serializer, PrimaryKeyRelatedField, ValidationError

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from core.messages import MSG_ERRORS

User = get_user_model()

class PermissionAssignUserSerializer(Serializer):
  permissions = PrimaryKeyRelatedField(
    queryset=Permission.objects.all(),
    many=True
  )

  def validate_permissions(self, value):
    if not isinstance(value, list):
      raise ValidationError([MSG_ERRORS['permission_do_not_exists']])
    return value

  def save(self, user):
    user.user_permissions.set(self.validated_data['permissions'])
    user.save()
    return user