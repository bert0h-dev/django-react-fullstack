from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from core.messages import MSG_LOGS, MSG_SUCCESS
from core.responses import api_success
from core.decorators import log_view_action
from core.permissions import IsAdminOrStaff
from core.utils.mixins import ListOnlyMixin
from core.utils.models import get_model_name

from accounts.filters import UserFilter
from accounts.serializers.s_users import UserSerializer, ChangePasswordSerializer

User = get_user_model()

@extend_schema_view(
  list=extend_schema(
    summary="Listar usuarios del sistema",
    description="Permite listar usuarios del sistema. Solo accesible a administradores o staff.",
    parameters=[
      OpenApiParameter(name='email', description='Filtrar por email', required=False, type=str),
      OpenApiParameter(name='first_name', description='Filtrar por nombre', required=False, type=str),
      OpenApiParameter(name='last_name', description='Filtrar por apellido', required=False, type=str),
      OpenApiParameter(name='is_active', description='Filtrar por estado activo', required=False, type=bool),
    ]
  ),
  create=extend_schema(
    summary="Crear un nuevo usuario",
    description="Permite crear usuarios en el sistema. Solo accesible a administradores o staff.",
  ),
  retrieve=extend_schema(
    summary="Detalle de un usuario",
    description="Permite ver el detalle de un usuario en espeficio. Solo accesible a administradores o staff.",
  ),
  update=extend_schema(
    summary="Actualización de la información de un usuario",
    description="Permite actualizar la información de un usuario en especifico. Solo accesible a administradores o staff.",
  ),
  partial_update=extend_schema(
    summary="Actualización de información parcial de un usuario",
    description="Permite actualizar la información de manera parcial de un usuario en especifico. Solo accesible a administradores o staff.",
  ),
  destroy=extend_schema(
    summary="Eliminar un usuario del sistema",
    description="Permite eliminar un usuario dentro del sistema. Solo accesible a administradores o staff.",
  )
)
class UserViewSet(ListOnlyMixin, ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [IsAdminOrStaff]
  filter_backends = [DjangoFilterBackend]
  filterset_class = UserFilter

  # Configuracion de mixin
  log_list_action = MSG_LOGS["user_list"]
  message_list = MSG_SUCCESS["user_list"]

  def get_queryset(self):
    return User.objects.select_related('user').all()
  
  @log_view_action(
    MSG_LOGS["user_details"],
    object_getter=lambda self, request, kwargs: self.get_object().email,
    object_meta=lambda self, request, kwargs: {
      "id": self.get_object().id,
      "type": get_model_name(self.get_object())
    }
  )
  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)
    return api_success(data=serializer.data, message=MSG_SUCCESS["user_details"])
  
  @log_view_action(
    MSG_LOGS["user_create"], 
    object_getter=lambda self, request, kwargs: self.get_object().email,
    object_meta=lambda self, request, kwargs: {
      "id": self.get_object().id,
      "type": get_model_name(self.get_object())
    }
  )
  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    return api_success(data=serializer.data, message=MSG_SUCCESS["user_create"], status_code=status.HTTP_201_CREATED)

  @log_view_action(
    MSG_LOGS["user_update"],
    object_getter=lambda self, request, kwargs: self.get_object().email,
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
    return api_success(data=serializer.data, message=MSG_SUCCESS["user_update"])
  
  @log_view_action(MSG_LOGS["user_destroy"])
  def destroy(self, request, *args, **kwargs):
    instance = self.get_object()
    self.perform_destroy(instance)
    return api_success(message=MSG_SUCCESS["user_destroy"], status_code=status.HTTP_204_NO_CONTENT)

@extend_schema(
  summary="Cambiar contraseña del usuario autenticado",
  description="Permite cambiar la contraseña del usuario autenticado. Se requiere proporcionar la contraseña actual y la nueva contraseña.",
  request=ChangePasswordSerializer,
  responses={200: None},
)
class ChangePasswordView(APIView):
  serializer_class = ChangePasswordSerializer
  permission_classes = [IsAdminOrStaff]

  @log_view_action(
    MSG_LOGS["user_password_update"], 
    object_getter=lambda self, request, kwargs: self.get_object().email,
    object_meta=lambda self, request, kwargs: {
      "id": self.get_object().id,
      "type": get_model_name(self.get_object())
    }
  )
  def put(self, request, user_id, *args, **kwargs):
    user = User.objects.get(id=user_id)

    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user.set_password(serializer.validated_data['new_password'])
    user.save()

    return api_success(message=MSG_SUCCESS["user_password_update"])