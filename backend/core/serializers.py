from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from core.models import AccessLog

class AccessLogSerializer(serializers.ModelSerializer):
  """
  Serializador para el historial de accesos al sistema.
  Incluye información sobre el usuario, la dirección IP, la acción realizada y la fecha y hora del acceso.
  """

  user_email = serializers.EmailField(source="user.email", read_only=True)

  class Meta:
    model = AccessLog
    fields = ['id', 'user_email', 'ip_address', 'action', 'timestamp', 'user_agent', 'object_id', 'object_type']

class RolesDetailSerializer(serializers.ModelSerializer):
  permissions = serializers.SerializerMethodField()

  class Meta:
    model = Group
    fields = ["id", "name", "permissions"]

  def get_permissions(self, group):
    return [
      {
        "id": perm.id,
        "codename": perm.codename,
        "name": perm.name,
        "app_label": perm.content_type.app_label,
        "model": perm.content_type.model,
      }
      for perm in group.permissions.select_related("content_type").all()
    ]

class RolesCreateSerializer(serializers.ModelSerializer):
  """
  Serializador para crear un grupo (rol) con permisos.
  Permite asignar múltiples permisos al grupo al momento de su creación.
  """

  permissions = serializers.PrimaryKeyRelatedField(
    queryset=Permission.objects.all(),
    many=True,
    write_only=True,
  )

  class Meta:
    model = Group
    fields = ["name", "permissions"]

  def create(self, validated_data):
    permissions = validated_data.pop("permissions", [])
    group = Group.objects.create(**validated_data)
    group.permissions.set(permissions)
    return group

class RolesUpdateSerializer(serializers.ModelSerializer):
  """
  Serializador para actualizar un grupo (rol) existente.
  Permite modificar el nombre del grupo y sus permisos asociados.
  """

  permissions = serializers.PrimaryKeyRelatedField(
    queryset=Permission.objects.all(),
    many=True,
    write_only=True,
  )

  class Meta:
    model = Group
    fields = ["name", "permissions"]

  def update(self, instance, validated_data):
    permissions = validated_data.pop("permissions", [])
    instance.name = validated_data.get("name", instance.name)
    instance.save()
    instance.permissions.set(permissions)
    return instance