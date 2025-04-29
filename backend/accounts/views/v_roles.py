from rest_framework import status 
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet

from drf_spectacular.utils import extend_schema, extend_schema_view
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.contrib.auth.models import Group

from core.messages import MSG_LOGS, MSG_SUCCESS, MSG_ERRORS
from core.responses import api_success, api_error
from core.decorators import log_view_action
from core.permissions import IsAdminOrStaff
from core.utils.mixins import ListOnlyMixin
from core.utils.models import get_model_name

from accounts.serializers.s_roles import RolesSerializer, RolesAssignUserSerializer

User = get_user_model()

@extend_schema_view(
  list=extend_schema(
    summary="Listar roles",
    description="Lista todos los roles del sistema."
  ),
  retrieve=extend_schema(
    summary="Ver detalle de rol",
    description="Devuelve los detalles de un rol específico."
  ),
  create=extend_schema(
    summary="Crear nuevo rol",
    description="Crea un nuevo rol en el sistema."
  ),
  update=extend_schema(
    summary="Actualizar rol",
    description="Actualiza completamente un rol existente."
  ),
  partial_update=extend_schema(
    summary="Actualizar parcialmente rol",
    description="Actualiza algunos campos de un rol existente."
  ),
  destroy=extend_schema(
    summary="Eliminar rol",
    description="Elimina un rol si no tiene usuarios asignados."
  )
)
class RoleViewSet(ListOnlyMixin, ModelViewSet):
  queryset = Group.objects.all().annotate(user_count=Count('user'))
  serializer_class = RolesSerializer
  permission_classes = [IsAdminOrStaff]

  # Configuracion de mixin
  log_list_action = MSG_LOGS["role_list"]
  success_list = MSG_SUCCESS["role_list"]

  @log_view_action(
    MSG_LOGS["role_details"], 
    object_getter=lambda self, request, kwargs: self.get_object().name,
    object_meta=lambda self, request, kwargs: {
      "id": self.get_object().id,
      "type": get_model_name(self.get_object())
    }
  )
  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)
    return api_success(data=serializer.data, message=MSG_SUCCESS["role_details"])

  @log_view_action(
    MSG_LOGS["role_create"], 
    object_getter=lambda self, request, kwargs: self.get_object().name,
    object_meta=lambda self, request, kwargs: {
      "id": self.get_object().id,
      "type": get_model_name(self.get_object())
    }
  )
  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    return api_success(data=serializer.data, message=MSG_SUCCESS["role_create"], status_code=status.HTTP_201_CREATED)
  
  @log_view_action(
    MSG_LOGS["role_update"], 
    object_getter=lambda self, request, kwargs: self.get_object().name,
    object_meta=lambda self, request, kwargs: {
      "id": self.get_object().id,
      "type": get_model_name(self.get_object())
    }
  )
  def update(self, request, *args, **kwargs):
    partial = kwargs.pop('partial', False)
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)
    return api_success(data=serializer.data, message=MSG_SUCCESS["role_details"])
  
  @log_view_action(MSG_LOGS["role_destroy"])
  def destroy(self, request, *args, **kwargs):
    instance = self.get_object()
    if instance.user_set.exists():
      return api_error(message=MSG_ERRORS["role_do_assign"], status_code=status.HTTP_400_BAD_REQUEST)
    self.perform_destroy(instance)
    return api_success(message=MSG_SUCCESS["role_destroy"], status_code=status.HTTP_204_NO_CONTENT)

@extend_schema(
  summary="Asignar rol a usuario",
  description="Asigna un rol específico a un usuario. Elimina roles anteriores y asigna solo el nuevo rol."
)
class RoleAssignUserView(GenericAPIView):
  serializer_class = RolesAssignUserSerializer
  permission_classes = [IsAdminOrStaff]

  @log_view_action(
    MSG_LOGS["role_assign"],
    object_getter=lambda self, request, kwargs: self.get_object().name,
    object_meta=lambda self, request, kwargs: {
      "id": self.get_object().id,
      "type": get_model_name(self.get_object())
    }
  )
  def post(self, request, user_id, *args, **kwargs):
    try:
      user = User.objects.get(id=user_id)
    except User.DoesNotExist:
      return api_error(message=MSG_ERRORS["user_do_not_exists"], status_code=status.HTTP_400_BAD_REQUEST)

    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(user=user)
    return api_success(data=serializer.data, message=MSG_SUCCESS["role_assign"])