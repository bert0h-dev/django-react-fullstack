from rest_framework.serializers import Serializer, ModelSerializer, PrimaryKeyRelatedField, ValidationError

from django.contrib.auth.models import Group, Permission

from core.messages import MSG_ERRORS

class RolesSerializer(ModelSerializer):
  permissions = PrimaryKeyRelatedField(
    queryset=Permission.objects.all(), 
    many=True, 
    required=False
  )

  class Meta:
    model = Group
    fields = ['id', 'name', 'permissions']
    
  def validate_name(self, value):
    if Group.objects.exclude(id=self.instance.id if self.instance else None).filter(name=value).exists():
      raise ValidationError(MSG_ERRORS['role_do_exists'])
    return value

  def validate(self, attrs):
    if 'permissions' in attrs and not isinstance(attrs['permissions'], list):
      raise ValidationError(MSG_ERRORS['role_do_not_permisions'])
    return attrs
  
class RolesAssignUserSerializer(Serializer):
  role_id = PrimaryKeyRelatedField(
    queryset=Group.objects.all(),
    required=True
  )

  def save(self, user):
    role = self.validated_data['role_id']
    user.groups.clear()
    user.groups.add(role)
    user.save()
    return user