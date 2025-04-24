from rest_framework import generics, status

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import AccessLog
from .filters import AccessLogFilter
from .decorators import log_view_action
from .responses import api_success, api_error
from .serializers import (
  # Logs
  AccessLogSerializer,
  # Roles
  RolesDetailSerializer,
  RolesCreateSerializer, 
  RolesUpdateSerializer
)
from .permissions import (
  # Logs
  CanViewLog, 
  # Roles
  CanViewGroup, CanCreateGroup, 
  CanUpdateGroup, CanDeleteGroup
)
from .utils.models import get_model_name

User = get_user_model()

@extend_schema(
    summary="Historial de acciones del sistema",
    description="Devuelve una lista paginada y filtrable de logs de acceso/auditoría.",
    parameters=[
      OpenApiParameter("user", int, description="Filtrar por ID de usuario"),
      OpenApiParameter("ip_address", str, description="Filtrar por IP"),
      OpenApiParameter("action", str, description="Buscar en acciones"),
      OpenApiParameter("object_type", str, description="Filtrar por modelo afectado"),
      OpenApiParameter("date_after", str, description="Fecha desde (YYYY-MM-DD)"),
      OpenApiParameter("date_before", str, description="Fecha hasta (YYYY-MM-DD)"),
    ]
)
class AccessLogListView(generics.ListAPIView):
  queryset = AccessLog.objects.select_related("user").order_by("-timestamp")
  serializer_class = AccessLogSerializer
  permission_classes = [CanViewLog]
  filter_backends = [DjangoFilterBackend]
  filterset_class = AccessLogFilter

  def list(self, request, *args, **kwargs):
    page = self.paginate_queryset(self.get_queryset())
    serializer = self.get_serializer(page, many=True)
    return api_success(data=self.get_paginated_response(serializer.data).data, message="Historial de accesos")

@extend_schema(
    summary="Listar roles (grupos)",
    description="Devuelve todos los grupos del sistema con sus permisos asignados, filtrando por apps definidas.",
    responses={200: None}
)
class RolesListView(generics.ListAPIView):
  """
  Vista para listar los grupos (roles) del sistema.
  """
  permission_classes = [CanViewGroup]

  def get(self, request):
    allowed_apps = getattr(settings, "PROJECT_PERMISSION_APPS", [])
    data = []

    for group in Group.objects.prefetch_related("permissions"):
      permisos_filtrados = group.permissions.filter(
        content_type__app_label__in=allowed_apps
      ).select_related("content_type")

      permissions_list = [
        {
          "id": perm.id,
          "codename": perm.codename,
          "name": perm.name,
          "app_label": perm.content_type.app_label,
          "model": perm.content_type.model,
        }
        for perm in permisos_filtrados
      ]

      data.append({
        "id": group.id,
        "name": group.name,
        "permissions": permissions_list
      })

    return api_success(data=data, message="Roles listados correctamente")

@extend_schema(
    summary="Obtener detalle de un rol",
    description="Devuelve nombre y permisos asignados de un grupo específico.",
    responses={200: RolesDetailSerializer}
)
class RolesDetailView(generics.RetrieveAPIView):
  queryset = Group.objects.prefetch_related("permissions__content_type")
  serializer_class = RolesDetailSerializer
  permission_classes = [CanViewGroup]
  lookup_url_kwarg = "id"

  @log_view_action(
    "Visualizó el detalle del rol:", 
    object_getter=lambda self, request, kwargs: self.get_object().name,
    object_meta=lambda self, request, kwargs: {
      "id": self.get_object().id,
      "type": get_model_name(self.get_object())
    }
  )
  def get(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)
    return api_success(data=serializer.data, message="Detalle del rol")

@extend_schema(
  summary="Crear nuevo rol (grupo)",
  description="Permite crear un nuevo rol y asignar permisos.",
  request=RolesCreateSerializer,
  responses={201: RolesCreateSerializer}
)
class RolesCreateView(generics.CreateAPIView):
  queryset = Group.objects.all()
  serializer_class = RolesCreateSerializer
  permission_classes = [CanCreateGroup]

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    return api_success(data=response.data, message="Rol creado correctamente", status_code=status.HTTP_201_CREATED)

@extend_schema(
  summary="Actualizar un rol (grupo)",
  description="Permite modificar el nombre de un grupo y reasignar permisos.",
  request=RolesUpdateSerializer,
  responses={200: RolesUpdateSerializer},
)
class RolesUpdateView(generics.UpdateAPIView):
  queryset = Group.objects.all()
  serializer_class = RolesUpdateSerializer
  permission_classes = [CanUpdateGroup]
  lookup_url_kwarg = "id"

  def patch(self, request, *args, **kwargs):
    response = super().partial_update(request, *args, **kwargs)
    return api_success(data=response.data, message="Rol actualizado correctamente")

@extend_schema(
  summary="Eliminar un rol (grupo)",
  description="Permite eliminar un grupo si no está asignado a ningún usuario.",
  responses={204: None}
)
class RolesDeleteView(generics.DestroyAPIView):
  queryset = Group.objects.all()
  permission_classes = [CanDeleteGroup]
  lookup_url_kwarg = "id"

  def delete(self, request, *args, **kwargs):
    group = self.get_object()

    # 🔒 Validar si el grupo está en uso
    users_with_group = User.objects.filter(groups=group)
    if users_with_group.exists():
      return api_error(message="No se puede eliminar este rol porque está asignado a uno o más usuarios.", status_code=status.HTTP_400_BAD_REQUEST)

    group.delete()
    return api_success(message="Rol eliminado correctamente", status_code=status.HTTP_204_NO_CONTENT)